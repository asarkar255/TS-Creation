import openai
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

def generate_ts_from_abap(abap_code: str) -> str:
    prompt_template = ChatPromptTemplate.from_template("""
You are a Technical Architect specializing in SAP ABAP. When generating a Technical Specification (TS) for ABAP code, ensure the following structure is followed:
- Formatting shoud be docx compatible.
- Remember Titles should be Bold and in uppercase .
- Provide Numbering and sub-numbering for each section.
- Title and Header should be in Blue color.
- TSD hsould be minimum 1000 words.( thi is is a must)                        
1. Title – Short description of the program/report.
2. Objective – What the ABAP program is supposed to do.
3. Functional Description – Functional logic, input/output behavior, expected flow should be descriptive.
4. Technical Design:
    - Report Type (Executable, Module Pool, etc.)
    - Selection screen elements
    - Events used (START-OF-SELECTION, AT SELECTION-SCREEN, etc.)
    - Internal tables, work areas, global variables
    - Forms and Subroutines
    - Local/Global Classes and Methods
    - Interfaces and Function Modules used
5. Database Tables Used – List with descriptions of each table accessed.
6. Performance Considerations – Use of indexes, buffering, FOR ALL ENTRIES, etc.
7. Error Handling – TRY-CATCH blocks, SY-SUBRC checks, Message handling.
8. Assumptions and Dependencies – Any preconditions or external system dependencies.
9. Testing Strategy – Functional tests, unit tests, and sample test cases.
10. Screenshots or Outputs (if applicable)
11. Development Objects Created – A table with proper bordering and headings:
    - Object Name (e.g., ZMY_REPORT, ZMY_TABLE)
    - Object Type (e.g., Report, Table, View, Function Module, Class, etc.)
12. Flowchart – Provide a simple textual or visual representation (diagram) showing the main flow of logic in the ABAP program.
    Format: It should be an actual image 

ABAP Code:
{abap_code}

Technical Specification:
""")

    prompt = prompt_template.format_messages(abap_code=abap_code)

    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    response = llm.invoke(prompt)

    return response.content

