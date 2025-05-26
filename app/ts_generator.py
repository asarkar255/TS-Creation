import openai
import os


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

def generate_ts_from_abap(abap_code: str) -> str:
    prompt = f"""
You are a SAP ABAP technical architect. Analyze the ABAP code below and write a technical specification (TS) document for it.

ABAP Code:
{abap_code}

Technical Specification:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in SAP ABAP documentation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response['choices'][0]['message']['content']
