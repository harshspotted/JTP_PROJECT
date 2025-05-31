from pydantic import BaseModel, Field
from typing import List, Literal
from pydantic import BaseModel


# Limit skill names to allowed values
SkillName = Literal[
    "Python",
    "AI and Machine learning",
    "Git",
    "MongoDB",
    "SQL",
    "Docker",
    "Excel",
    "Javascript",
    "Cloud Platform",
]

# Limit level values to allowed ones
SkillLevel = Literal["Basic", "CollegeResearch", "Professional", "Other"]


class Skill(BaseModel):
    skill_name: SkillName
    level: SkillLevel
    months: int = Field(default=5, ge=0, description="Number of months of experience")


class RecommendationRequest(BaseModel):
    skills: List[Skill]
    description: str = Field(..., description="Short description of the candidate")
    top_k: int = Field(5, description="How many entries to show")


class RecommendationResponse(BaseModel):
    top_projects: List[int]
    scores: List[float]


class SkillMetadata(BaseModel):
    skill_name: str
    level: str
    months: int


class RecommendationWithMetaDataResult(BaseModel):
    rank: int
    project_id: str
    score: float
    description: str
    required_skills: List[SkillMetadata]


class AnalysisInput(BaseModel):
    employee_skills: List[SkillMetadata]
    employee_description: str

    project_skills: List[SkillMetadata]
    project_description: str

    score: float


class AnalysisOutput(BaseModel):
    fitness_evaluation: str
    recommended_courses: str
