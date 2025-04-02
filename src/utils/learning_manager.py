import json
import logging
import PyPDF2
import os
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LearningManager:
    def __init__(self, model_path=None, db_path=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = model_path or os.path.join(script_dir, "model.json")
        self.db_path = db_path or os.path.join(script_dir, "learning_data.db")
        self.model = self.load_model()
        self._setup_database()

    def _setup_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS learned_data (
                                    id INTEGER PRIMARY KEY,
                                    data_type TEXT,
                                    content TEXT)''')
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error setting up database: {e}")

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
            self._save_to_database('user_input', input_data)
        except Exception as e:
            logger.error(f"Error capturing user input: {e}")

    def capture_user_output(self, output_data):
        try:
            self.model['user_outputs'] = self.model.get('user_outputs', []) + [output_data]
            self.save_model()
            self._save_to_database('user_output', output_data)
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
                text = self._process_pdf(file_path)
            elif file_path.endswith('.txt') or file_path.endswith('.md'):
                text = self._process_text(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path}")
                return None

            if text:
                self._save_to_database('processed_text', text)
            return text
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
            self._save_to_database('learned_text', text)
        except Exception as e:
            logger.error(f"Error learning from text: {e}")

    def _save_to_database(self, data_type, content):
        try:
            self.cursor.execute("INSERT INTO learned_data (data_type, content) VALUES (?, ?)", (data_type, content))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving to database: {e}")

    def load_from_database(self, data_type):
        try:
            self.cursor.execute("SELECT content FROM learned_data WHERE data_type=?", (data_type,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error loading from database: {e}")
            return []

    def save_model_to_json(self, file_path):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self.model, json_file)
        except Exception as e:
            logger.error(f"Error saving model to JSON file {file_path}: {e}")

    def load_model_from_json(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                self.model = json.load(json_file)
        except Exception as e:
            logger.error(f"Error loading model from JSON file {file_path}: {e}")
