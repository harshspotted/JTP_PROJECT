from sqlalchemy.orm import Session
from schemas import crud, orm
from typing import List, Optional

# Users


def get_user(db: Session, external_id: str) -> Optional[crud.User]:
    return db.query(orm.User).filter(orm.User.external_id == external_id).first()


def create_user(
    db: Session, user: crud.UserBase, skills: List[crud.SkillBase]
) -> crud.User:
    db_user = orm.User(external_id=user.external_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    for sk in skills:
        db_skill = orm.Skill(name=sk.skill_name, level=sk.level, months=sk.months)
        db_skill.users.append(db_user)
        db.add(db_skill)
    db.commit()
    return db_user


# Projects


def get_project(db: Session, external_id: str) -> Optional[crud.Project]:
    return db.query(orm.Project).filter(orm.Project.external_id == external_id).first()


def create_project(
    db: Session,
    project: crud.ProjectBase,
    skills: List[crud.SkillBase],
) -> crud.Project:
    db_proj = orm.Project(external_id=project.external_id)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    for sk in skills:
        db_skill = orm.Skill(name=sk.skill_name, level=sk.level, months=sk.months)
        db_skill.projects.append(db_proj)
        db.add(db_skill)
    db.commit()
    return db_proj


# Interactions


def create_interaction(
    db: Session, interaction: crud.InteractionBase
) -> crud.Interaction:
    db_int = orm.Interaction(
        user_id=interaction.user_id,
        project_id=interaction.project_id,
        rating=interaction.rating,
    )
    db.add(db_int)
    db.commit()
    db.refresh(db_int)
    return db_int


def get_interactions(
    db: Session, skip: int = 0, limit: int = 100
) -> List[crud.Interaction]:
    return db.query(orm.Interaction).offset(skip).limit(limit).all()
