import streamlit as st
import json
import pandas as pd

from streamlit_chat import message
import os
from pathlib import Path

from llama_index.indices.struct_store import GPTPandasIndex
from llama_index import download_loader
import openai

openai.api_key = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

from fuzzywuzzy import fuzz


# Load environment variables from .env file
import dotenv
dotenv.load_dotenv('.env')

# Specify the path to the JSON file
file_path = "utils/data_map.json"
with open(file_path, "r") as file:
    json_data = json.load(file)

JSONReader = download_loader("JSONReader")
loader = JSONReader()
documents = loader.load_data(Path(file_path))
langchain_documents = [d.to_langchain_format() for d in documents]
llm = OpenAI(temperature=0.9)
qa_chain = load_qa_chain(llm)

database_dir = os.getcwd()+"\\database\\"

@st.cache_data
def fetch_data(url):
    df = pd.read_csv(url)
    df.date = pd.to_datetime(df.date)
    df.set_index('date', inplace=True)
    return df


# Initialization of session_state variables
if 'old_chat_option' not in st.session_state:
    st.session_state['old_chat_option'] = None
if 'selected_chat_option' not in st.session_state:
    st.session_state['selected_chat_option'] = None
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'btn_query' not in st.session_state:
    st.session_state['btn_query'] = None
if 'btn_chat' not in st.session_state:
    st.session_state['btn_chat'] = None

def handle_query_click():
    st.session_state['user_chat_input'] = ""
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state["old_chat_option"] = None
    st.session_state["selected_chat_option"] = None
    st.session_state['btn_chat'] = False
    st.session_state['btn_query'] = True

def handle_chat_click():
    st.session_state['user_chat_input'] = ""
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state["old_chat_option"] = None
    st.session_state["selected_chat_option"] = None
    st.session_state['btn_chat'] = True
    st.session_state['btn_query'] = False

def handle_selectbox_change():
    st.session_state['user_chat_input'] = ""
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state["old_chat_option"] = st.session_state["selected_chat_option"]
    st.session_state["selected_chat_option"] = st.session_state.new_chat_option


# Title
st.title('US Economic research analyst')

# Buttons
#if not st.session_state['btn_query'] and not st.session_state['btn_chat']:
col1, col2 = st.columns(2)
col1.button('Data Query', key="btn_query_", on_click=handle_query_click)
col2.button('Data Chat', key="btn_chat_", on_click=handle_chat_click)

# Query functionality
if st.session_state['btn_query']:
    economic_data_series = [v["series_name"] for v in json_data.values()]
    user_query = st.text_input("What do you want to know about US Economics?", key="user_query")
    if user_query:
        threshold = 50  # Adjust this threshold as per your requirements
        relevant_options = []
        for option in economic_data_series:
            similarity_score = fuzz.token_set_ratio(user_query.lower(), option.lower())
            if similarity_score >= threshold:
                relevant_options.append(option)
        if len(relevant_options) == 0:
            st.write("Sorry, I couldn't find anything relevant. Can you try writing your query with more details or check out Data Chat tab to check for available series.")

        for series_name in relevant_options:
            for key, value in json_data.items():
                if value["series_name"] == series_name:
                    csv_url = database_dir + value["csv_file"]
                    df = fetch_data(csv_url)
                    st.line_chart(data=df, use_container_width=True)
                    df.index = df.index.astype(str)
                    last_40_rows = df.tail(40)
                    last_40_rows_json = last_40_rows.to_json(orient="columns")
                    template = '''
                    Write like an economic research analyst.
                    Try to answer user query: {query} if you can using the given file. If not, skip.
                    Also, Write a commentary about the short-term trend (6 months) and long term-trend(past 3- years) based on the data.
                    Comment about how the index has done in the recent months including the latest print and the print before that month based on the csv files available to you.
                    Also, make a comment about future term as well.
                    The latest data for the series is here {data_given}
                    '''
                    prompt = template.format(query=user_query, data_given =last_40_rows_json )
                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": user_query},
                        ]
                    )
                    st.write(response["choices"][0]["message"]["content"])

# Chat functionality
if st.session_state['btn_chat']:
    economic_data_series = [v["series_name"] for v in json_data.values()]
    economic_data_series.insert(0, '')  # Add an empty string at the beginning
    st.selectbox('Select a data series:', economic_data_series, key="new_chat_option", on_change=handle_selectbox_change)

    if st.session_state.selected_chat_option:
        selected_data = next((value for value in json_data.values() if value["series_name"] == st.session_state['selected_chat_option']), None)

        if selected_data:
            series_name = selected_data["series_name"]
            published_by = selected_data["published_by"]
            units = selected_data["units"]
            demography = selected_data["demography"]
            frequency = selected_data["frequency"]
            geography = selected_data["geography"]
            source = selected_data["source"]
            seasonal_adjustment = selected_data["seasonal_adjustment"]
            csv_file = selected_data["csv_file"]
            csv_url = database_dir + csv_file

            df = fetch_data(csv_url)

            title = f"### {series_name}"
            subtitle = f"**Frequency:** {frequency}, **Units:** {units}"
            footnote = f"*Published by:* {published_by}"

            st.markdown(title)
            st.markdown(subtitle)
            st.markdown(footnote)

            st.line_chart(data=df, use_container_width=True)

            index = GPTPandasIndex(df=df)
            query_engine = index.as_chat_engine()

            st.write("Chat with selected economic data:")

            def generate_response(user_query):
                response = query_engine.chat(user_query)
                return response.response
            
            def get_text():
                return st.text_input("You: ", key="user_chat_input")
            
            user_input = get_text()

            if user_input:
                output = generate_response(user_input)
                st.session_state.past.append(user_input)
                st.session_state.generated.append(output)
            
            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

