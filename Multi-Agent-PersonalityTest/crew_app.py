from crewai import Crew, Process # Crew => Agent group; Process => Agent group job style
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import crewhelper # custom module
import os

# implicit api-key usage
os.environ["OPENAI_API_KEY"] = os.getenv("openai_apikey")
os.environ["GOOGLE_API_KEY"] = os.getenv("google_apikey")

# LLM MODELS GENERATION
llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
llm_gpt = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)

# General usable instructions as prompt
instructions=f"""Develop a personality test to use to determine the characteristics of people in professional life.
When developing this test, act in accordance with the well-known and widely accepted approaches of the Big Five, 
16 Personalities or 4 Colors approach. The personality test you developed should include personality types 
and the character traits of each of them.You should write questions to test each personality type and character. 
Depending on the answers to these questions, you should decide on a method on how to connect the user with a type
and character traits. There should also be short summaries of each personality type to show to people taking this test. 
After preparing the contents of the personality test in accordance with these criteria, you should write a Python Streamlit
application to include all these contents. So users can find out their personality types using this application. 
Take a deep breath and complete these tasks one by one.
"""

# Agents
test_expert = crewhelper.test_expert(llm=llm_gpt)
software_engineer = crewhelper.software_engineer(llm=llm_gpt)
test_consultant = crewhelper.test_consultant(llm=llm_gpt)
# Tasks
test_development_task = crewhelper.create_test_task(instructions=instructions, agent=test_expert)
code_task = crewhelper.create_code_task(instructions=instructions, agent=software_engineer)
test_review_task = crewhelper.create_review_task(instructions=instructions, agent=test_consultant)

# Agent Group
crew = Crew(
    agents = [
        test_expert, 
        software_engineer,
        test_consultant
        ],
    tasks = [
        test_development_task, 
        test_review_task,
        code_task,
        ],
    verbose = True, # Give process report
    process = Process.sequential # tasks shall be processed sequentially as written above
)

result = crew.kickoff() # agents group starts to lead processes

print("*"*100)
print("RESULTS:")
print("*"*100)
print("*"*100)
print(result)