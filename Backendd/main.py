import gradio as gr
import os
import warnings
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings('ignore')


def load_pdf(file_path: str) -> List[Document]:
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []


def split_documents(documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 100) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)


def create_vector_store(documents: List[Document], embedding_model: str = 'sentence-transformers/all-MiniLM-L6-v2'):
    try:
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        return Chroma.from_documents(documents, embeddings)
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None


def create_qa_chain(vector_store):
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2
        )
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        return None


class PDFProcessor:
    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.processed_files = []

    def process_pdfs(self, pdf_files) -> str:
        # Convert to file paths
        pdf_paths = [file.name for file in pdf_files if hasattr(file, 'name')]

        new_files = [f for f in pdf_paths if f not in self.processed_files]
        if not new_files:
            return "No new PDFs to process."

        all_documents = []
        for pdf_file in new_files:
            documents = load_pdf(pdf_file)
            if not documents:
                return f"Failed to load PDF: {pdf_file}"
            all_documents.extend(documents)

        split_docs = split_documents(all_documents)

        if self.vector_store is None:
            self.vector_store = create_vector_store(split_docs)
        else:
            embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
            self.vector_store.add_documents(split_docs)

        if not self.vector_store:
            return "Failed to create vector store"

        self.qa_chain = create_qa_chain(self.vector_store)
        if not self.qa_chain:
            return "Failed to create QA chain"

        self.processed_files.extend(new_files)
        return f"Successfully processed {len(new_files)} PDF(s). Total processed files: {len(self.processed_files)}"

    def query_pdfs(self, query):
        if not self.qa_chain:
            return "Please upload and process PDFs first", []

        try:
            response = self.qa_chain.invoke({"query": query})
            sources = []
            for doc in response['source_documents']:
                sources.append(f"Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:500]}...")
            return response['result'], sources
        except Exception as e:
            return f"Error processing query: {e}", []


def create_gradio_interface():
    pdf_processor = PDFProcessor()

    with gr.Blocks(title="PDF Question Answering") as demo:
        gr.Markdown("# 📄 PDF Question Answering System")

        with gr.Row():
            pdf_input = gr.File(
                file_count="multiple",
                file_types=['.pdf'],
                label="Upload PDF Files"
            )

        with gr.Row():
            process_btn = gr.Button("🚀 Process PDFs")
            status_output = gr.Textbox(label="Processing Status", interactive=False)

        with gr.Row():
            query_input = gr.Textbox(label="Ask a Question")
            submit_btn = gr.Button("🔍 Submit Query")

        answer_output = gr.Textbox(label="Answer", interactive=False)
        sources_output = gr.Textbox(label="Source Documents", interactive=False, lines=5)

        process_btn.click(
            fn=pdf_processor.process_pdfs,
            inputs=[pdf_input],
            outputs=[status_output]
        )

        submit_btn.click(
            fn=pdf_processor.query_pdfs,
            inputs=[query_input],
            outputs=[answer_output, sources_output]
        )

    return demo


def main():
    demo = create_gradio_interface()
    demo.launch(share=False)


if __name__ == "__main__":
    main()
