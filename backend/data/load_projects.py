import json
from pathlib import Path


# Global variables to store city data.
training_data_dict = {}


async def load_projects(file_path: str = None):
    """
    Loads cities from the given CSV file into global lists.
    """
    global training_data_dict

    if file_path is None:
        file_path = Path(__file__).parent / "training_data.json"

    with open(file_path, encoding="utf-8") as f:
        training_data_dict = json.load(f)

    return training_data_dict
