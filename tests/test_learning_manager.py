import pytest
import os
import json
from src.utils.learning_manager import LearningManager

@pytest.fixture
def learning_manager(tmp_path):
    model_path = tmp_path / "model.json"
    return LearningManager(model_path=str(model_path))

def test_capture_user_input(learning_manager):
    input_data = "User input example"
    learning_manager.capture_user_input(input_data)
    assert input_data in learning_manager.model['user_inputs']

def test_capture_user_output(learning_manager):
    output_data = "User output example"
    learning_manager.capture_user_output(output_data)
    assert output_data in learning_manager.model['user_outputs']

def test_update_model(learning_manager):
    input_data = "User input example"
    output_data = "User output example"
    learning_manager.capture_user_input(input_data)
    learning_manager.capture_user_output(output_data)
    learning_manager.update_model()
    assert 'user_inputs' in learning_manager.model
    assert 'user_outputs' in learning_manager.model

def test_process_text_file(learning_manager, tmp_path):
    # Create a test text file
    text_file = tmp_path / "test.txt"
    text_content = "This is a test text file."
    with open(text_file, 'w') as f:
        f.write(text_content)
    
    processed_text = learning_manager.process_text_file(str(text_file))
    assert processed_text == text_content

def test_learn_from_text(learning_manager):
    text_content = "This is a test text for learning."
    learning_manager.learn_from_text(text_content)
    assert text_content in learning_manager.model['learned_texts']
