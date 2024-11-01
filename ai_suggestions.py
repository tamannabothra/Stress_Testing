import requests
import json
import os

def fetch_logs(file_path):
    """Reads the log file content."""
    with open(file_path, 'r') as file:
        logs = file.read()
    return logs

def analyze_logs(log_content):
    """Sends the log content to the Gemini API for analysis."""
    url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Give One line brief suggestions on the log analysis provided for each function.\n\n"+log_content  # Send the actual log content
            }
        ],
        "model": "gpt-4o",
        "max_tokens": 100,
        "temperature": 0.9
    }
    
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),  # Use your API key
        "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    # Sending request to API
    response = requests.post(url, json=payload, headers=headers)

    # Check for success
    if response.status_code == 200:
        response_data = response.json()
        # Debugging
        print("Response Data:", json.dumps(response_data, indent=2))  # Pretty-print the response

        # Check if the expected keys are present
        if 'choices' in response_data and len(response_data['choices']) > 0:
            suggestions = response_data['choices'][0]['message']['content']
            return suggestions
        else:
            print("No suggestions found in the response.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Fetch and analyze logs
log_file = '/root/Stress_Testing/stress_test.log'
log_content = fetch_logs(log_file)
suggestions = analyze_logs(log_content)

# Save suggestions to a file if analysis was successful
if suggestions:
    with open('suggestions.txt', 'w') as file:
        file.write(suggestions)
    print("Suggestions saved to 'suggestions.txt'")
else:
    print("No suggestions available due to API error.")
