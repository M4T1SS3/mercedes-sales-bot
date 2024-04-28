import json
import re


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


import re


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



text = """
Thanks for sharing that information! Based on your daily commute and the frequency of your vacations, it looks like you need an electric vehicle that offers great efficiency, comfort for long drives, and doesn't necessarily require a large amount of space. Considering these aspects, I'll recommend three Mercedes-Benz electric vehicles that could fit your needs very well. Here are the recommendations: { "car_recommendations": [ { "car_name": "EQE Sedan", "advantages": [ "Suitable for daily commutes with a focus on advanced technology and comfort, ideal for both work and long distance travel.", "Dynamic driving experience with efficient energy usage, perfect for your 30 km daily commute.", "Sleek design and luxurious interior, providing a pleasant driving experience for vacations and everyday usage." ] }, { "car_name": "EQA", "advantages": [ "Compact SUV offering efficiency and modern luxury, making it versatile for city commuting and occasional long journeys.", "Easy to handle and park in urban settings due to its compact size, yet comfortable enough for vacation travel.", "Stylish, with advanced features that ensure a smooth and enjoyable ride without the need for extensive space." ] }, { "car_name": "EQB", "advantages": [ "Offers the practicality of an SUV with the efficiency of an electric vehicle, suitable for regular commutes and vacation trips.", "More space than the EQA, giving you flexibility for any additional needs without being overly large.", "Environmentally friendly and stylish, bridging the gap between daily utility and leisure travel." ] } ] } Each of these options provides a balance of efficiency, comfort, and technology, tailored to both your daily commute and longer vacation drives. Do any of these stand out to you, or would you like more information on any specific model?"""
print(cut_json(text))
