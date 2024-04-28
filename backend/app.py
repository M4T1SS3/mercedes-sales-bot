from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from prompts import STAGE_1_PROMPT, STAGE_2_PROMPT
import json
import re

app = Flask(__name__)
CORS(app)

# Set OpenAI API key in environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Dictionary to store chat histories by session ID
chat_histories = {}
chat_stages = {}


def extract_json_from_text(text, stage):
    # Regular expression to capture everything between the first and last curly braces
    json_pattern = re.compile(r"\{.*\}", re.DOTALL)  # Matches the first set of enclosing braces

    # Search for the entire JSON structure
    match = json_pattern.search(text)  # Find the first JSON-like pattern

    if match:
        try:
            json_content = match.group(0)  # The full JSON content


            # Attempt to parse the JSON content
            parsed_json = json.loads(json_content)

            print("Parsed JSON\n----------------------\n")
            print(parsed_json)
            print("\n----------------------\n")

            if stage == 1:
                parsed_json = parsed_json.pop('car_recommendations')

            print("Parsed JSON2\n----------------------\n")
            print(parsed_json)
            print("\n----------------------\n")

            return parsed_json  # Return the parsed JSON
        except json.JSONDecodeError:

            # Handle invalid JSON
            print("Failed to parse JSON")
            return []
    else:
        # If no JSON pattern is found
        print("No JSON found in the text")
        return []


def cut_json(text):
    # Regular expression to find JSON-like patterns
    json_pattern = re.compile(r"\{.*?\}", re.DOTALL)  # Matches JSON-like objects

    # Find the first JSON-like pattern
    match = json_pattern.search(text)  # Finds the first occurrence of JSON

    if match:
        json_start = match.start()  # Start index of the JSON pattern

        # Cut out everything after the JSON
        remaining_text = text[:json_start]  # Everything from the start to the end of the JSON

        if remaining_text.endswith("```json"):
            remaining_text = remaining_text[:-6]

        return remaining_text
    else:
        # If no JSON pattern is found, return the entire text
        return text


@app.route('/chat', methods=['POST'])
def chat():
    print("Request received")
    session_id = request.json.get('session_id')
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # If no session_id provided, create a new one
    if not session_id:
        return jsonify({'error': 'No session_id provided'}), 400

    if session_id not in chat_histories:
        chat_histories[session_id] = []  # initialize the chat history for this session
        chat_stages[session_id] = 1  # initialize the chat stage for this session

    # Add the user's message to the chat history
    chat_histories[session_id].append({"role": "user", "content": user_message})

    # Prepare the chat context from history
    chat_context = chat_histories[session_id]  # get chat history for this session

    if chat_stages[session_id] == 1:
        prompt = STAGE_1_PROMPT
    else:
        prompt = STAGE_2_PROMPT

    # Add system instructions if it's the first message
    if len(chat_context) == 1:
        chat_context.insert(0, {"role": "system", "content": prompt})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=chat_context
    )

    # Add the AI's response to the chat history
    ai_response = response.choices[0].message.content.strip()

    chat_histories[session_id].append({"role": "assistant", "content": ai_response})

    car_recommendations = extract_json_from_text(ai_response, chat_stages[session_id])

    if car_recommendations and chat_stages[session_id] == 1:
        chat_stages[session_id] = 2
        chat_context.insert(0, {"role": "system", "content": STAGE_2_PROMPT})

    ai_response = cut_json(ai_response)

    # Return the response along with the session ID for future requests
    print(f"Session ID: {session_id}\n User: {user_message}\n AI: {ai_response}\n CAR RECOMMENDATIONS: "
          f"{car_recommendations}\n Stage: {chat_stages[session_id]}\n")
    return jsonify({'response': ai_response, 'session_id': session_id, 'car_recommendations': car_recommendations,
                    'end_of_chat': False})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
