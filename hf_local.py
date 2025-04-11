import os
from dotenv import load_dotenv
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face API key
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY_READ")

# Print masked API key for verification
if HUGGING_FACE_API_KEY:
    # Show only the first 5 and last 5 characters of the API key
    masked_key = HUGGING_FACE_API_KEY[:5] + "..." + HUGGING_FACE_API_KEY[-5:]
    print(f"API key loaded: {masked_key}")
else:
    print("Failed to load API key from .env file")
    exit(1)

# Test if the API key is valid by making a simple API call to Hugging Face Hub
def test_api_key():
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    api_url = "https://huggingface.co/api/models"
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            print("API key is valid! Successfully connected to Hugging Face API.")
            return True
        else:
            print(f"API key validation failed. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error occurred while testing API key: {e}")
        return False

# Run the test
is_valid = test_api_key()

if is_valid:
    try:
        print("\nAttempting to load the sarvam-1 model...")
        
        # Load model and tokenizer
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("sarvamai/sarvam-1")
        print("Tokenizer loaded successfully!")
        
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained("sarvamai/sarvam-1")
        print("Model loaded successfully!")

        # Example usage
        text = "कर्नाटक की राजधानी है:"
        print(f"\nGenerating completion for: '{text}'")
        
        inputs = tokenizer(text, return_tensors="pt")
        
        # Generate with no_grad to save memory
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=5)
        
        result = tokenizer.decode(outputs[0])
        
        print(f"\nRESULT:\n-----\n\n{result}")
        
    except Exception as e:
        print(f"\nError during model operations: {e}")
        print("This may be due to lacking permissions for the model or not having the required dependencies.")
