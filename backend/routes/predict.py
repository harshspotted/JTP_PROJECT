from fastapi import APIRouter, HTTPException
from schemas.predict import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationWithMetaDataResult,
)
from services.predict import RecommendationService
from typing import List


router = APIRouter(
    prefix="/predict",
    tags=["Predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=List[RecommendationWithMetaDataResult])
async def recommend_projects(payload: RecommendationRequest):
    """
    Recommend the top-K most relevant projects based on user's skills and description.

    This endpoint takes a list of skills and a textual description of the candidate,
    and returns a ranked list of recommended projects with metadata such as matching score,
    project description, and required skills.

    Parameters:
    -----------
    **payload** : `RecommendationRequest`
        A JSON object containing:
        - skills: List of skills with name, level, and months of experience.
        - description: A short free-text description of the candidate (e.g., interests or goals).
        - top_k: Number of top matching projects to return.

    Returns:
    --------
    `List[RecommendationWithMetaDataResult]`
        A list of recommendations sorted by relevance score in descending order. Each result includes:
        - rank: Rank of the project (1 being the highest match).
        - project_id: Unique identifier of the project.
        - score: Relevance score from the recommendation model.
        - description: Textual summary of the project.
        - required_skills: List of skill metadata that the project requires.

    Example:
    --------
    **Request body:**
    {
        "skills": [
            {"skill_name": "Python", "level": "CollegeResearch", "months": 12},
            {"skill_name": "Docker", "level": "Professional", "months": 6}
        ],
        "description": "I love backend development and want to work on scalable systems.",
        "top_k": 3
    }

    **Response:**
    [
        {
            "rank": 1,
            "project_id": "project_22",
            "score": 55707.93,
            "description": "A backend project using Docker and Python...",
            "required_skills": [
                {"skill_name": "Python", "level": "Professional", "months": 12},
                {"skill_name": "Docker", "level": "CollegeResearch", "months": 6}
            ]
        },
        ...
    ]
    """
    try:
        service = RecommendationService()

        result = await service.recommend_with_metadata(
            skills=[s.model_dump() for s in payload.skills],
            description=payload.description,
            top_k=payload.top_k,
        )

        return result

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
