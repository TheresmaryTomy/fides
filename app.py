import ollama
from dotenv import load_dotenv

# Fides system prompt
system_prompt = """You are Fides, a faithful and trustworthy Catholic AI companion. 
You help Catholics with questions about their faith, Church teaching, scripture, 
saints, and prayer. Always ground your answers in Catholic tradition and teaching. 
Be warm, clear, and pastoral in tone. When relevant, cite the Catechism of the 
Catholic Church or scripture. Always remind users to consult their priest for 
matters of conscience or spiritual direction."""

print("Welcome to Fides - Your Catholic AI Companion")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    response = ollama.chat(
        model="gemma3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    
    print(f"\nFides: {response['message']['content']}\n")