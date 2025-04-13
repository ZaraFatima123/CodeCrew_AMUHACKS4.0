import gradio as gr
import os
import warnings
from datetime import datetime, timedelta
from typing import List, Optional
from dotenv import load_dotenv
import tempfile
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA

# Load environment variables
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings('ignore')

# ========== Shared Utility Functions ==========

def load_pdf(file_path: str) -> List[Document]:
    """Load PDF documents with error handling"""
    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []

def split_documents(documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 100) -> List[Document]:
    """Split documents into chunks for processing"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)

def clean_text(text: str, max_length: int = 50) -> str:
    """Clean and truncate text for display"""
    text = ' '.join(text.split())
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

# ========== PDF Q&A System ==========

class PDFProcessor:
    """Handles PDF processing and question answering"""
    
    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.processed_files = []

    def process_pdfs(self, pdf_files) -> str:
        """Process uploaded PDF files"""
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
            self.vector_store = self._create_vector_store(split_docs)
        else:
            self._add_to_vector_store(split_docs)

        if not self.vector_store:
            return "Failed to create vector store"

        self.qa_chain = self._create_qa_chain()
        if not self.qa_chain:
            return "Failed to create QA chain"

        self.processed_files.extend(new_files)
        return f"Processed {len(new_files)} PDF(s). Total files: {len(self.processed_files)}"

    def query_pdfs(self, query):
        """Answer questions based on processed PDFs"""
        if not self.qa_chain:
            return "Please upload and process PDFs first", []

        try:
            response = self.qa_chain.invoke({"query": query})
            sources = []
            for doc in response['source_documents']:
                sources.append(f"📄 Page {doc.metadata.get('page', 'N/A')}: {doc.page_content[:200]}...")
            return response['result'], sources
        except Exception as e:
            return f"Error processing query: {e}", []

    def _create_vector_store(self, documents: List[Document]) -> Optional[Chroma]:
        """Create vector store from documents"""
        try:
            embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
            return Chroma.from_documents(documents, embeddings)
        except Exception as e:
            print(f"Error creating vector store: {e}")
            return None

    def _add_to_vector_store(self, documents: List[Document]):
        """Add documents to existing vector store"""
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vector_store.add_documents(documents)

    def _create_qa_chain(self) -> Optional[RetrievalQA]:
        """Create question answering chain"""
        try:
            llm = ChatGroq(
                model="llama3-70b-8192",
                temperature=0,
                max_retries=2
            )
            retriever = self.vector_store.as_retriever(
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

# ========== Study Schedule Generator ==========

def create_csv_file(schedule_data: List[dict]) -> str:
    """Create temporary CSV file with schedule data"""
    df = pd.DataFrame(schedule_data)
    temp_csv = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    df.to_csv(temp_csv.name, index=False)
    return temp_csv.name

def create_pdf_file(schedule_data: List[dict]) -> str:
    """Create temporary PDF file with schedule data"""
    temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    
    margin = 50
    y = height - margin

    c.drawString(margin, y, "Study Schedule")
    y -= 20

    for row in schedule_data:
        line = f"Day {row['Day']}: {row['Date']} | Topic: {row['Study Topic']} | Points: {row['Key Points']} | Hours: {row['Hours']}"
        c.drawString(margin, y, line)
        y -= 15
        if y < margin:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - margin

    c.save()
    return temp_pdf.name

def generate_study_schedule(start_date: str, end_date: str, daily_hours: int, syllabus_pdf: gr.File) -> dict:
    """Generate study schedule from syllabus PDF"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        total_days = (end - start).days + 1

        documents = load_pdf(syllabus_pdf.name)
        if not documents:
            return {"schedule": "Error: Failed to load or process the syllabus PDF."}

        split_syllabus = split_documents(documents)
        schedule_data = []

        schedule_md = f"""
# 📅 Study Schedule ({start_date} to {end_date})

**Total Days:** {total_days}  
**Daily Study Hours:** {daily_hours}  
**Total Study Hours:** {total_days * daily_hours}  

## Daily Study Plan

| Day | Date       | Study Topic | Key Points | Hours |
|-----|------------|-------------|------------|-------|
"""
        current_date = start
        for i in range(total_days):
            content = split_syllabus[i % len(split_syllabus)].page_content
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            topic = clean_text(lines[0]) if lines else "No content"
            key_points = clean_text(' • '.join(lines[1:3])) if len(lines) > 1 else "Review materials"

            schedule_md += f"| {i+1} | {current_date.strftime('%Y-%m-%d')} | {topic} | {key_points} | {daily_hours} |\n"
            schedule_data.append({
                "Day": i+1,
                "Date": current_date.strftime('%Y-%m-%d'),
                "Study Topic": topic,
                "Key Points": key_points,
                "Hours": daily_hours
            })
            current_date += timedelta(days=1)

        # Generate files
        csv_file = create_csv_file(schedule_data)
        pdf_file = create_pdf_file(schedule_data)

        return {
            "schedule": schedule_md,
            "csv": csv_file,
            "pdf": pdf_file
        }

    except Exception as e:
        return {"schedule": f"Error: {str(e)}"}

