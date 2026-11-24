from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.models import User, UserRole, AIModel, RiskAssessment, Approval, AuditLog, RiskLevel
from app.schemas import RegisterIn, LoginIn, UserOut, TokenOut, ModelIn, ModelOut, AssessmentIn, DecisionIn
from app.security import hash_password, verify_password, make_token
from app.deps import current_user, roles_required

router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}

@router.post("/auth/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(full_name=data.full_name, email=data.email, hashed_password=hash_password(data.password), role=UserRole.ANALYST)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/auth/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(403, "Account inactive")
    return {"access_token": make_token(user.id), "user": user}

@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

def audit(db, actor, action, kind, entity_id, details=""):
    db.add(AuditLog(actor_id=actor, action=action, entity_type=kind, entity_id=entity_id, details=details))

@router.post("/models", response_model=ModelOut, status_code=201)
def create_model(data: ModelIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = AIModel(**data.model_dump(), owner_id=user.id)
    db.add(item); db.flush()
    audit(db, user.id, "model.created", "AIModel", item.id, item.name)
    db.commit(); db.refresh(item)
    return item

@router.get("/models", response_model=list[ModelOut])
def list_models(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return db.query(AIModel).order_by(AIModel.created_at.desc()).all()

@router.get("/models/{model_id}", response_model=ModelOut)
def get_model(model_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(AIModel, model_id)
    if not item: raise HTTPException(404, "Model not found")
    return item

@router.post("/models/{model_id}/assessments")
def create_assessment(model_id: int, data: AssessmentIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    model = db.get(AIModel, model_id)
    if not model: raise HTTPException(404, "Model not found")
    score = data.impact_score * data.likelihood_score
    level = RiskLevel.CRITICAL if score >= 20 else RiskLevel.HIGH if score >= 15 else RiskLevel.MEDIUM if score >= 8 else RiskLevel.LOW
    model.risk_level = level
    item = RiskAssessment(model_id=model_id, assessor_id=user.id, impact_score=data.impact_score,
        likelihood_score=data.likelihood_score, risk_score=score, rationale=data.rationale)
    db.add(item); db.flush()
    audit(db, user.id, "risk.assessment_submitted", "RiskAssessment", item.id, f"Score {score}")
    db.commit(); db.refresh(item)
    return {"id": item.id, "model_id": item.model_id, "risk_score": item.risk_score, "risk_level": level.value, "status": item.status}

@router.get("/assessments")
def list_assessments(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.query(RiskAssessment).order_by(RiskAssessment.created_at.desc()).all()
    return [{"id": r.id, "model_id": r.model_id, "risk_score": r.risk_score, "rationale": r.rationale, "status": r.status, "created_at": r.created_at} for r in rows]

@router.post("/assessments/{assessment_id}/decision")
def decide(assessment_id: int, data: DecisionIn, db: Session = Depends(get_db),
           reviewer: User = Depends(roles_required(UserRole.ADMIN, UserRole.REVIEWER))):
    item = db.get(RiskAssessment, assessment_id)
    if not item: raise HTTPException(404, "Assessment not found")
    if item.assessor_id == reviewer.id: raise HTTPException(403, "Self-approval is not allowed")
    if item.status != "submitted": raise HTTPException(409, "Assessment is no longer pending")
    item.status = data.decision
    db.add(Approval(assessment_id=item.id, reviewer_id=reviewer.id, decision=data.decision, comments=data.comments))
    audit(db, reviewer.id, "risk.decision_recorded", "RiskAssessment", item.id, data.decision)
    db.commit()
    return {"assessment_id": item.id, "status": item.status}

@router.get("/audit-logs")
def audit_logs(db: Session = Depends(get_db), user: User = Depends(roles_required(UserRole.ADMIN, UserRole.AUDITOR))):
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(500).all()
    return [{"id": x.id, "actor_id": x.actor_id, "action": x.action, "entity_type": x.entity_type,
             "entity_id": x.entity_id, "details": x.details, "created_at": x.created_at} for x in rows]
