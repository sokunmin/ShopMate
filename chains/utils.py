import re

from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory


def escape_dollar_signs(text):
    return re.sub(r'\$', r'\\$', text)


def create_chain(llm, prompt, input_key, output_key) -> LLMChain:
    memory = ConversationBufferMemory(
        input_key=input_key, memory_key="chat_history"
    )
    return LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        output_key=output_key,
        memory=memory,
    )
