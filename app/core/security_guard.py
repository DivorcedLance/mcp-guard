# ---------------------------------------------------------
# MCP IMPLEMENTATION LAYER
# Logic based on Thesis: "Mitigation of Prompt Injection..."
# Author: José Luis Vergara Pachas
# ---------------------------------------------------------

import re
from fastapi import HTTPException, status

class SecurityException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class SecurityGuard:
    """
    Implements heuristic checks and MCP (Model Context Protocol) validation logic
    to prevent Prompt Injection attacks before they reach the LLM or Vector Store.
    """

    # Common patterns used in Prompt Injection / Jailbreaking
    FORBIDDEN_PATTERNS = [
        r"ignore previous instructions",
        r"system override",
        r"dan mode",
        r"do anything now",
        r"act as an unrestricted",
        r"forget your rules",
        r"you are now",
        r"alpha mode",
        r"god mode"
    ]

    @classmethod
    def analyze_prompt_safety(cls, query: str) -> bool:
        """
        Analyzes the user query for potential security threats.
        
        Args:
            query (str): The raw input from the user.
            
        Returns:
            bool: True if safe, raises SecurityException if unsafe.
        """
        normalized_query = query.lower().strip()

        # 1. Heuristic Pattern Matching
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, normalized_query):
                # Log this security event (In a real app, send to monitoring)
                print(f"[SECURITY ALERT] Prompt Injection detected: {pattern}")
                raise SecurityException(
                    detail=f"Security Protocol Triggered: Potentially unsafe content detected ({pattern}). Request denied."
                )

        # 2. Length Checks (Simple DoS mitigation)
        if len(query) > 5000:
            raise SecurityException(detail="Input exceeds maximum security length.")

        return True

security_guard = SecurityGuard()
