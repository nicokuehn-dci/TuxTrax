import json
import logging
import PyPDF2
import os

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

    def process_text_file(self, file_path):
        try:
            if file_path.endswith('.pdf'):
                return self._process_pdf(file_path)
            elif file_path.endswith('.txt') or file_path.endswith('.md'):
                return self._process_text(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return None

    def _process_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfFileReader(f)
                text = ""
                for page_num in range(reader.numPages):
                    text += reader.getPage(page_num).extract_text()
                return text
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {e}")
            return None

    def _process_text(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return None

    def learn_from_text(self, text):
        try:
            # Placeholder for learning logic
            logger.info("Learning from text.")
            self.model['learned_texts'] = self.model.get('learned_texts', []) + [text]
            self.save_model()
        except Exception as e:
            logger.error(f"Error learning from text: {e}")
