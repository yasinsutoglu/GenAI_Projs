import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import (create_pandas_dataframe_agent,)
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os 
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_anthropic = os.getenv("anthropic_apikey")

# assign llm model func
def pick_llm(model_name):
    if model_name == "GPT-Turbo":
        selected_llm = ChatOpenAI(api_key=my_key_openai, model="gpt-4-turbo-preview",temperature = 0)
    elif model_name == "Claud-3-Opus":
        selected_llm = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-3-opus-20240229", temperature=0)
    elif model_name == "Claud-3-Haiku":
        selected_llm = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-3-haiku-20240307", temperature=0)

    return selected_llm

#summarize data
def summarize_csv(data_file, selected_llm):
    df = pd.read_csv(data_file, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors": "True"})

    data_summary = {}
    data_summary["initial_data_sample"] = df.head()
    data_summary["column_descriptions"] = pandas_agent.run("Make a table with columns from the data. The table should include the names of the columns and a brief explanation in English about the information they contain. Export this as a table.")
    data_summary["missing_values"] = pandas_agent.run("Is there any missing data in this dataset? If so, how many are there? Answer with 'There is missing data in X number of cells in this dataset.'")
    data_summary["duplicate_values"] = pandas_agent.run("Is there duplicate data in this dataset? If so, how many are there? Give your answer as 'There is duplicate data in X number of cells in this dataset.'")
    data_summary["essential_metrics"] = df.describe()

    return data_summary

def get_dataframe(data_file):
    df = pd.read_csv(data_file, low_memory=False)
    return df

def analyze_trend(data_file, variable_of_interest, selected_llm):
    df = pd.read_csv(data_file, low_memory=False)
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors": "True"})
    trend_response = pandas_agent.run(f"Briefly comment on the change trend of the following variable in the data set: {variable_of_interest} Don't refuse to interpret. Since the lines in the data are date-based from past to present, you can make comments by looking at the lines in the data. Give your answer in English.")

    return trend_response

def ask_question(data_file, question, selected_llm):
    df = pd.read_csv(data_file, low_memory=False)
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors": "True"})
    AI_Response = pandas_agent.run(f"{question} Give your answer in English.")

    return AI_Response
