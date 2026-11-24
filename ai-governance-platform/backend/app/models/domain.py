from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class LifecycleStatus(str, enum.Enum):
    DEVELOPMENT = "development"
    VALIDATION = "validation"
    APPROVED = "approved"
    MONITORING = "monitoring"
    RETIRED = "retired"

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AIModel(Base):
    __tablename__ = "ai_models"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(60), nullable=False)
    use_case: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(String(120), default="Not specified")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lifecycle_status: Mapped[LifecycleStatus] = mapped_column(Enum(LifecycleStatus), default=LifecycleStatus.DEVELOPMENT)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("ai_models.id"), nullable=False, index=True)
    assessor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    impact_score: Mapped[int] = mapped_column(Integer, nullable=False)
    likelihood_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="submitted")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("risk_assessments.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[str] = mapped_column(String(30), default="pending")
    comments: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
