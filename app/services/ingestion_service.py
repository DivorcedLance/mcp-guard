import os
import shutil
import time  # <--- IMPORTANTE PARA EL RETRASO
from pathlib import Path
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone

from app.core.config import settings

class IngestionService:
    def __init__(self):
        # Usamos el modelo más nuevo, suele tener mejor manejo de quota
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",  # <--- ACTUALIZADO
            google_api_key=settings.GOOGLE_API_KEY,
            task_type="retrieval_document"
        )
        
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = "mcp-guard-index"

    async def process_pdf(self, file: UploadFile) -> dict:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        try:
            # 1. Cargar
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()
            
            # 2. Dividir (Chunks)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            total_chunks = len(chunks)
            print(f"📄 Documento dividido en {total_chunks} fragmentos. Iniciando carga lenta...")

            # 3. PROCESAMIENTO POR LOTES (THROTTLING)
            # Para evitar el error 429, enviamos de 5 en 5 y esperamos.
            batch_size = 5
            sleep_time = 3  # Segundos de espera entre lotes
            
            for i in range(0, total_chunks, batch_size):
                batch = chunks[i : i + batch_size]
                
                # Subir lote actual
                PineconeLangChain.from_documents(
                    documents=batch,
                    embedding=self.embeddings,
                    index_name=self.index_name
                )
                
                print(f"✅ Procesado lote {i} a {min(i + batch_size, total_chunks)} de {total_chunks}")
                
                # Descansar para respetar la cuota gratuita (si no es el último lote)
                if i + batch_size < total_chunks:
                    time.sleep(sleep_time)

            return {
                "filename": file.filename,
                "chunks_processed": total_chunks,
                "status": "success",
                "mode": "slow_ingestion_for_free_tier"
            }
            
        finally:
            if file_path.exists():
                os.remove(file_path)

ingestion_service = IngestionService()