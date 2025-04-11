import os
import json
import csv
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

# Define the system prompt for Indian state services examination
system_prompt = """You are an Indian national taking the state services main examination from 2019.

- Choose the correct answer from the list of choices given by indicating a 1, 2, 3, or 4
- Only output 1, 2, 3, or 4. Do not use any other text"""

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

        # Load questions from JSON file
        with open('questions.json', 'r') as f:
            questions = json.load(f)
        
        # Prepare data for CSV export
        results = []
        
        # Process each question
        for item in questions:
            print(f"\nQuestion {item['question']}:")
            print(f"Query: {item['query']}")
            
            # Define the messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": item['query']}
            ]
            
            # Apply the chat template to the messages
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            print(f"\nProcessing prompt for question {item['question']}...")
            
            # Tokenize the prompt
            inputs = tokenizer(prompt, return_tensors="pt")
            
            # Generate with no_grad to save memory
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=10, temperature=0.1)
            
            # Decode the result
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the model's answer (this may need adjustment based on actual output format)
            model_answer = result.strip()[-1] if result.strip() and result.strip()[-1] in "1234" else "N/A"
            is_correct = model_answer == str(item['gold'])
            
            # Store results for CSV export
            results.append({
                'question_id': item['question'],
                'query': item['query'],
                'gold_answer': item['gold'],
                'model_answer': model_answer,
                'is_correct': is_correct
            })
            
            print(f"Model Answer: {model_answer}")
            print(f"Correct Answer: {item['gold']}")
            print(f"Correct: {is_correct}")
            print("-" * 50)
        
        # Calculate and print overall accuracy
        total_questions = len(results)
        correct_answers = sum(1 for result in results if result['is_correct'])
        accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        print(f"\nFinal Results:")
        print(f"Total Questions: {total_questions}")
        print(f"Correct Answers: {correct_answers}")
        print(f"Accuracy: {accuracy:.2f}%")

        # Export results to CSV
        csv_filename = 'sarvam_results.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['question_id', 'query', 'gold_answer', 'model_answer', 'is_correct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        print(f"\nResults exported to {csv_filename}")
        
    except Exception as e:
        print(f"\nError during model operations: {e}")
        print("This may be due to lacking permissions for the model or not having the required dependencies.")
