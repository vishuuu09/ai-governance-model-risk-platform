from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ModelIn(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    version: str = Field(min_length=1, max_length=60)
    use_case: str = Field(min_length=10)
    provider: str = Field(default="Not specified", max_length=120)

class ModelOut(BaseModel):
    id: int
    name: str
    version: str
    use_case: str
    provider: str
    owner_id: int
    lifecycle_status: str
    risk_level: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AssessmentIn(BaseModel):
    impact_score: int = Field(ge=1, le=5)
    likelihood_score: int = Field(ge=1, le=5)
    rationale: str = Field(min_length=15, max_length=5000)

class DecisionIn(BaseModel):
    decision: str = Field(pattern="^(approved|rejected|needs_changes)$")
    comments: str = Field(default="", max_length=3000)
