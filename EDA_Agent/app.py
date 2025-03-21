import streamlit as st
import datahelper # custom module

if "dataload" not in st.session_state:
    st.session_state.dataload = False

# callback function to be used for caching
def activate_dataload():
    st.session_state.dataload = True

st.set_page_config(page_title="Data Explorer 🤖", layout="wide")
st.image(image="./img/app_banner.jpg", use_column_width=True)
st.title("Data Explorer🤖")
st.divider()

# -----------Sidebar----------------------
st.sidebar.subheader("Upload File")
st.sidebar.divider()

selected_llm = st.sidebar.radio(label="Pick Your LLM!", options=["GPT-Turbo", "Claud-3-Opus", "Claud-3-Haiku"])

loaded_file = st.sidebar.file_uploader("Choose CSV File To Upload", type="csv")

load_data_btn = st.sidebar.button(label="Upload", on_click=activate_dataload, use_container_width=True)

# --------------------Explatory Data Analysis Screen-----------------------------
col_prework, col_dummy, col_interaction = st.columns([4,1,7])

if st.session_state.dataload:
    @st.cache_data # built-in streamlit func decorator for caching
    def summarize():
        loaded_file.seek(0) # ensuring the loader start from beginning
        data_summary = datahelper.summarize_csv(data_file=loaded_file, selected_llm=selected_llm)
        return data_summary
    
    data_summary = summarize()

    with col_prework:
        st.info("DATASET SUMMARY")
        st.subheader("Sample Part of Your DataSet:")
        st.write(data_summary["initial_data_sample"])
        st.divider()
        st.subheader("Column Descriptions:")
        st.write(data_summary["column_descriptions"])
        st.divider()
        st.subheader("Missing/Lost Data Status:")
        st.write(data_summary["missing_values"])
        st.divider()
        st.subheader("Duplicated Data Status:")
        st.write(data_summary["duplicate_values"])
        st.divider()
        st.subheader("Essential Metrics")
        st.write(data_summary["essential_metrics"])
    
    with col_dummy:
        st.empty()
    # ---------------------------
    with col_interaction:
        st.info("INTERACTION WITH DATASET")
        variable_of_interest = st.text_input(label="Which Variable Will You Examine?")
        examine_btn = st.button(label="EXAMINE")
        st.divider()
        @st.cache_data
        def explore_variable(data_file, variable_of_interest):
            data_file.seek(0)
            dataframe = datahelper.get_dataframe(data_file=data_file)
            st.bar_chart(data=dataframe, y=[variable_of_interest])
            st.divider()
            # --------------------
            data_file.seek(0)
            trend_response = datahelper.analyze_trend(data_file=loaded_file, variable_of_interest=variable_of_interest, selected_llm=selected_llm)
            st.success(trend_response)
            return

        if variable_of_interest or examine_btn:
            explore_variable(data_file=loaded_file, variable_of_interest=variable_of_interest)
    # ---------------------------

        free_question = st.text_input(label="What Do You Wish To Know About The DataSet?")
        ask_btn = st.button(label="ASK")
        st.divider()
        @st.cache_data
        def answer_question(data_file, question):
            data_file.seek(0)
            AI_Response = datahelper.ask_question(data_file=loaded_file, question=question, selected_llm=selected_llm)
            st.success(AI_Response)
            return
        
        if free_question or ask_btn:
            answer_question(data_file=loaded_file, question=free_question)







