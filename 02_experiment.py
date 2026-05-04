import os
from langfuse import get_client
from langfuse.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Setup - get the global client
langfuse = get_client()
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# "Task" function says what we are actually testing. 
# It must take 'item' as a keyword argument.
def gemma_architect_task(item):
    response = client.chat.completions.create(
        model="gemma4-pro:latest",
        messages=[
            {"role": "system", "content": "You are a senior software architect. Answer concise and technical."},
            {"role": "user", "content": item.input}
        ]
    )
    # Return the string you want to save as the 'output' for this run
    return response.choices[0].message.content

# Run the Experiment
def start_benchmark():
    print("Fetching dataset...")
    # Pull your items from the UI dataset
    dataset = langfuse.get_dataset("Production-Benchmark")

    print(f"Running experiment on {len(dataset.items)} items...")
    
    # Iterate through each example in the dataset
    # It automatically creates the traces and links them to your dataset.
    dataset.run_experiment(
        name="Gemma-v2-Architect-Prompt",
        task=gemma_architect_task,
        metadata={"model": "gemma4-pro", "prompt_version": "v2"}
    )

if __name__ == "__main__":
    start_benchmark()
    print("\nExperiment complete! View the results in the Langfuse 'Datasets' tab.")