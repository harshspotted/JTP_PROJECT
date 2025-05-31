from fastapi import APIRouter, HTTPException
from database import get_db
import services.crud as crud_service
from schemas import crud, orm

# Base router
router = APIRouter(
    prefix="/api",
    tags=["CRUD"],
    responses={404: {"description": "Not found"}},
)


# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/",
)  # response_model=crud.User)
def create_user_endpoint(
    user: crud.UserBase,
    skills: List[crud.SkillBase],
    db: Session = Depends(get_db),
):
    if crud_service.get_user(db, external_id=user.external_id):
        raise HTTPException(status_code=400, detail="User already exists")
    return crud_service.create_user(db, user, skills)


@user_router.get(
    "/",
)  # response_model=List[crud.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(orm.User).offset(skip).limit(limit).all()


# routers/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.post(
    "/",
)  # response_model=crud.Project)
def create_project_endpoint(
    project: crud.ProjectBase,
    skills: List[crud.SkillBase],
    db: Session = Depends(get_db),
):
    if crud_service.get_project(db, external_id=project.external_id):
        raise HTTPException(status_code=400, detail="Project already exists")
    return crud_service.create_project(db, project, skills)


@project_router.get(
    "/",
)  # response_model=List[crud.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(orm.Project).offset(skip).limit(limit).all()


# routers/interactions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


interaction_router = APIRouter(prefix="/interactions", tags=["interactions"])


@interaction_router.post(
    "/",
)  # response_model=crud.Interaction)
def create_interaction_endpoint(
    interaction: crud.InteractionBase, db: Session = Depends(get_db)
):
    return crud_service.create_interaction(db, interaction)


@interaction_router.get(
    "/",
)  # response_model=List[crud.Interaction])
def read_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_service.get_interactions(db, skip, limit)


# Attach routes
router.include_router(user_router)
router.include_router(project_router)
router.include_router(interaction_router)
