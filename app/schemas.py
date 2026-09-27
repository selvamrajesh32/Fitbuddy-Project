from pydantic import BaseModel, Field


class UserInput(BaseModel):
    name: str
    user_id: str
    age: int = Field(..., ge=1, le=120)
    weight: float = Field(..., gt=0)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str


class UserAPIResponse(BaseModel):
    user_id: str
    name: str
    workout_plan: dict
    nutrition_tip: str