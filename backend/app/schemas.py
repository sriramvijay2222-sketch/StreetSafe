from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

Category = Literal["open drain", "flooding", "exposed electrical wire", "broken streetlight", "unsafe crossing", "other"]
Severity = Literal["low", "medium", "high"]
Status = Literal["submitted", "under review", "in progress", "resolved", "rejected"]

class ReportCreate(BaseModel):
    category: Category
    title: str = Field(min_length=3, max_length=140)
    description: str = Field(min_length=5, max_length=3000)
    severity: Severity
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    @field_validator("title", "description")
    @classmethod
    def non_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value

class StatusUpdate(BaseModel):
    status: Status
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("note")
    @classmethod
    def clean_note(cls, value: str | None) -> str | None:
        return value.strip() if value else None

class HistoryOut(BaseModel):
    previous_status: str
    new_status: str
    note: str | None
    changed_at: datetime
    model_config = {"from_attributes": True}

class DuplicateOut(BaseModel):
    incident_id: str
    category: str
    latitude: float
    longitude: float
    status: str

class ReportOut(BaseModel):
    incident_id: str
    category: str
    title: str
    description: str
    severity: str
    priority_score: int
    priority_label: str
    category_weight: int
    severity_points: int
    latitude: float
    longitude: float
    status: str
    is_demo: bool
    created_at: datetime
    possible_duplicate_ids: list[str] = []
    possible_duplicates: list[DuplicateOut] = []

class StatsOut(BaseModel):
    total: int
    open: int
    high_priority: int
    resolved: int
