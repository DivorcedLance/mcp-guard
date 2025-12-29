from fastapi import FastAPI
from app.api.v1.endpoints import chat, documents
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Secure RAG Knowledge Base Manager implementing MCP principles."
)

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])

@app.get("/")
async def root():
    return {"message": "MCP-Guard System is Online", "university": "UNMSM"}

# DB Initialization placeholder (normally done via Alembic)
# from app.db.base import Base
# from app.db.session import engine
# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
