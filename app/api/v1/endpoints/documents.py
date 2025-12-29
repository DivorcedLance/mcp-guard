# Placeholder para subida de archivos y endpoints relacionados a documentos.
# Implementar lógica de subida y vectorización aquí en el futuro.
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion_service import ingestion_service

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Sube un PDF, lo vectoriza y lo guarda en la Base de Conocimiento (Pinecone).
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    
    try:
        result = await ingestion_service.process_pdf(file)
        return {"message": "Documento procesado correctamente", "details": result}
    except Exception as e:
        print(f"Error en ingesta: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando el documento: {str(e)}")