import dotenv
import streamlit as st
import time
import os

from langchain.chains.llm import LLMChain
from langchain.chains.llm_math.base import LLMMathChain
from langchain_core.tools import Tool
from langsmith import Client
from langchain import hub
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig, RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.run_collector import RunCollectorCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_text_splitters import SpacyTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap
import google.generativeai as genai


from chains.agents import StreamHandler, ChainAgent
from chains.loader import NewCSVLoader
from chains.utils import escape_dollar_signs

st.set_page_config(page_title="ShopMate", page_icon="🦜")
st.title("🦜 ShopMate")

dotenv.load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# Customize if needed
client = Client()
ls_tracer = LangChainTracer(project_name=os.environ["LANGCHAIN_PROJECT"], client=client)
run_collector = RunCollectorCallbackHandler()
cfg = RunnableConfig()
cfg["callbacks"] = [ls_tracer, run_collector]
cfg["configurable"] = {"session_id": "any"}

files = ["./data/coupons.csv", "./data/credit_cards.csv", "./data/products.csv"]


# @st.cache_resource
def data_to_embeddings(files, embeddings, topk=6):
    if not os.path.exists("faiss_index"):
        docs = []
        for f in files:
            match f.lower():
                case x if x.endswith(".csv"):
                    loader = NewCSVLoader(f, encoding="utf-8")
                case x if x.endswith(".pdf"):
                    loader = PyPDFLoader(f)
                case _:
                    raise ValueError(f"Unsupported file type: {f}")
            d = loader.load()
            # text_splitter = SpacyTextSplitter(pipeline="en_core_web_sm", chunk_size=100, chunk_overlap=50)
            # d = text_splitter.split_documents(d)
            docs.extend(d)
        vector_store = FAISS.from_documents(docs, embeddings)
        vector_store.save_local("faiss_index")
    else:
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": topk})
    return retriever


# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")

reset_history = st.sidebar.button("Reset Chat History")
if len(msgs.messages) == 0 or reset_history:
    msgs.clear()
    msgs.add_ai_message("Hi, I'm ShopMate. How can I help you today?")
    st.session_state["last_run"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="Hi, I'm ShopMate. How can I help you today?")
    ]

for msg in st.session_state.messages:
    if msg.role == "assistant":
        msg.content = escape_dollar_signs(msg.content)
    st.chat_message(msg.role).write(msg.content)


# If user inputs a new prompt, generate and draw a new response
if user_input := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=user_input))
    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        chat_agent = ChainAgent(model_name='gemini', stream_handler=stream_handler)
        retriever = data_to_embeddings(files, GoogleGenerativeAIEmbeddings(), topk=10)
        chain = chat_agent.chain_shopmate(msgs, retriever)
        response = chain.invoke({"question": user_input}, cfg)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response.content)
        )
    st.session_state.last_run = run_collector.traced_runs[0].id
