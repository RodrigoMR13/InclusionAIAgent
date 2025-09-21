import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

class ChromaDBService():
    PASTA_BASE: str
    def __init__(self, pasta_base: str = None):
        load_dotenv(r"C:\Users\Public\repos\Estudos\Faculdade\projeto_aplicado_3\env")
        self.PASTA_BASE = pasta_base

    # Função principal para criar o banco de dados
    def create_db(self):
        docs = self.load_docs()
        chunks = self.chunk_docs(docs)
        self.vectorize_chunks(chunks)


    # Carrega os documentos da pasta especificada
    def load_docs(self):
        loader = PyPDFDirectoryLoader(self.PASTA_BASE, glob="*.pdf")
        return loader.load()


    # Divide os documentos em chunks menores (pedaços de texto)
    def chunk_docs(docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=250,
            length_function=len,
            add_start_index=True
        )
        return text_splitter.split_documents(docs)


    # Vetoriza os chunks com o processo de embedding
    def vectorize_chunks(chunks):
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        db = Chroma(persist_directory="db", embedding_function=embeddings)
        for i, chunk in enumerate(chunks):
            db.add_documents([chunk])
            if i % 5 == 0:
                time.sleep(2)
        print(f"Persisted {len(chunks)} chunks.")