from pydantic import BaseModel
from typing import List

class DailyPlan(BaseModel):
    day: str
    diet: str
    exercise: str
    rest: str
    nutrition_tip: str
    destress_activity: str
    social_association: str

class WellnessPlan(BaseModel):
    highLevelStrategy: str
    weekPlan: List[DailyPlan]
