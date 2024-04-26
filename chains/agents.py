from typing import Optional

import os
import re
import streamlit as st
from langchain.agents import initialize_agent, AgentType

from langchain.chains import LLMChain
from langchain.chains.llm_math.base import LLMMathChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import Tool
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAI
from langchain.schema.output_parser import StrOutputParser
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap

from chains.templates import system_coupon_prompt, coupon_template
from chains.utils import escape_dollar_signs


def get_question(input):
    if not input:
        return None
    elif isinstance(input, str):
        return input
    elif isinstance(input, dict) and 'question' in input:
        return input['question']
    elif isinstance(input, BaseMessage):
        return input.content
    else:
        raise Exception("string or dict with 'question' key expected as RAG chain input.")


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += escape_dollar_signs(token)
        self.container.write(self.text)


class ChainAgent:
    def __init__(self, model_name="gemini", stream_handler=None):
        match model_name:
            case "gemini":
                self.llm = ChatGoogleGenerativeAI(
                    google_api_key=os.getenv('GOOGLE_API_KEY'),
                    model='gemini-pro',
                    temperature=0,
                    max_tokens=16384)
                    # streaming=True,
                    # callbacks=[stream_handler] if stream_handler else None)
            case _:
                raise Exception("unknown model name: " + model_name)

    def chain_shopmate(self, msgs, retriever):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", coupon_template),
                ("placeholder", "{chat_history}"),  # same as `MessagesPlaceholder(variable_name="chat_history")`
                ("human", "{question}"),
            ]
        )
        chain = (
            RunnableParallel({
                "context": RunnableLambda(get_question) | retriever,
                "question": RunnablePassthrough(),
            })
            | prompt
            | self.llm
        )
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: msgs,
            input_messages_key="question",
            history_messages_key="chat_history",
        )
        return chain_with_history

    def chain_shopmate_with_tools(self, retriever, question):
        math_chain = LLMMathChain.from_llm(llm=self.llm)
        math_tool = Tool.from_function(
            name="Calculator",
            func=math_chain.run,
            description="""
                Useful for when you need calculations about the cost or price among items. 
                This tool is only for math questions and nothing else. Only input math expressions.
            """
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": system_coupon_prompt,
            },
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        agent = initialize_agent(
            tools=[math_tool, qa_chain],
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            handle_parsing_errors=True
        )

        return agent
