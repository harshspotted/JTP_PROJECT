import os
import logging
import json
import pandas as pd
from enum import Enum
from typing import Dict, Callable, List, Any

import openai
from pydantic import BaseModel, ValidationError

from helpers import process_jobs, process_resumes
from llm_config import ModelProvider, OllamaModels, OpenAIModels, init_llm_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------- Main ----------


async def main():

    # Using Local LLM
    provider = ModelProvider.OLLAMA
    model = OllamaModels.GEMMA3_1B

    # # Uncomment to use OpenAI Models instead
    # provider = ModelProvider.OPENAI
    # model = OpenAIModels.GPT_4_1

    # Initialize Client
    client = init_llm_client(provider, model)

    # Process data

    resumes_csv = "data/resume_scraped.csv"
    jobs_csv = "data/jobs_scraped.csv"

    await process_resumes(
        client,
        model.value,
        resumes_csv,
        "outputs/output_employee_parsed.json",
        "outputs/output_employee_data.json",
        "outputs/output_employee_mapping.json",
        max_records=5000,
    )

    await process_jobs(
        client,
        model.value,
        jobs_csv,
        "outputs/output_projects_parsed.json",
        "outputs/output_projects_data.json",
        "outputs/output_projects_mapping.json",
        max_records=1000,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
