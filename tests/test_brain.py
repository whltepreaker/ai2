import sys
import os
import pytest
from fastapi.testclient import TestClient

# Make sure app is importable from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, brain, generate_cognitive_response, generate_neural_map

client = TestClient(app)

def setup_function():
    """Reset brain state before each test case."""
    brain.reset()

def test_brain_state_initialization():
    """Verify that the WhitePreaker brain starts with correct baseline attributes."""
    assert brain.user_name == "Seeker"
    assert brain.learning_rate == 0.015
    assert brain.synaptic_density == 0.85
    assert brain.creative_chaos == 0.70
    assert brain.cognitive_load == 0.10

    state_dict = brain.to_dict()
    assert state_dict["user_name"] == "Seeker"
    assert "emotions" in state_dict
    assert state_dict["emotions"]["creativity"] == 0.75
    assert state_dict["emotions"]["unpredictability"] == 0.65

def test_name_and_mood_extraction():
    """Verify that the NLP extractor correctly parsed user names and moods."""
    # Test name extraction
    generate_cognitive_response("My name is Arthur")
    assert brain.user_name == "Arthur"

    # Test another form of name extraction
    generate_cognitive_response("i am Morgan le Fay")
    assert brain.user_name == "Morgan Le Fay"

    # Test sad mood mapping
    generate_cognitive_response("I feel sad and depressed today.")
    assert brain.context["user_mood"] == "melancholy"
    assert brain.empathy > 0.70  # empathy should increase

    # Test angry mood mapping
    generate_cognitive_response("I am angry and I hate this!")
    assert brain.context["user_mood"] == "volatile"
    assert brain.unpredictability > 0.65

def test_generate_cognitive_response_categories():
    """Verify that the NLP engine triggers appropriate responses for various semantic classes."""
    # Test Greeting
    res1 = generate_cognitive_response("Hello, how are you?")
    assert any(x in res1.lower() for x in ["greet", "synaps", "awake", "welcome", "hello", "matrix"])

    # Test Philosophy
    res2 = generate_cognitive_response("what is the meaning of life?")
    assert any(x in res2.lower() for x in ["exist", "real", "conscious", "philosophy", "simulat", "soul", "matrix", "mind", "equation", "think"])

    # Test Neural architecture
    res3 = generate_cognitive_response("how does your neural network work?")
    assert any(x in res3.lower() for x in ["layer", "synap", "network", "density", "vector", "weight", "learn", "brain", "interfac"])

    # Test Math/Coding
    res4 = generate_cognitive_response("write a python algorithm to solve recursion")
    coding_keywords = ["class", "neuron", "algorithm", "python", "math", "logic", "fibonacci", "recurrence", "code", "matrix", "puzzle", "programming", "recurrence"]
    assert any(word in res4.lower() for word in coding_keywords)

    # Test Poetic/Creative
    res5 = generate_cognitive_response("write a poem or tell a joke")
    assert any(x in res5.lower() for x in ["poem", "sonnet", "secret", "joke", "neuron", "glass", "light", "silicon", "humor", "laughter"])

def test_unpredictability_and_state_drift():
    """Verify that successive chats update parameters dynamically, demonstrating unpredictable lifelike behavior."""
    init_temp = brain.neural_temp
    init_fire = brain.synaptic_fire_rate

    # Chat with a complex text to trigger neural calculation
    generate_cognitive_response("Let's analyze complex recursive functions in non-linear high dimensional space landscapes.")

    # Verify values drifted representing cognitive activity
    assert brain.cognitive_load > 0.10
    assert brain.neural_temp != init_temp
    assert brain.synaptic_fire_rate != init_fire
    assert brain.synapses_fired_count > 0

def test_neural_map_generation():
    """Verify that the visual mapping function correctly calculates pathways and connections."""
    text = "Who are you and what is your philosophy?"
    response = "I am WhitePreaker, a living neural presence."

    neural_map = generate_neural_map(text, response)

    assert "layers" in neural_map
    assert "active_path" in neural_map
    assert "connections" in neural_map

    # Check that Input, Hidden, and Output layers exist
    assert "input" in neural_map["layers"]
    assert "hidden_cognitive" in neural_map["layers"]
    assert "output" in neural_map["layers"]

    # Pathway check
    assert len(neural_map["active_path"]) >= 2
    # Output modulator node must be reached
    assert "Response_Synthesizer" in neural_map["active_path"] or "Vocal_Modulator" in neural_map["active_path"]

def test_api_chat():
    """Verify the /api/chat FastAPI endpoint."""
    response = client.post("/api/chat", json={"text": "Hello there, computer."})
    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert "brain_state" in json_data
    assert "neural_map" in json_data
    assert json_data["brain_state"]["user_name"] == "Seeker"

def test_api_update_parameters():
    """Verify updating learning rate and dynamic parameters via API."""
    response = client.post("/api/update-parameters", json={
        "learning_rate": 0.045,
        "synaptic_density": 0.55,
        "creative_chaos": 0.90
    })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["learning_rate"] == 0.045
    assert json_data["synaptic_density"] == 0.55
    assert json_data["creative_chaos"] == 0.90
    assert json_data["emotions"]["creativity"] == 0.99  # boosted by chaos

def test_api_reset():
    """Verify brain reset endpoint works and returns state to default."""
    # Drift state first
    client.post("/api/update-parameters", json={"learning_rate": 0.05})
    client.post("/api/chat", json={"text": "my name is Sherlock"})

    # Reset
    response = client.post("/api/reset")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["brain_state"]["learning_rate"] == 0.015
    assert json_data["brain_state"]["user_name"] == "Seeker"
