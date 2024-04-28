from openai import OpenAI
from prompts import STAGE_1_PROMPT_new
import os


# Set OpenAI API key in environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

messages = []
system_message = STAGE_1_PROMPT_new

# Add the system's role message to the chat history
messages.append({"role": "system", "content": system_message})

while True:
    # User inputs their question or message
    user_message = input("Enter your question or message: ")
    messages.append({"role": "user", "content": user_message})

    # Generate response from the model considering the full chat history
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages = messages
    )
    print(response.choices[0].message.content.strip()) 
    
    # Check if the user has any more questions after receiving a recommendation
    if "recommendation" in response.choices[0].message.content.lower():
        follow_up = input("Do you have any more questions? (yes/no): ")
        if follow_up.lower() == "no":
            print("Thank you for chatting. Have a great day!")
            break

