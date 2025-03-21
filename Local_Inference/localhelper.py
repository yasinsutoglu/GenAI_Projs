from openai import OpenAI

#ollama generation
def generate_with_ollama(model_name="mistral", chat_history=[], temperature=0):
    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key="ollama"
    )

    AI_Response = client.chat.completions.create(
        model=model_name,
        messages=chat_history,
        temperature=temperature
    )

    return AI_Response.choices[0].message.content


#lm studio generation
def generate_with_lmstudio(chat_history=[], temperature=0):
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

    AI_Response = client.chat.completions.create(
        model="",
        messages=chat_history,
        temperature=temperature
    )

    return AI_Response.choices[0].message.content

