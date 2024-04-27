from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from prompts import STAGE_1_PROMPT
import json
import re

app = Flask(__name__)
CORS(app)

# Set OpenAI API key in environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Dictionary to store chat histories by session ID
chat_histories = {}


def extract_json_from_text(text):
    # Regular expression to find JSON-like patterns
    json_pattern = re.compile(r"\{.*?\}", re.DOTALL)  # Matches JSON-like objects

    matches = json_pattern.findall(text)  # Find all JSON-like patterns in the text

    parsed_json = []

    for match in matches:
        try:
            # Attempt to parse each JSON-like match
            data = json.loads(match)
            parsed_json.append(data)  # Append valid JSON objects
        except json.JSONDecodeError:
            # Ignore invalid JSON
            pass

    return parsed_json


def cut_json(text):
    # Regular expression to find JSON-like patterns
    json_pattern = re.compile(r"\{.*?\}", re.DOTALL)  # Matches JSON-like objects

    # Find the first JSON-like pattern
    match = json_pattern.search(text)  # Finds the first occurrence of JSON

    if match:
        json_start = match.start()  # Start index of the JSON pattern

        # Cut out everything after the JSON
        remaining_text = text[:json_start]  # Everything from the start to the end of the JSON

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

    # Add the user's message to the chat history
    chat_histories[session_id].append({"role": "user", "content": user_message})

    # Prepare the chat context from history
    chat_context = chat_histories[session_id]  # get chat history for this session

    # Add system instructions if it's the first message
    if len(chat_context) == 1:
        chat_context.insert(0, {"role": "system", "content": STAGE_1_PROMPT})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=chat_context
    )

    # Add the AI's response to the chat history
    ai_response = response.choices[0].message.content.strip()
    chat_histories[session_id].append({"role": "assistant", "content": ai_response})

    car_recommendations = extract_json_from_text(ai_response)
    ai_response = cut_json(ai_response)

    # Return the response along with the session ID for future requests
    print(f"Session ID: {session_id}\n User: {user_message}\n AI: {ai_response}")
    return jsonify({'response': ai_response, 'session_id': session_id, 'car_recommendations': car_recommendations})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
