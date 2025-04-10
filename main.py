import os
import json
import csv
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = OpenAI(api_key=openai_api_key)

# Load questions from JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

instructions = """
You are an Indian national taking the state services main examination from 2019.

- Choose the correct answer from the list of choices given by indicating a 1, 2, 3, or 4
- Only output 1, 2, 3, or 4. Do not use any other text
"""

# Prepare data for CSV export
results = []

# Test all questions
for item in questions:
    print(f"\nQuestion {item['question']}:")
    print(f"Query: {item['query']}")
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using gpt-3.5-turbo for testing
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": item['query']}
        ]
    )
    
    model_answer = completion.choices[0].message.content.strip()
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
total_questions = len(questions)
correct_answers = sum(1 for result in results if result['is_correct'])
accuracy = (correct_answers / total_questions) * 100

print(f"\nFinal Results:")
print(f"Total Questions: {total_questions}")
print(f"Correct Answers: {correct_answers}")
print(f"Accuracy: {accuracy:.2f}%")

# Export results to CSV
csv_filename = 'exam_results.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['question_id', 'query', 'gold_answer', 'model_answer', 'is_correct']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print(f"\nResults exported to {csv_filename}")