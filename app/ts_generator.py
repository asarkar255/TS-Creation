import openai
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
# Load your RAG knowledge base from a text file
rag_file_path = os.path.join(os.path.dirname(__file__), "rag_knowledge_base.txt")
loader = TextLoader(rag_file_path)
documents = loader.load()

# Split documents for embedding
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Create vector store with OpenAI embeddings and Chroma
embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embedding)

# Create retriever
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4", temperature=0.3),
    chain_type="stuff",
    retriever=retriever,
)
def generate_ts_from_abap(abap_code: str) -> str:
    # Retrieve relevant context from the RAG knowledge base
    retrieved_context = qa_chain.run(abap_code)

    # Combine the retrieved context with the ABAP code for the prompt
    prompt_input = f"{retrieved_context}\n\nABAP Code:\n{abap_code}"

    prompt = ChatPromptTemplate.format_messages(abap_code=prompt_input)

    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    response = llm.invoke(prompt)

    return response.content


