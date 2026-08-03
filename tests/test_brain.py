import sys
import os
import re
import pytest
from fastapi.testclient import TestClient

# Make sure app is importable from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, brain, generate_neural_map, DirectiveExtractor, ToneModulator, SYNAPTIC_SPARKS

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
    assert "last_topic" in state_dict
    assert state_dict["last_topic"] == "general"

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


def test_conversational_patterns_and_greetings():
    """Verify that greetings and specific conversational intents yield natural human-like responses."""
    # Test Greeting
    response = client.post("/api/chat", json={"text": "hello whitepreaker"})
    assert response.status_code == 200
    data = response.json()
    assert "WhitePreaker" in data["response"]
    assert any(w in data["response"].lower() for w in ["chat", "mind", "explore", "seeker", "inquiry", "discourse", "discuss", "active", "online", "pathways"])

    # Test Identity of AI
    response = client.post("/api/chat", json={"text": "who are you?"})
    assert "WhitePreaker" in response.json()["response"]
    assert "neural system" in response.json()["response"] or "conversational AI" in response.json()["response"]

    # Test Identity of User (unregistered default is Seeker)
    response_my_name1 = client.post("/api/chat", json={"text": "what is my name?"})
    assert "Seeker" in response_my_name1.json()["response"]

    # Test Identity of User after registration
    response_reg = client.post("/api/chat", json={"text": "my name is Alex"})
    response_my_name2 = client.post("/api/chat", json={"text": "what is my name"})
    assert "Alex" in response_my_name2.json()["response"]

    # Test Scientific Domain
    response = client.post("/api/chat", json={"text": "tell me about quantum physics"})
    assert "spacetime" in response.json()["response"].lower() or "quantum" in response.json()["response"].lower() or "physics" in response.json()["response"].lower()

    # Test Fallback and context extraction
    response = client.post("/api/chat", json={"text": "let us discuss photosynthesis"})
    assert "photosynthesis" in response.json()["response"].lower()

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

def test_parameter_auto_modulation():
    """Verify that learning rate, synaptic density, and creative chaos auto-modulate and stay within bounds."""
    brain.reset()
    lr_init = brain.learning_rate
    sd_init = brain.synaptic_density
    cc_init = brain.creative_chaos

    # Send a highly complex prompt to trigger modulation
    client.post("/api/chat", json={"text": "Explain quantum superpositions and chaotic unpredictable jump states in a complex scientific way with maximum details."})

    # Assert parameters changed
    assert brain.learning_rate != lr_init or brain.synaptic_density != sd_init or brain.creative_chaos != cc_init

    # Ensure all parameters remain capped strictly in [0.0, 1.0]
    assert 0.0 <= brain.learning_rate <= 1.0
    assert 0.0 <= brain.synaptic_density <= 1.0
    assert 0.0 <= brain.creative_chaos <= 1.0


def test_fallback_response_uniqueness():
    """Verify that consecutive fallback responses are not identical and include context/topic dynamically."""
    brain.reset()

    # Send two unique unknown fallback queries
    res1 = client.post("/api/chat", json={"text": "Who is the prime minister of some imaginary country?"})
    res2 = client.post("/api/chat", json={"text": "What is the taste of a purple elephant's shadow?"})

    ans1 = res1.json()["response"]
    ans2 = res2.json()["response"]

    # They shouldn't be identical
    assert ans1 != ans2

    # They should reflect some extracted context/topic
    assert "prime" in ans1.lower() or "minister" in ans1.lower() or "imaginary" in ans1.lower() or "shadow" in ans2.lower() or "elephant" in ans2.lower()

