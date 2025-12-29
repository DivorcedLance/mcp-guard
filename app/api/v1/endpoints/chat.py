from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.security_guard import security_guard, SecurityException
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Secure Chat Endpoint implementing MCP-Guard Logic.
    """
    
    # STEP 1: Security Layer (The "Guard")
    # This logic comes directly from the thesis requirements to stop attacks early.
    try:
        security_guard.analyze_prompt_safety(request.query)
    except SecurityException as e:
        # Rethrow as HTTP exception to be handled by FastAPI
        raise e

    # STEP 2: RAG Pipeline
    # Only executes if security check passes
    response_text = await rag_service.get_response(request.query)

    return ChatResponse(
        response=response_text,
        security_check_passed=True
    )
