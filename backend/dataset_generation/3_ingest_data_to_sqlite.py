# This file is run once to initialize the data into SQL Alchemy

import json
from database import SessionLocal, Base, engine
from schemas.orm import Skill, User, Project, Interaction


def init_db():
    Base.metadata.create_all(bind=engine)


def ingest():
    with open("./data/training_data.json") as f:
        data = json.load(f)
    db = SessionLocal()
    for uid, info in data.get("users", {}).items():
        user = User(external_id=uid)
        db.add(user)
        db.commit()
        db.refresh(user)
        for sk in info.get("skills", []):
            skill = Skill(name=sk["skill_name"], level=sk["level"], months=sk["months"])
            skill.users.append(user)
            db.add(skill)
        db.commit()
    for pid, info in data.get("projects", {}).items():
        proj = Project(external_id=pid)
        db.add(proj)
        db.commit()
        db.refresh(proj)
        for sk in info.get("skills", []):
            skill = Skill(name=sk["skill_name"], level=sk["level"], months=sk["months"])
            skill.projects.append(proj)
            db.add(skill)
        for it in info.get("interactions", []):
            print(it)
            interaction = Interaction(
                user_id=it["user_id"], project_id=pid, rating=it["rating"]
            )
            db.add(interaction)
        db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
    ingest()
