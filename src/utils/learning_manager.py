import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LearningManager:
    def __init__(self, model_path="model.json"):
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        try:
            with open(self.model_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.info("Model file not found. Initializing new model.")
            return {}
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return {}

    def save_model(self):
        try:
            with open(self.model_path, 'w') as f:
                json.dump(self.model, f)
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def capture_user_input(self, input_data):
        try:
            self.model['user_inputs'] = self.model.get('user_inputs', []) + [input_data]
            self.save_model()
        except Exception as e:
            logger.error(f"Error capturing user input: {e}")

    def capture_user_output(self, output_data):
        try:
            self.model['user_outputs'] = self.model.get('user_outputs', []) + [output_data]
            self.save_model()
        except Exception as e:
            logger.error(f"Error capturing user output: {e}")

    def update_model(self):
        try:
            # Placeholder for model update logic
            logger.info("Updating model based on user interactions.")
            self.save_model()
        except Exception as e:
            logger.error(f"Error updating model: {e}")
