from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(api_key=my_key_openai)

assistant_id = "asst_9PkxJouK0097L2lrUxSznB2U" #| Python Coding Assistant

#create a new thread
#create a new run
#create a new message
#take the AI response

def start_new_thread():
    thread = client.beta.threads.create()
    thread_id = thread.id

    return thread_id


def add_message_to_thread(thread_id, prompt):
    message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=prompt,
            )


def execute_run_cycle(thread_id):
    run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    # continuously check run status whether to be completed
    while True:
        # retrieve() => get run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        if run.completed_at:
            elapsed = run.completed_at - run.created_at
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            print(f"Run completed in {elapsed}")
            print("-"*100)
            break
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0]

    AI_Response = last_message.content[0].text.value

    return AI_Response