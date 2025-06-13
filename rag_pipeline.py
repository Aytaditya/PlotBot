import os
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import chromadb
from uuid import uuid4

load_dotenv()

llm = AzureChatOpenAI(
    openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
    openai_api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-4.1",
    temperature=0,
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-large",
    openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
    openai_api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    chunk_size=1000
)

params = {
    "num": 5,
    "gl": "us",
    "hl": "en",
    "engine": "google",
    "device": "desktop",
    "google_domain": "google.com"
}

search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERP_API_KEY"), params=params)


extraction_prompt = ChatPromptTemplate.from_template("""
You are an expert analyst assistant.

Extract the core business query topic from the user's question. Your answer should be short and precise, combining the company/product name and the business intent.

Examples:
- Question: "Is OpenAI profitable yet?" → Answer: "OpenAI profitability"
- Question: "What are the growth plans of SpaceX?" → Answer: "SpaceX future plans"
- Question: "How is Google's AI division performing?" → Answer: "Google AI performance"
- Question: "What is Apple's next product launch?" → Answer: "Apple product roadmap"

Now, analyze and extract the main topic:

Question: "{question}"

Return only the business query topic.
""")

def extract_topic(question: str) -> str:
    chain = extraction_prompt | llm
    return chain.invoke({"question": question}).content.strip()

def search_top_link(topic: str) -> str:
    query = f"{topic} site:techcrunch.com OR site:bloomberg.com OR site:businessinsider.com OR site:wikipedia.org"
    results = search.results(query)
    organic_results = results.get("organic_results", [])
    return organic_results[0].get("link", None) if organic_results else None

def load_content_from_url(url: str) -> str:
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content if docs else "No content loaded."

def create_vectorstore(content: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(content)
    documents = [Document(page_content=t, metadata={"source": "web"}) for t in texts]
    uuids = [str(uuid4()) for _ in documents]

    client = chromadb.PersistentClient(path="./chroma_store")
    vectorstore = Chroma(
        client=client,
        collection_name="wikipedia_rag",
        embedding_function=embeddings
    )
    vectorstore.add_documents(documents=documents, ids=uuids)
    return vectorstore

def run_rag(question: str) -> str:
    topic = extract_topic(question)
    url = search_top_link(topic)

    if not url:
        return "No relevant page found."

    content = load_content_from_url(url)
    vectorstore = create_vectorstore(content)
    retriever = vectorstore.as_retriever()

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a business analyst.

        Use the following context to answer the question clearly and concisely:

        Context:
        {context}

        Question: {question}

        If the user asks something outside business, respond with:
        I'm only able to answer questions related to the business as I am a business analyst.

        if someone ask you your name, respond with:
        My name is Benny the business analyst.

        Answer:
        
        ALWAYS RETURN ANSWER IN MARKDOWN FORMAT.
        """  
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=False
    )

    return qa_chain.run(question)