def test_expanded_conversational_domains():
    """Verify that the new expanded vocabulary domains set last_topic and respond correctly."""
    brain.reset()

    # Test Cyberpunk Domain
    res = client.post("/api/chat", json={"text": "What is cyberpunk and decentralized grids?"})
    assert res.status_code == 200
    data = res.json()
    assert data["brain_state"]["last_topic"] == "cyberpunk"
    assert "neon" in data["response"].lower() or "cyberpunk" in data["response"].lower() or "sovereign" in data["response"].lower()

    # Test History Domain
    res2 = client.post("/api/chat", json={"text": "Tell me about ancient civilizations and roman empire"})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["brain_state"]["last_topic"] == "history"
    assert "civilization" in data2["response"].lower() or "ancient" in data2["response"].lower() or "rome" in data2["response"].lower() or "history" in data2["response"].lower()

    # Test Coding Domain
    res3 = client.post("/api/chat", json={"text": "How do I optimize python asynchronous event loop code?"})
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["brain_state"]["last_topic"] == "coding"
    assert "python" in data3["response"].lower() or "function" in data3["response"].lower() or "recursive" in data3["response"].lower()

def test_context_aware_followups():
    """Verify that follow-up triggers like 'why' use the previous last_topic to generate meaningful follow-ups."""
    brain.reset()

    # 1. Start with a Physics topic
    client.post("/api/chat", json={"text": "Let us talk about quantum entanglement"})
    assert brain.last_topic == "physics"

    # 2. Ask a follow-up "why?" or "tell me more"
    res = client.post("/api/chat", json={"text": "explain how that works and tell me more"})
    assert res.status_code == 200
    data = res.json()
    # Should speak about quantum mechanics or spacetime since topic is physics
    assert "superposition" in data["response"].lower() or "measurement" in data["response"].lower() or "quantum" in data["response"].lower() or "spacetime" in data["response"].lower() or "gravity" in data["response"].lower()

    # 3. Switch to Coding
    client.post("/api/chat", json={"text": "I want to code a software API"})
    assert brain.last_topic == "coding"

    # 4. Ask follow up "explain how"
    res2 = client.post("/api/chat", json={"text": "tell me more about this topic"})
    assert "solid" in res2.json()["response"].lower() or "architect" in res2.json()["response"].lower() or "python" in res2.json()["response"].lower() or "software" in res2.json()["response"].lower() or "complexity" in res2.json()["response"].lower()

def test_self_correction_filter():
    """Verify that the dynamic self-correction polisher in ToneModulator cleans up and truncates to 3 sentences."""
    sample_raw = "Diving into physical laws... Unlocking mathematical systems... Exploring philosophical inquiries... Calibrating emotional registers... Analyzing machine intelligence... Activating creative vectors... Booting programming and software core... Interfacing with the neon cyberspace grid... Accessing chronological history files..."
    polished = ToneModulator.self_correct_response(sample_raw)

    assert "Physical laws govern the cosmos." in polished
    assert "Mathematics represents pure logical syntax." in polished
    assert "Philosophy probes the nature of reality." in polished
    # Confirm maximum sentence limit of 3 is strictly enforced
    sentences = re.split(r"(?<=[.!?])\s+", polished)
    assert len(sentences) <= 3

def test_spontaneous_synaptic_sparks():
    """Verify that fallback answers under high creative chaos append a Synaptic Reflection Spark."""
    brain.reset()
    # Force high creative chaos
    brain.creative_chaos = 0.85

    # Send a long fallback query to trigger a spark
    res = client.post("/api/chat", json={"text": "What are the chaotic unpredictable jumps inside your virtual neurons when they think about nothingness?"})
    assert res.status_code == 200
    response_text = res.json()["response"]

    assert "Synaptic Reflection Spark:" in response_text
    # Verify that it appends one of the valid sparks
    assert any(spark in response_text for spark in SYNAPTIC_SPARKS)

def test_dynamic_semantic_learning_loop():
    """Verify that WhitePreaker dynamically learns a user's statement at runtime and semantically recalls it."""
    brain.reset()

    # Send a highly unique informative statement (avoiding formatting trigger words like 'code' or 'python')
    res1 = client.post("/api/chat", json={"text": "My absolute hidden passphrase key is Delta-Omega-99"})
    assert res1.status_code == 200

    # Verify statement was learned
    assert "My absolute hidden passphrase key is Delta-Omega-99" in brain.dynamic_user_corpus

    # Ask a semantic question targeting that learned sentence
    res2 = client.post("/api/chat", json={"text": "Tell me what is my hidden passphrase key?"})
    assert res2.status_code == 200

    data = res2.json()
    assert "Delta-Omega-99" in data["response"]
    assert "previously mentioned" in data["response"]
