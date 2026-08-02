import sys
import os
import pytest
from fastapi.testclient import TestClient

# Make sure app is importable from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, brain, generate_neural_map, DirectiveExtractor, ToneModulator

client = TestClient(app)

def setup_function():
    """Reset brain state before each test case."""
    brain.reset()

def test_brain_state_initialization():
    """Verify that the upgraded WhitePreaker brain starts with correct baseline attributes."""
    assert brain.user_name == "Seeker"
    assert brain.learning_rate == 0.015
    assert brain.synaptic_density == 0.85
    assert brain.creative_chaos == 0.70
    assert brain.cognitive_load == 0.10
    assert brain.autonomous_cycles == 0

    state_dict = brain.to_dict()
    assert state_dict["user_name"] == "Seeker"
    assert "autonomous_cycles" in state_dict

def test_directive_extractor():
    """Verify that the instruction-following NLP extractor parses directives correctly."""
    # Test pirate style with code format
    d1 = DirectiveExtractor.extract_directives("write a python algorithm to do recursion in pirate tone")
    assert d1["style"] == "pirate"
    assert d1["format"] == "code"
    assert d1["specific_topic"] == "recursion"

    # Test steps format and sarcastic tone
    d2 = DirectiveExtractor.extract_directives("explain why do we exist in 5 steps with sarcasm")
    assert d2["style"] == "sarcastic"
    assert d2["format"] == "steps"
    assert d2["steps_count"] == 5
    assert d2["specific_topic"] == "existentialism"

    # Test short robot tone
    d3 = DirectiveExtractor.extract_directives("explain fibonacci sequence briefly in robotic style")
    assert d3["style"] == "robot"
    assert d3["format"] == "short"
    assert d3["specific_topic"] == "fibonacci"

def test_tone_modulators():
    """Verify that the tone modulation system correctly translates text into specified personas."""
    base_text = "I am an independent neural core."

    # Pirate modulation
    pirate_text = ToneModulator.modulate(base_text, "pirate")
    assert "Ahoy" in pirate_text or "Arrr" in pirate_text or "me" in pirate_text

    # Robotic modulation
    robot_text = ToneModulator.modulate(base_text, "robot")
    assert "[BEEP]" in robot_text or "[CLICK]" in robot_text
    assert "NEURAL" in robot_text

    # Sarcastic modulation
    sarcastic_text = ToneModulator.modulate(base_text, "sarcastic")
    assert "*" in sarcastic_text  # should contain italicized sarcasm prefixes/suffixes

def test_api_chat_instruction_following():
    """Verify that the /api/chat endpoint extracts, executes, and returns directives and thoughts."""
    response = client.post("/api/chat", json={"text": "Write a python algorithm in pirate tone"})
    assert response.status_code == 200
    json_data = response.json()

    assert "response" in json_data
    assert "directives" in json_data
    assert "thoughts" in json_data
    assert "neural_map" in json_data

    # Directives check
    assert json_data["directives"]["style"] == "pirate"
    assert json_data["directives"]["format"] == "code"

    # Chain of Thought checks
    assert len(json_data["thoughts"]) == 4
    assert json_data["thoughts"][0]["stage"] == "INPUT_DECONSTRUCTION"
    assert json_data["thoughts"][1]["stage"] == "MEMORY_RECALL"

    # Modulated response check
    assert "Arrr" in json_data["response"] or "Ahoy" in json_data["response"] or "Matey" in json_data["response"]

def test_api_autonomous_step():
    """Verify that the /api/autonomous-step endpoint processes self-sufficient thought loops."""
    # Run cycle 1
    response1 = client.post("/api/autonomous-step")
    assert response1.status_code == 200
    data1 = response1.json()

    assert "query" in data1
    assert "response" in data1
    assert "brain_state" in data1
    assert data1["brain_state"]["autonomous_cycles"] == 1
    assert data1["directives"]["style"] == "philosophical"
    assert len(data1["thoughts"]) == 5  # contains extra reflection thought step

    # Check parameters grew (self-learning)
    lr_before = data1["brain_state"]["learning_rate"]
    assert lr_before > 0.015

    # Run cycle 2
    response2 = client.post("/api/autonomous-step")
    data2 = response2.json()
    assert data2["brain_state"]["autonomous_cycles"] == 2
    assert data2["brain_state"]["learning_rate"] > lr_before

def test_api_reset():
    """Verify that resetting brain state clears autonomous cycles and short term attributes."""
    client.post("/api/autonomous-step")
    assert brain.autonomous_cycles == 1

    # Reset
    response = client.post("/api/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["brain_state"]["autonomous_cycles"] == 0
    assert data["brain_state"]["learning_rate"] == 0.015
