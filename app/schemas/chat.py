from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    
class ChatResponse(BaseModel):
    response: str
    security_check_passed: bool
