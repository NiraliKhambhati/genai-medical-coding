from dotenv import load_dotenv
import anthropic

# Load your API key from the .env file
load_dotenv()

# Connect to Claude
client = anthropic.Anthropic()

# Send a test question
response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "In one sentence, what is ICD-10?"}
    ]
)

# Show Claude's answer
print(response.content[0].text)