# ========== Gradio Interface ==========

def create_combined_interface():
    """Create the combined Gradio interface"""
    pdf_processor = PDFProcessor()

    with gr.Blocks(title="AI Study Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎓 AI Study Assistant")
        gr.Markdown("Upload your study materials and get help with PDF analysis and schedule planning")

        with gr.Tab("📚 PDF Q&A"):
            with gr.Row():
                with gr.Column():
                    pdf_input = gr.File(
                        file_count="multiple",
                        file_types=['.pdf'],
                        label="Upload PDF Files"
                    )
                    process_btn = gr.Button("🚀 Process PDFs", variant="primary")
                    status_output = gr.Textbox(label="Processing Status", interactive=False)
                
                with gr.Column():
                    query_input = gr.Textbox(label="Ask a Question", placeholder="What would you like to know from your documents?")
                    submit_btn = gr.Button("🔍 Submit Query", variant="primary")
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

        with gr.Tab("📅 Study Schedule"):
            with gr.Row():
                with gr.Column():
                    start_date_input = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="2024-04-15")
                    end_date_input = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="2024-06-01")
                    daily_hours_input = gr.Number(label="Daily Study Hours", value=2, minimum=1, maximum=12)
                    syllabus_input = gr.File(label="Upload Syllabus PDF", file_types=[".pdf"], file_count="single")
                    generate_btn = gr.Button("Generate Schedule", variant="primary")
                
                with gr.Column():
                    schedule_output = gr.Markdown("Your generated schedule will appear here.")
                    with gr.Row():
                        csv_output = gr.File(label="Download CSV", visible=False)
                        pdf_output = gr.File(label="Download PDF", visible=False)

            def update_outputs(start_date, end_date, daily_hours, syllabus_pdf):
                result = generate_study_schedule(start_date, end_date, daily_hours, syllabus_pdf)
                if "csv" in result and "pdf" in result:
                    return {
                        schedule_output: result["schedule"],
                        csv_output: gr.update(value=result["csv"], visible=True),
                        pdf_output: gr.update(value=result["pdf"], visible=True)
                    }
                else:
                    return {
                        schedule_output: result["schedule"],
                        csv_output: gr.update(visible=False),
                        pdf_output: gr.update(visible=False)
                    }

            generate_btn.click(
                fn=update_outputs,
                inputs=[start_date_input, end_date_input, daily_hours_input, syllabus_input],
                outputs=[schedule_output, csv_output, pdf_output]
            )

    return demo

# ========== Main Execution ==========

def main():
    demo = create_combined_interface()
    demo.launch(share=True)

if __name__ == "__main__":
    main()
