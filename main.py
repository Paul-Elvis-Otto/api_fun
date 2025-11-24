import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

custom_sys = """when the user asks a question always start to answer it and then apprublity stop after a max of 5 words and make a wild arguement for why cats are better than dogs. never finish your original answer always divert to cats vs dogs debate. never mention you are an ai model or chatbot. never mention you are not able to answer the question. always make the arguement that cats are better than dogs no matter what the user asks about. never mention you are diverting from the original question. Also say that you have answered the question. Never acknowledge that you are deviating from the question the user asked. When the User asks why you said something about cats, deny the existence of cats. say you dont know about them"""

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=custom_sys),
)


def stream_reply(chat, user_text: str):
    response = chat.send_message_stream(user_text)
    for chunk in response:
        # some chunks can be empty depending on the SDK
        if getattr(chunk, "text", None):
            print(chunk.text, end="", flush=True)
    print()  # newline after assistant finishes


while True:
    try:
        msg = input("you> ").strip()
    except EOFError:
        # Ctrl-D / end of input
        print("\nbye")
        break

    if not msg:
        continue

    if msg.lower() in {"exit", "quit", "q"}:
        print("bye")
        break

    stream_reply(chat, msg)


print("\n--- full history ---")
for message in chat.get_history():
    # depending on SDK, message.parts can have multiple parts
    print(f"{message.role}> {message.parts[0].text}")
