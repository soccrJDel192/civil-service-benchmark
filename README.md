# Civil Service Benchmark

This repository contains a benchmark test suite for evaluating different AI models on Indian Civil Service examination questions. The project tests various models including Claude, Hugging Face models, and local models like Krutrim.

## Project Structure

- `main.py` - Main entry point for running tests
- `claude.py` - Tests using Anthropic's Claude model
- `hugging_face.py` - Tests using Hugging Face API models
- `hf_local.py` - Tests using local Hugging Face models
- `questions.json` - Dataset of civil service examination questions
- `*.csv` - Results files from different model runs

## Prerequisites

- Python 3.12 or higher
- Git
- pip (Python package installer)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/soccrJDel192/civil-service-benchmark.git
cd civil-service-benchmark
```

2. Create and activate the required virtual environments:

### For Claude Tests (claude.py)
```bash
python -m venv claude-env
source claude-env/bin/activate  # On macOS/Linux
# or
.\claude-env\Scripts\activate  # On Windows
```

### For Hugging Face API Tests (hugging_face.py)
```bash
python -m venv hugging-face-env
source hugging-face-env/bin/activate  # On macOS/Linux
# or
.\hugging-face-env\Scripts\activate  # On Windows
```

### For Local Hugging Face Tests (hf_local.py)
```bash
python -m venv hf-local
source hf-local/bin/activate  # On macOS/Linux
# or
.\hf-local\Scripts\activate  # On Windows
```

3. Install dependencies for each environment:

#### Claude Environment
```bash
pip install -r requirements.txt
pip install anthropic
```

#### Hugging Face API Environment
```bash
pip install -r requirements.txt
pip install huggingface_hub
```

#### Local Hugging Face Environment
```bash
pip install -r requirements.txt
pip install torch transformers sentencepiece protobuf
```

4. Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
HUGGING_FACE_API_KEY_READ=your_hugging_face_api_key
```

5. Paste the JSON data into the `questions.json` file

Create a test dataset in .csv format and convert it to JSON. The JSON fields should be "question", "query", and "gold", where "question" is the number of the question (e.g. question 1,2,3), "query" is the actual question itself with the answers in it, and "gold" is the correct answer. See below for an example:

```  {
    "question": 2,
    "query": "The following persons were members of which Secret Society? (a) Mahadeo Vinayak Ranade, (b) Damodar Bhide, (c) Khanderao Sathe, (d) Balwant Natu. Choose from the following options: (1) Paramahansa Sabha, (2) Chaphekar Club, (3) Star Club, (4) Abhinav Bharat Society",
    "gold": 2
  } 
```

## Running Tests

### Claude Tests
```bash
source claude-env/bin/activate  # Activate Claude environment
python claude.py
deactivate  # Deactivate environment when done
```

### Hugging Face API Tests
```bash
source hugging-face-env/bin/activate  # Activate Hugging Face environment
python hugging_face.py
deactivate  # Deactivate environment when done
```

### Local Hugging Face Tests
```bash
source hf-local/bin/activate  # Activate local Hugging Face environment
python hf_local.py
deactivate  # Deactivate environment when done
```

## Results

The test results are saved in CSV files:
- `claude_results.csv` - Results from Claude model
- `huggingface_results.csv` - Results from Hugging Face API models
- `krutrim_results.csv` - Results from local Krutrim model

Each CSV file contains:
- Question ID
- Query text
- Gold standard answer
- Model's answer
- Whether the answer was correct

## Notes

- Make sure to deactivate each virtual environment after use
- The local Hugging Face tests require significant disk space and memory
- API keys should be kept secure and never committed to the repository
- Virtual environment directories are ignored in .gitignore

## Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are installed in the correct virtual environment
2. Verify your API keys are correctly set in the .env file
3. Check that you have sufficient disk space and memory for local model tests
4. Make sure you're using the correct Python version (3.12 or higher) 