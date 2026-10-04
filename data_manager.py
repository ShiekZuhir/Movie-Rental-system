import json
import os
from typing import Dict, Any


class DataManager:
    def __init__(self, data_folder: str = "data"):
        self.data_folder = data_folder
        self.ensure_data_folder_exists()

    def ensure_data_folder_exists(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def save_data(self, data: Dict[str, Any], filename: str = "cinema_at_home_data.json") -> bool:
        try:
            filepath = os.path.join(self.data_folder, filename)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved successfully to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self, filename: str = "cinema_at_home_data.json") -> Dict[str, Any]:
        try:
            filepath = os.path.join(self.data_folder, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"Data loaded successfully from {filepath}")
            return data
        except FileNotFoundError:
            print(f"No saved data found at {filepath}. Starting with empty system.")
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}