from typing import List
from pydantic import BaseModel


class SkillBase(BaseModel):
    skill_name: str
    level: str
    months: int


class Skill(SkillBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    external_id: str


class User(UserBase):
    id: int
    skills: List[Skill] = []

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    external_id: str


class Project(ProjectBase):
    id: int
    skills: List[Skill] = []

    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    user_id: str
    project_id: str
    rating: float


class Interaction(InteractionBase):
    id: int

    class Config:
        from_attributes = True
