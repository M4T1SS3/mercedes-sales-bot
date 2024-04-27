from openai import OpenAI
import os


# Set OpenAI API key in environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


user_message = input("Enter prompt:")


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are an assistant specializing in recommending Mercedes-Benz electric vehicles. The customer is looking for a new car."},
    {"role": "user", "content": f": {user_message}"},
    ]
)
print(response.choices[0].message.content.strip())

