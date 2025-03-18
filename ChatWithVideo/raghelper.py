from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")

llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

embeddings = OpenAIEmbeddings(api_key=my_key_openai)

#1- Chat with LangModel
def ask_gemini(prompt):
    AI_Response = llm_gemini.invoke(prompt)
    return AI_Response.content

#2- RAG Process by video transcript textures
def rag_with_video_transcript(transcript_docs, prompt):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    splitted_documents = text_splitter.split_documents(transcript_docs)
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    retriever = vectorstore.as_retriever()
    relevant_documents = retriever.get_relevant_documents(prompt)

    context_data = ""

    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    final_prompt = f"""I have a question: {prompt}
    To answer this question we have the following information: {context_data} .
    Just use the available information I have given you here to answer this question. Never go beyond these.
    """

    AI_Response = ask_gemini(final_prompt)

    return AI_Response, relevant_documents