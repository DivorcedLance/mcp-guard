import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, Boolean, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class SecurityLevel(str, Enum):
    PUBLIC = "PUBLIC"
    CONFIDENTIAL = "CONFIDENTIAL"

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String, index=True)
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    security_level: Mapped[SecurityLevel] = mapped_column(SQLAEnum(SecurityLevel), default=SecurityLevel.PUBLIC)
    is_vectorized: Mapped[bool] = mapped_column(Boolean, default=False)
