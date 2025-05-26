import openai
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

def generate_ts_from_abap(abap_code: str) -> str:
    prompt_template = ChatPromptTemplate.from_template("""
You are a SAP ABAP technical architect. Analyze the ABAP code below and write a technical specification (TS) document for it.

ABAP Code:
{abap_code}

Technical Specification:
""")

    prompt = prompt_template.format_messages(abap_code=abap_code)

    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    response = llm(prompt)

    return response.content

