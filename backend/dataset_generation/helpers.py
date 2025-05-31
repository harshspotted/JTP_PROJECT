import os
import logging
import json
import pandas as pd
from enum import Enum
from typing import Dict, Callable, List, Any, Literal

import openai
from pydantic import BaseModel, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Constants ----------

SKILL_CATEGORIES: List[str] = [
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
LEVEL_WEIGHT = {"Basic": 1.0, "CollegeResearch": 2.0, "Professional": 3.0, "Other": 1.5}

# ---------- Data Models ----------


class Skill(BaseModel):
    skill_name: Literal[
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
    level: Literal["Basic", "CollegeResearch", "Professional", "Other"]
    months: int


class SkillList(BaseModel):
    skills: List[Skill]


# ---------- Helper Functions ----------


def dedupe_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for s in skills:
        key = (s["skill_name"], s["level"], s["months"])
        if key not in seen:
            seen.add(key)
            result.append(s)
    return result


async def recognize_skills(
    client: openai.Client,
    model_name: str,
    text: str,
    max_tokens: int = 40,
    temperature: float = 0.2,
) -> List[Dict[str, Any]]:

    prompt = (
        "You are an expert data extraction agent. Given any free-form text, "
        "identify mentions of: " + ", ".join(SKILL_CATEGORIES) + ". "
        "Assign a level from: " + ", ".join(LEVEL_WEIGHT.keys()) + ". "
        "Estimate months of experience, estimate the months of experience if stated or reasonably implied (round to nearest whole month). Output a JSON list of objects with keys: skill_name, level, months. Example output:"
        "["
        "{'skill_name': 'Python', 'level': 'Professional', 'months': 24},"
        "{'skill_name': 'Git', 'level': 'Basic', 'months': 6}"
        "]"
    )
    try:
        resp = client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=SkillList,
        )
        return [s.model_dump() for s in resp.choices[0].message.parsed.skills]
    except Exception as e:
        logger.error(f"Skill recognition failed: {e}")
        return []


def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------- Processing Functions ----------


async def process_resumes(
    client: openai.Client,
    model_name: str,
    resumes_path: str,
    output_parsed: str,
    output_data: str,
    output_map: str,
    max_records: int = None,
):
    df = pd.read_csv(resumes_path)
    parsed, data, mapping = [], [], {}

    for idx, row in df.iterrows():
        if max_records and idx >= max_records:
            break
        skills = await recognize_skills(
            client, model_name, row["text"], max_tokens=12000
        )
        skills = dedupe_skills(skills)
        if not skills:
            continue

        emp_id = int(row["resume_id"])
        key = f"employee_{emp_id}"
        parsed.append({key: {"description": row["text"], "skills": skills}})
        data.append(
            {
                "employee_id": emp_id,
                "resume_text": row["text"],
                "roles": "_".join(eval(row["labels"])),
            }
        )
        mapping[emp_id] = {
            "parsed_index": len(parsed) - 1,
            "data_index": len(data) - 1,
            "parsed_key": key,
        }

    write_json(output_parsed, parsed)
    write_json(output_data, data)
    write_json(output_map, mapping)


async def process_jobs(
    client: openai.Client,
    model_name: str,
    jobs_path: str,
    output_parsed: str,
    output_data: str,
    output_map: str,
    max_records: int = None,
):
    df = pd.read_csv(jobs_path)
    parsed, data, mapping = [], [], {}

    for idx, row in df.iterrows():
        if max_records and idx >= max_records:
            break
        desc = f"{row['jobtitle']}: {row['jobdescription']}"
        skills = await recognize_skills(client, model_name, desc, max_tokens=10000)
        skills = dedupe_skills(skills)
        if not skills:
            continue

        proj_id = idx + 1
        key = f"project_{proj_id}"
        parsed.append({key: {"description": desc, "skills": skills}})
        data.append(
            {
                "project_id": proj_id,
                "project_text": desc,
                "roles": row["jobtitle"],
                "experience": row.get("experience"),
            }
        )
        mapping[proj_id] = {
            "parsed_index": len(parsed) - 1,
            "data_index": len(data) - 1,
            "parsed_key": key,
        }

    write_json(output_parsed, parsed)
    write_json(output_data, data)
    write_json(output_map, mapping)
