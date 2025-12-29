import time
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from langchain.schema import SystemMessage, HumanMessage
from app.core.config import settings

class RAGService:
    def __init__(self):
        # 1. LLM: Agregamos el flag 'convert_system_message_to_human=True'
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            convert_system_message_to_human=True  # <--- ¡ESTA ES LA LÍNEA QUE FALTABA!
        )
        
        # 2. EMBEDDINGS
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=settings.GOOGLE_API_KEY,
            task_type="retrieval_query"
        )
        
        # 3. Conexión a Pinecone
        self.vector_store = PineconeLangChain.from_existing_index(
            index_name="mcp-guard-index",
            embedding=self.embeddings
        )

    async def get_response(self, query: str) -> str:
        docs = []
        
        # A. RETRIEVAL CON REINTENTOS
        max_retries = 3
        for attempt in range(max_retries):
            try:
                docs = self.vector_store.similarity_search(query, k=3)
                break 
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️ Cuota excedida en Chat. Reintentando... ({attempt+1})")
                    time.sleep(2)
                else:
                    print(f"❌ Error fatal en búsqueda vectorial: {e}")
                    return "Lo siento, el sistema de memoria está saturado. Intenta de nuevo."

        context_text = "\n\n".join([d.page_content for d in docs])
        
        if not context_text:
            context_text = "No se encontró información relevante en los documentos internos."

        # B. PROMPT
        system_instruction = (
            "Eres un asistente seguro de la UNMSM. "
            "Responde a la pregunta basándote EXCLUSIVAMENTE en el siguiente contexto. "
            "Si la respuesta no está en el contexto, di que no tienes esa información."
        )
        
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=f"Contexto Recuperado:\n{context_text}\n\nPregunta: {query}")
        ]

        # C. GENERACIÓN
        response = await self.llm.ainvoke(messages)
        return response.content

rag_service = RAGService()