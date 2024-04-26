# Tutorial: https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm/

from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate

model = VertexAI(model_name="gemini-pro")

print("------ [1-1] ------")
message = "What are some of the pros and cons of Python as a programming language?"
response = model.invoke(message)
print(response)

print("------ [1-2] ------")
for chunk in model.stream(message):
    print(chunk, end="", flush=True)

model.batch([message])

result = model.generate([message])
print(result.generations)

print("------ [2] ------")

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | model

question = """
I have five apples. I throw two away. I eat one. How many apples do I have left?
"""
print(chain.invoke({"question": question}))

print("------ [3] ------")
llm = VertexAI(model_name="code-bison", max_output_tokens=1000, temperature=0.3)
question = "Write a python function that checks if a string is a valid email address"
print(model.invoke(question))
