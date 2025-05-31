import keras
import numpy as np
from fastembed import TextEmbedding
from typing import List, Dict, Tuple, Any
from schemas.predict import (
    RecommendationRequest,
    SkillMetadata,
    RecommendationWithMetaDataResult,
)
from constants import LEVEL_WEIGHT, SKILL_CATEGORIES, skill2idx
from models.two_tower import Tower, TwoTowerModel, ResidualBlock
from data.load_projects import load_projects


class RecommendationService:
    def __init__(self):
        """
        A service to generate project recommendations using a two-tower neural network model.

        This class loads a trained model and preprocessed data to generate personalized
        recommendations for users based on their skills and textual description.

        Attributes:
        -----------
        model : keras.Model
            A pre-trained Two-Tower Keras model that computes similarity between user and project vectors.
        project_profiles : np.ndarray
            Numeric skill profile vectors for each project.
        project_text_embs : np.ndarray
            Text embeddings of project descriptions.
        text_model : fastembed.TextEmbedding
            Embedding model used to convert textual descriptions into vector form.
        n_projects : int
            Total number of projects.

        Methods:
        --------
        build_user_vector(skills: List[Dict[str, Any]]) -> np.ndarray
            Convert user's skill dictionary into a numerical feature vector.

        embed_text(text: str) -> np.ndarray
            Convert a text description into a dense vector using the embedding model.

        async recommend(skills: List[Dict[str, Any]], description: str, top_k: int) -> Tuple[List[int], List[float]]
            Compute similarity scores between the user and all projects, return top K matches.

        async recommend_with_metadata(skills: List[Dict[str, Any]], description: str, top_k: int) -> List[RecommendationWithMetaDataResult]
            Wrapper over `recommend` that adds project metadata and returns full details.

        Example:
        --------
        >>> service = RecommendationService()
        >>> await service.recommend(
                skills=[{"skill_name": "Python", "level": "Professional", "months": 10}],
                description="Interested in ML pipelines",
                top_k=3
            )
        ([3, 5, 0], [0.923, 0.902, 0.876])
        """
        # Load the trained model for inference
        model_path = "data/weights/two_tower_model.keras"
        project_profiles_path = "data/weights/project_profiles.npy"
        project_text_embs_path = "data/weights/project_text_embs.npy"

        self.model = keras.saving.load_model(model_path, compile=False)

        self.project_profiles = np.load(project_profiles_path)
        self.project_text_embs = np.load(project_text_embs_path)
        self.text_model = TextEmbedding()
        self.n_projects = self.project_profiles.shape[0]

    def build_user_vector(self, skills: List[Dict[str, Any]]) -> np.ndarray:
        """Convert skill dicts into a numeric feature vector."""
        vec = np.zeros(len(SKILL_CATEGORIES), dtype=float)
        for s in skills:
            name = s["skill_name"]
            level = s["level"]
            months = s["months"]
            if name not in skill2idx or level not in LEVEL_WEIGHT:
                raise ValueError(f"Invalid skill entry: {s}")
            vec[skill2idx[name]] = months * LEVEL_WEIGHT[level]
        return vec

    def embed_text(self, text: str) -> np.ndarray:
        """Generate a text embedding vector."""
        emb_gen = self.text_model.embed([text])
        return np.vstack(list(emb_gen))[0]

    async def recommend(
        self, skills: List[Dict[str, Any]], description: str, top_k: int = 5
    ) -> Tuple[List[int], List[float]]:
        """Return top-K project indices and match scores."""
        user_num = self.build_user_vector(skills)
        user_txt = self.embed_text(description)
        num_tile = np.tile(user_num, (self.n_projects, 1))
        txt_tile = np.tile(user_txt, (self.n_projects, 1))

        # For inference, compile=False model can still run predict
        preds = self.model.predict(
            [num_tile, txt_tile, self.project_profiles, self.project_text_embs],
            verbose=0,
        ).flatten()
        idxs = np.argsort(preds)[-top_k:][::-1]
        return idxs.tolist(), preds[idxs].tolist()

    async def recommend_with_metadata(
        self,
        skills: List[Dict[str, Any]],
        description: str,
        top_k: int = 5,
    ) -> List[RecommendationRequest]:
        """Wraps recommend and returns enriched metadata as Pydantic models."""
        training_data_dict = await load_projects()
        idx2proj = {
            i: pid for i, pid in enumerate(training_data_dict["projects"].keys())
        }
        top_idxs, scores = await self.recommend(skills, description, top_k=top_k)
        enriched: List[RecommendationRequest] = []
        for rank, (idx, score) in enumerate(zip(top_idxs, scores), start=1):
            pid = idx2proj[idx]
            project_data = training_data_dict["projects"].get(pid, {})
            skill_objs = [
                SkillMetadata(
                    skill_name=s.get("skill_name", "Unknown"),
                    level=s.get("level", "Unknown"),
                    months=s.get("months", 0),
                )
                for s in project_data.get("skills", [])
            ]

            enriched.append(
                RecommendationWithMetaDataResult(
                    rank=rank,
                    project_id=pid,
                    score=score,
                    description=project_data.get("description", ""),
                    required_skills=skill_objs,
                )
            )

        return enriched
