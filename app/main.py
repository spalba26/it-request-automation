from typing import Literal
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db, insert_software_incident
from pydantic import BaseModel, Field, field_validator
from app.services import calculate_priority

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class SoftwareIncidentCreate(BaseModel):
    requester_id: str = Field(min_length=1)
    resource: str = Field(min_length=1)
    description: str = Field(min_length=1)
    impact: Literal["low", "medium", "high"]
    urgency: Literal["low", "medium", "high"]

    @field_validator("requester_id")
    @classmethod
    def validate_requester_id(cls, value: str):
        if not value.strip():
            raise ValueError("Requester cannot be empty or whitespace")
        return value.strip()
    
    @field_validator("resource")
    @classmethod
    def validate_resource(cls, value: str):
        if not value.strip():
            raise ValueError("Resource cannot be empty or whitespace")
        return value.strip()
    
    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str):
        if not value.strip():
            raise ValueError("Description cannot be empty or whitespace")
        return value.strip()
    
@app.post("/software-incidents", status_code=201)
def create_software_incident(s_incident: SoftwareIncidentCreate):
    priority = calculate_priority(s_incident.impact, s_incident.urgency)
    incident_data = s_incident.model_dump()
    incident_data["priority"] = priority
    incident_data["request_type"] = "software_incident"
    incident_data["assigned_team"] = "IT Support"
    incident_data["status"] = "pending"
    request_id = insert_software_incident(incident_data)
    incident_data["id"] = request_id
    return incident_data 