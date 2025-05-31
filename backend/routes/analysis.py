from fastapi import APIRouter, HTTPException

from typing import Any, Dict, List

import openai

from constants import SKILL_CATEGORIES, LEVEL_WEIGHT
from schemas.predict import AnalysisInput, AnalysisOutput
from dataset_generation.llm_config import (
    ModelProvider,
    OllamaModels,
    OpenAIModels,
    init_llm_client,
)

from settings import settings

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)


async def perform_analysis_from_context(
    client: openai.Client,
    model_name: str,
    text: str,
    max_tokens: int = 200,
    temperature: float = 0.2,
) -> AnalysisOutput:
    prompt = (
        "You are a senior talent-and-training consultant. "
        "You will receive a JSON object with two parts:\n\n"
        "1. Employee profile:\n"
        "   - employee_skills: a list of {skill_name, level, months}\n"
        "   - employee_description: a brief bio of the employee\n\n"
        "2. Project requirements:\n"
        "   - project_skills: a list of {skill_name, level, months}\n"
        "   - project_description: a brief overview of the project goals\n\n"
        "Consider the following skills: " + ", ".join(SKILL_CATEGORIES) + ".\n"
        "Recognized levels: " + ", ".join(LEVEL_WEIGHT) + ".\n\n"
        "Answer with JSON conforming to the AnalysisOutput schema, containing exactly two fields:\n"
        "  fitness_evaluation: A single value (High, Medium, or Low) followed by a one-sentence justification.\n"
        "  recommended_courses: A concise recommendation of training or activities to cover any identified gaps.\n\n"
        "Example output:\n"
        "{\n"
        '  "fitness_evaluation": "Medium - Strong Python background, but lacks Docker experience.",\n'
        '  "recommended_courses": "Complete an intermediate Docker workshop and practice containerizing two microservices."\n'
        "}"
    )

    response = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        response_format=AnalysisOutput,
    )
    return response.choices[0].message.parsed


@router.post("/", response_model=AnalysisOutput)
async def generate_analysis(payload: AnalysisInput) -> AnalysisOutput:
    """
    Generate an analysis of how well an employee fits a project and recommend training to address any skill gaps.

    Parameters:
    -----------
    payload: AnalysisInput
        - employee_skills: List of SkillMetadata (skill_name, level, months)
        - employee_description: str (brief employee bio)
        - project_skills: List of SkillMetadata (skill_name, level, months)
        - project_description: str (project context and goals)
        - score: float (relevance score between employee and project)

    Returns:
    --------
    AnalysisOutput
        - fitness_evaluation: "High", "Medium", or "Low" plus a short justification
        - recommended_courses: concise next steps to upskill for any identified gaps

    Example:
    --------
    **Request body:**
    ```json
    {
      "employee_skills": [
        {"skill_name": "Python", "level": "Professional", "months": 24},
        {"skill_name": "Docker", "level": "Basic", "months": 3}
      ],
      "employee_description": "Senior backend developer with extensive API experience.",
      "project_skills": [
        {"skill_name": "Python", "level": "Professional", "months": 12},
        {"skill_name": "Docker", "level": "Professional", "months": 6},
        {"skill_name": "Cloud Platform", "level": "CollegeResearch", "months": 3}
      ],
      "project_description": "Containerize microservices for a real-time analytics platform.",
      "score": 0.75
    }
    ```

    **Response:**
    ```json
    {
      "fitness_evaluation": "Medium - Excellent Python background, but Docker skills need deepening.",
      "recommended_courses": "Enroll in an advanced Docker course and complete two hands-on container projects."
    }
    ```
    """
    try:
        if settings.OPENAI_API_KEY == "":
            model_name = OllamaModels.GEMMA3_1B
            client = init_llm_client(ModelProvider.OLLAMA, model_name)
        else:
            model_name = OpenAIModels.GPT_4O
            client = init_llm_client(ModelProvider.OPENAI, OpenAIModels.GPT_4O)

        context_text = " ".join(
            [
                f"Employee skills: {payload.employee_skills}",
                f"Employee description: {payload.employee_description}",
                f"Project skills: {payload.project_skills}",
                f"Project description: {payload.project_description}",
                f"Score: {payload.score}",
            ]
        )

        analysis = await perform_analysis_from_context(
            client=client,
            model_name=model_name.value,
            text=context_text,
            max_tokens=7000,
            temperature=0.5,
        )
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
