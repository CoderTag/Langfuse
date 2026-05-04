import os
import uuid
from langfuse.openai import OpenAI 
from langfuse import observe, get_client, propagate_attributes
from dotenv import load_dotenv

load_dotenv()

# Initialize the client for local Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

@observe()
def ask_ai_registry(user_question):
    langfuse = get_client()

    # 1. Fetch the prompt from the Langfuse Registry
    # This automatically tracks WHICH version of the prompt you used!
    langfuse_prompt = langfuse.get_prompt("architect-assistant", label="production")
    
    # 2. Compile the prompt with variables
    # This replaces {{specialty}} and {{question}} with real values
    compiled_prompt = langfuse_prompt.compile(
        specialty="Cloud Native", 
        question=user_question
    )

    # 3. Use the compiled prompt in your LLM call
    response = client.chat.completions.create(
        model="gemma4-pro:latest",
        messages=[{"role": "user", "content": compiled_prompt}],
        # This links the LLM call to this specific prompt version in the UI
        langfuse_prompt=langfuse_prompt 
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print(ask_ai_registry("What is the best way to scale a Docker container?"))