from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatAnthropic
from langchain import hub
from langchain_community.callbacks import StreamlitCallbackHandler # used for accordion chat history ui-part
from langchain_community.tools.tavily_search import TavilySearchResults
import streamlit as st
import os
import customtools
from dotenv import load_dotenv

load_dotenv()

# API-KEYS
my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")
my_key_anthropic = os.getenv("anthropic_apikey")
os.environ["TAVILY_API_KEY"] = os.getenv("tavily_apikey")

# AI LANG MODELS
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")
llm_gpt = ChatOpenAI(api_key=my_key_openai, model="gpt-4-0125-preview", temperature=0, streaming=True)
llm_claude = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-2.1")

# Get Prompt Template As System Prompt
agent_prompt = hub.pull("hwchase17/react")

def configure_agent(selected_llm, selected_search_engine, selected_image_generator, selected_web_scraper):
    if selected_llm == "GPT-4":
        llm = llm_gpt
    elif selected_llm == "Gemini Pro":
        llm = llm_gemini
    elif selected_llm == "Claude 2.1":
        llm = llm_claude

    image_generator_tool = customtools.get_tool(selected_image_generator=selected_image_generator)
    web_scraping_tool = customtools.get_web_tool(selected_web_scraper=selected_web_scraper)
    
    if selected_search_engine == "DuckDuckGo":
        tools = load_tools(["ddg-search"]) # returns List[Tool]
        tools.extend([image_generator_tool, web_scraping_tool])
    elif selected_search_engine == "Tavily":
        tools = [TavilySearchResults(max_results=1), image_generator_tool, web_scraping_tool]

    agent = create_react_agent(llm=llm, tools=tools, prompt=agent_prompt) # AGENT CREATION
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # AGENT RUN CLASS

    return agent_executor

#------------------------------------ST-UI-----------------------------------------
st.set_page_config(page_title="Chat with ReAct Agent")
st.image(image="./img/ai_agent_banner.png")
st.title("Chatting With ReAct Agent")
st.divider()

st.sidebar.header("Agent Configs")
st.sidebar.divider()
selected_llm = st.sidebar.radio(label="Pick LangModel!", options=["GPT-4", "Gemini Pro", "Claude 2.1"])
st.sidebar.divider()
selected_search_engine = st.sidebar.radio(label="Pick Search Engine!", options=["DuckDuckGo", "Tavily"], index=1)
st.sidebar.divider()
selected_image_generator = st.sidebar.radio(label="Pick Img GeneratorModel!", options=["Stable Diffusion XL","DALL-E 3"])
st.sidebar.divider()
selected_web_scraper = st.sidebar.radio(label="Pick WebScraping Tool!", options=["BeautifulSoup", "Selenium"])
st.sidebar.divider()
turkish_sensitivity = st.sidebar.checkbox(label="Force Turkish Answer", value=True)
st.sidebar.divider()
reset_chat_btn = st.sidebar.button(label="Reset Chat History")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(placeholder="Message Entry"):
    st.chat_message("user").write(prompt)

    if turkish_sensitivity:
        st.session_state.messages.append({"role": "user", "content": prompt + "Bu soruyu Türkçe yanıtla"})
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        st.info("🧠 Thought Chain Processing...")

        st_callback = StreamlitCallbackHandler(st.container())

        executor = configure_agent(selected_llm=selected_llm, selected_search_engine=selected_search_engine, selected_image_generator=selected_image_generator, selected_web_scraper=selected_web_scraper)

        AI_Response = executor.invoke(
            {"input": st.session_state.messages}, {"callbacks": [st_callback]},
            handle_parsing_errors=True # parameter to solve the problems as analysing language, context relations and parsing
        )

        st.markdown(AI_Response["output"], unsafe_allow_html=True) # to get clickable link
        st.session_state.messages.append({"role": "assistant", "content": AI_Response["output"]})

if reset_chat_btn:
    st.session_state.messages = []
    st.toast("Chat History Has Been Reseted!")






