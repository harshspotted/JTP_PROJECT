"""
Build Qdrant collections and generate an interaction matrix for recommendation,
including positive hits, hard negatives (via inverted search), and random negatives.
"""

import glob
import os
import json
import uuid
import logging
import random
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from fastembed import TextEmbedding
from settings import settings

# === Configuration ===
SKILL_CATEGORIES = [
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
EMBEDDING_DIM = 384
SKILL_COLLECTION = "employees_by_skills"
DESC_COLLECTION = "employees_by_description"
TOP_K = 50  # positive candidates
NEG_K = 5  # hard negatives per method
RAND_NEG_K = 10  # random negatives per project
HYBRID_ALPHA = 0.65  # weight for skill vs description
SCORE_THRESHOLD = 0.3  # minimum for positive
OUTPUT_PATH = "outputs/interactions.json"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def make_skill_vector(skills):
    vec = [0.0] * len(SKILL_CATEGORIES)
    for sk in skills:
        name = sk.get("skill_name")
        level = sk.get("level")
        months = sk.get("months", 0)
        if name in SKILL_CATEGORIES:
            idx = SKILL_CATEGORIES.index(name)
            vec[idx] += months * LEVEL_WEIGHT.get(level, 1.0)
    return vec


def connect_qdrant():
    url = settings.QDRANT_URL
    key = settings.QDRANT_API_KEY
    if not url or not key:
        raise EnvironmentError(
            "Set QDRANT_URL and QDRANT_API_KEY environment variables"
        )
    return QdrantClient(url=url, api_key=key, prefer_grpc=False)


def recreate_collection(client, name: str, vector_size: int):
    client.recreate_collection(
        collection_name=name,
        vectors_config=VectorParams(size=vector_size, distance="Cosine"),
    )


def upsert_employees(client, name: str, employees: list):
    points = []
    for emp in employees:
        full_id, rec = next(iter(emp.items()))
        try:
            point_id = int(full_id.split("_")[-1])
        except ValueError:
            point_id = uuid.uuid5(uuid.NAMESPACE_DNS, full_id)
        vec = make_skill_vector(rec.get("skills", []))
        payload = {
            "emp_id": full_id,
            "description": rec.get("description"),
            "skills": rec.get("skills"),
        }
        points.append(PointStruct(id=point_id, vector=vec, payload=payload))
    client.upsert(collection_name=name, points=points)


def upsert_descriptions(client, name: str, employees: list, embedder: TextEmbedding):
    points = []
    for emp in employees:
        full_id, rec = next(iter(emp.items()))
        try:
            point_id = int(full_id.split("_")[-1])
        except ValueError:
            point_id = uuid.uuid5(uuid.NAMESPACE_DNS, full_id)
        desc = rec.get("description", "")
        emb = list(embedder.embed([desc]))
        vector = emb[0] if emb else [0.0] * EMBEDDING_DIM
        payload = {"emp_id": full_id, "skills": rec.get("skills")}
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))
    client.upsert(collection_name=name, points=points)


def search_by_skills(client, skills: list, top_k: int):
    vec = make_skill_vector(skills)
    return client.search(
        collection_name=SKILL_COLLECTION, query_vector=vec, limit=top_k
    )


def search_by_description(client, text: str, embedder: TextEmbedding, top_k: int):
    emb = list(embedder.embed([text]))
    vec = emb[0] if emb else [0.0] * EMBEDDING_DIM
    return client.search(collection_name=DESC_COLLECTION, query_vector=vec, limit=top_k)


def search_negatives_by_skills(client, skills: list, neg_k: int):
    vec = make_skill_vector(skills)
    inv = [-x for x in vec]
    return client.search(
        collection_name=SKILL_COLLECTION, query_vector=inv, limit=neg_k
    )


def search_negatives_by_description(
    client, text: str, embedder: TextEmbedding, neg_k: int
):
    emb = list(embedder.embed([text]))
    inv = [-x for x in (emb[0] if emb else [0.0] * EMBEDDING_DIM)]
    return client.search(collection_name=DESC_COLLECTION, query_vector=inv, limit=neg_k)


def sample_random_negatives(employees: list, exclude_ids: set, num: int):
    all_ids = [list(e.keys())[0] for e in employees]
    pool = list(set(all_ids) - exclude_ids)
    return random.sample(pool, min(num, len(pool)))


def generate_interactions(employees, projects, client, embedder):
    interactions = []
    logger.info("Generating interaction matrix for %d projects", len(projects))
    for proj in tqdm(projects, desc="Projects"):
        proj_id, rec = next(iter(proj.items()))
        skills = rec.get("skills", [])
        desc = rec.get("description", "")
        seen_users = set()

        # Positive candidates
        hits_skills = search_by_skills(client, skills, TOP_K)
        hits_desc = search_by_description(client, desc, embedder, TOP_K)

        # Collect positive interactions
        for hit in (*hits_skills, *hits_desc):
            pid, score = hit.id, hit.score
            if pid in seen_users:
                continue
            # compute hybrid
            s_score = next((h.score for h in hits_skills if h.id == pid), 0.0)
            d_score = next((h.score for h in hits_desc if h.id == pid), 0.0)
            hybrid = HYBRID_ALPHA * s_score + (1 - HYBRID_ALPHA) * d_score
            if hybrid >= SCORE_THRESHOLD:
                emp_id = hit.payload["emp_id"]
                interactions.append(
                    {
                        "user_id": emp_id,
                        "project_id": proj_id,
                        "rating": round(hybrid, 4),
                    }
                )
                seen_users.add(pid)

        # Hard negatives
        for neg in search_negatives_by_skills(client, skills, NEG_K):
            if neg.id in seen_users:
                continue
            interactions.append(
                {"user_id": neg.payload["emp_id"], "project_id": proj_id, "rating": 0.0}
            )
            seen_users.add(neg.id)
        for neg in search_negatives_by_description(client, desc, embedder, NEG_K):
            if neg.id in seen_users:
                continue
            interactions.append(
                {"user_id": neg.payload["emp_id"], "project_id": proj_id, "rating": 0.0}
            )
            seen_users.add(neg.id)

        # Random negatives
        for emp_id in sample_random_negatives(employees, seen_users, RAND_NEG_K):
            interactions.append(
                {"user_id": emp_id, "project_id": proj_id, "rating": 0.0}
            )

    return interactions


def main():
    logger.info("Loading JSON data...")
    emp_path = os.path.expanduser("outputs/output_employee_parsed.json")
    proj_path = os.path.expanduser("outputs/output_projects_parsed.json")
    employees = json.load(open(emp_path))
    projects = json.load(open(proj_path))

    logger.info("Initializing embedder and Qdrant client")
    embedder = TextEmbedding()
    client = connect_qdrant()

    # (Re)create collections
    recreate_collection(client, SKILL_COLLECTION, len(SKILL_CATEGORIES))
    recreate_collection(client, DESC_COLLECTION, EMBEDDING_DIM)

    # Upsert
    logger.info("Upserting employee skill vectors...")
    upsert_employees(client, SKILL_COLLECTION, employees)
    logger.info("Upserting employee description embeddings...")
    upsert_descriptions(client, DESC_COLLECTION, employees, embedder)

    # Generate interactions
    interactions = generate_interactions(employees, projects, client, embedder)

    # Save
    logger.info("Saving interactions to %s", OUTPUT_PATH)
    with open(OUTPUT_PATH, "w") as out:
        json.dump({"interactions": interactions}, out, indent=2)
    logger.info("Done. Total interactions: %d", len(interactions))


if __name__ == "__main__":
    main()
