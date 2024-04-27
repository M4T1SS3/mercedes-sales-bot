from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Set OpenAI API key in environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are an assistant specializing in recommending Mercedes-Benz electric vehicles. The customer is looking for a new car."},
        {"role": "user", "content": f": {user_message}"},
        ]
    )
    return jsonify({'response': response.choices[0].message.content.strip()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)