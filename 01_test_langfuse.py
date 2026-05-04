import os
import uuid
from langfuse.openai import OpenAI 
# CHANGED: Import get_client instead of Langfuse and langfuse_context
from langfuse import observe, get_client, propagate_attributes
from dotenv import load_dotenv

load_dotenv()

# Initialize the client for local Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

 # The @observe decorator handles OpenTelemetry context automatically
@observe() 
def ask_ai(question):
    # METADATA - pushes the metadata to this trace and any child spans automatically
    # propagate_attributes MUST be used with a 'with' block
    with propagate_attributes(
        metadata={"os": "macOS", "model_family": "gemma"}
    ):
        response = client.chat.completions.create(
            model="gemma4-pro:latest",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": question}
            ]
        )
    
    # FETCH: Call get_client() to tap into the active context and get the Trace ID
    langfuse = get_client()
    trace_id = langfuse.get_current_trace_id()
    
    return response.choices[0].message.content, trace_id

if __name__ == "__main__":
    print("Connecting to Gemma via Ollama...")
    
    # Grab the global singleton client for scoring later
    langfuse = get_client()

    while True:
        question = input("\nWhat is your Question (type 'exit' to stop): ")
        if question.lower() == 'exit': break
        
        answer, t_id = ask_ai(question)
        print(f"\nGemma's Reply: {answer}")

        # SIMULATING USER FEEDBACK
        feedback = input("\nWas this helpful? (y/n): ")
        score_val = 1 if feedback.lower() == 'y' else 0

        # UPDATED: Use create_score() for v4
        langfuse.create_score(
            trace_id=t_id,
            name="user-feedback",
            value=score_val,
            comment="User manually rated this in the terminal"
        )
        print(f"Feedback sent to Langfuse for trace: {t_id}")