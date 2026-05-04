import os
from langfuse import get_client, observe, Evaluation
from langfuse.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup clients
langfuse = get_client()
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# --- THE GENERATOR (The student) ---
def gemma_architect_task(item):
    """This is the function we are testing."""
    response = client.chat.completions.create(
        model="gemma4-pro:latest",
        messages=[
            {"role": "system", "content": "You are a senior software architect. Be technical and very brief."},
            {"role": "user", "content": item.input}
        ]
    )
    return response.choices[0].message.content

# --- THE JUDGE (The teacher) ---
@observe() # Important: This lets us see the Judge's thinking in the UI!
def gemma_judge(input, output, expected_output, **kwargs):
    """
    This function grades the student.
    'output' is what the student wrote.
    'item' is the dataset item (includes expected_output).
    """
    print(f"Judging output for: {input[:30]}...")

    judge_prompt = f"""
    You are an impartial judge grading an AI response.
    
    [User Question]: {input}
    [Expected Answer]: {expected_output}
    [Actual AI Response]: {output}
    
    Does the AI response match the facts in the Expected Answer? 
    Is it concise and technical?
    
    Respond with ONLY a number: 1 (Pass) or 0 (Fail).
    """

    response = client.chat.completions.create(
        model="gemma4-pro:latest",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0 # Keep the judge consistent
    )
    
    score_str = response.choices[0].message.content.strip()
    
    # Try to extract the number (sometimes Gemma adds extra text)
    score = 1.0 if "1" in score_str else 0.0
    
    # Returning this format tells Langfuse EXACTLY which config to use
    return Evaluation(
        name="architect-accuracy", # Must match your UI Score Config name
        value=score,
        comment=f"Judge reasoned: {score_str}" # Optional: help you debug later
    )

# --- RUN THE EXPERIMENT ---
def start_auto_eval():
    dataset = langfuse.get_dataset("Production-Benchmark")

    dataset.run_experiment(
        name="Gemma-Architect-Auto-Eval",
        task=gemma_architect_task,
        # The key move: Pass your judge function here!
        evaluators=[gemma_judge], 
        metadata={"judge_model": "gemma", "version": "v3"}
    )

if __name__ == "__main__":
    start_auto_eval()
    print("\nBatch complete! Check the 'Datasets' tab to see the auto-generated scores.")