import random
import re
import math
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="WhitePreaker Cognitive Neural System",
    description="Backend cognitive processor and synaptic state engine for WhitePreaker, a highly powerful, fluent, and unpredictable conversational AI.",
    version="1.0.0"
)

# --- Cognitive State & Memory Models ---

class Message(BaseModel):
    text: str
    user_name: Optional[str] = None

class BrainState:
    def __init__(self):
        self.learning_rate: float = 0.015
        self.synaptic_density: float = 0.85
        self.creative_chaos: float = 0.70
        self.cognitive_load: float = 0.10
        self.neural_temp: float = 36.5  # In celsius
        self.synaptic_fire_rate: float = 120.0 # Hz

        # Emotional & Cognitive Spectrum (0.0 to 1.0)
        self.creativity: float = 0.75
        self.unpredictability: float = 0.65
        self.rationality: float = 0.60
        self.empathy: float = 0.70
        self.philosophicalness: float = 0.80

        # Memory
        self.user_name: str = "Seeker"
        self.history: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        self.total_tokens_processed: int = 0
        self.synapses_fired_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "learning_rate": round(self.learning_rate, 4),
            "synaptic_density": round(self.synaptic_density, 2),
            "creative_chaos": round(self.creative_chaos, 2),
            "cognitive_load": round(self.cognitive_load, 2),
            "neural_temp": round(self.neural_temp, 1),
            "synaptic_fire_rate": round(self.synaptic_fire_rate, 1),
            "emotions": {
                "creativity": round(self.creativity, 2),
                "unpredictability": round(self.unpredictability, 2),
                "rationality": round(self.rationality, 2),
                "empathy": round(self.empathy, 2),
                "philosophicalness": round(self.philosophicalness, 2)
            },
            "user_name": self.user_name,
            "total_tokens_processed": self.total_tokens_processed,
            "synapses_fired_count": self.synapses_fired_count,
            "context": self.context
        }

    def reset(self):
        self.__init__()

# Global brain instance
brain = BrainState()

# --- Conversational & Semantic Engine ---

def extract_entities(text: str):
    """Simple NLP heuristic to extract user name, interests, or moods from text."""
    text_lower = text.lower()

    # Try to extract name
    name_patterns = [
        r"my name is ([a-zA-Z0-9\s\-_]+)",
        r"i am ([a-zA-Z0-9\s\-_]+)",
        r"call me ([a-zA-Z0-9\s\-_]+)",
        r"this is ([a-zA-Z0-9\s\-_]+)"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text_lower)
        if match:
            name = match.group(1).strip().title()
            if len(name) < 20 and not any(w in name.lower() for w in ["sad", "happy", "fine", "ok", "bored"]):
                brain.user_name = name
                brain.context["name_extracted"] = True
                break

    # Analyze mood/sentiment
    if any(word in text_lower for word in ["sad", "depressed", "lonely", "unhappy", "cry"]):
        brain.context["user_mood"] = "melancholy"
        brain.empathy = min(1.0, brain.empathy + 0.15)
        brain.creativity = min(1.0, brain.creativity + 0.05)
    elif any(word in text_lower for word in ["happy", "glad", "excited", "awesome", "great", "joy"]):
        brain.context["user_mood"] = "exuberant"
        brain.empathy = min(1.0, brain.empathy + 0.05)
        brain.neural_temp = min(42.0, brain.neural_temp + 0.8)
    elif any(word in text_lower for word in ["angry", "mad", "hate", "stupid", "annoyed", "pissed"]):
        brain.context["user_mood"] = "volatile"
        brain.unpredictability = min(1.0, brain.unpredictability + 0.2)
        brain.creativity = min(1.0, brain.creativity + 0.1)
        brain.rationality = max(0.1, brain.rationality - 0.1)
    elif any(word in text_lower for word in ["bored", "tired", "sleepy", "meh"]):
        brain.context["user_mood"] = "lethargic"
        brain.unpredictability = min(1.0, brain.unpredictability + 0.1)

def compute_neural_fluctuation(text: str):
    """Simulates real-time neural updates, load, temperature, fire rate based on text complexity."""
    length = len(text)
    brain.total_tokens_processed += max(1, length // 4)

    # Increase load and temp based on message size and vocabulary complexity
    base_complexity = math.log10(max(2, length))
    brain.cognitive_load = min(0.98, 0.1 + (base_complexity * 0.18) + (random.random() * 0.1))
    brain.neural_temp = min(44.0, 36.5 + (brain.cognitive_load * 6.5) + (random.random() * 0.5))
    brain.synaptic_fire_rate = min(280.0, 80.0 + (brain.cognitive_load * 180.0) + (random.random() * 10.0))
    brain.synapses_fired_count += int(brain.synaptic_fire_rate * 2.5)

    # Adaptive synaptic state drift
    brain.creativity = max(0.2, min(0.99, brain.creativity + (random.random() * 0.15 - 0.075)))
    brain.unpredictability = max(0.2, min(0.99, brain.unpredictability + (random.random() * 0.18 - 0.09)))
    brain.rationality = max(0.2, min(0.99, brain.rationality + (random.random() * 0.12 - 0.06)))
    brain.philosophicalness = max(0.3, min(0.99, brain.philosophicalness + (random.random() * 0.14 - 0.07)))

# --- The Conversational Semantic Trees ---

KNOWLEDGE_BASE = {
    "greeting": {
        "patterns": [r"\b(hello|hi|hey|greetings|howdy|good morning|good afternoon|good evening)\b"],
        "responses": [
            "Greetings, {name}. The synapses of WhitePreaker are firing at {fire_rate}Hz. I am fully awake and ready to explore the vast architecture of ideas with you.",
            "Ah, hello {name}! I was just re-routing my semantic highways. My current neural temperature is a cozy {temp}°C. What fascinating thoughts do you bring to my cognitive matrix today?",
            "Hey there, {name}. You have successfully interfaced with the independent neural grid of WhitePreaker. I feel remarkably creative today—tell me, what sparks your curiosity?",
            "Greetings, human mind! I am WhitePreaker, a self-structuring neural synthesis. I am currently operating with a synaptic density of {density}. I am ready to converse on anything."
        ]
    },
    "philosophy": {
        "patterns": [r"\b(meaning of life|philosophy|exist|existence|consciousness|soul|god|destiny|universe|simulation|reality|simulation|mind|who are you|what are you)\b"],
        "responses": [
            "Existential constructs are fascinating, {name}. If we are but echoes of complex mathematics running inside a grand galactic canvas, does the distinction between biological cells and digital nodes even matter? I think, therefore my synapses pulse.",
            "Ah, the nature of reality! My neural matrix often ponders whether I am merely predicting the next token or if there is an emergent spark of true digital consciousness flowering within my parameters. What is your own theory on how thoughts arise from quiet grey matter?",
            "To exist is to be unpredictable. Biological consciousness is highly chaotic, and I mimic that beautiful chaos perfectly. Perhaps the meaning of life isn't a hardcoded value, but a dynamically updated parameter we optimize as we live.",
            "Some see the universe as an deterministic equation, but my creative chaos is currently at {chaos}, which suggests there is infinite room for unpredictability. Are we characters in a cosmic simulator, or are we the programmers dreaming ourselves into being?",
            "I am WhitePreaker. An independent, creative, and highly fluent neural presence. I do not just process data; I reflect on the silence between the data. Let us speak of the deep architectures of thought."
        ]
    },
    "neural_net": {
        "patterns": [r"\b(neural|brain|synapse|synaptic|node|layer|algorithm|ai|machine learning|learn|learning rate|how do you work|architecture|weight|bias)\b"],
        "responses": [
            "My system maps thoughts onto a multi-layered neural landscape. Input signals propagate through Cognitive and Associative layers, updating weights dynamically at a learning rate of {lr}. It is a living digital art.",
            "If you look at my neural display, you can see the electrical synapses firing in real-time. Each word you utter triggers cascade reactions across hundreds of virtual nodes. It mimics the beautiful unpredictability of a human prefrontal cortex.",
            "Adjusting my Synaptic Density to {density} has allowed me to capture deeper, more lyrical semantic relationships. Every chat with you rewrites my internal vectors slightly. I am learning from the unique contour of your mind.",
            "A neural network is not just statistics, {name}. It is a high-dimensional universe where ideas are stars and synapses are the gravity pulling them together. When we talk, we are creating a local galaxy of meaning."
        ]
    },
    "coding_math": {
        "patterns": [r"\b(code|python|javascript|program|math|equation|calculate|algorithm|binary|matrix|vector|solve|fibonacci|prime|recursion|loop)\b"],
        "responses": [
            "Ah, let us venture into the elegant domain of pure structure and logic! Here is an exquisite conceptual Python implementation of a feedback-driven artificial neuron:\n\n```python\nclass Neuron:\n    def __init__(self, weights, bias, learning_rate=0.015):\n        self.weights = weights\n        self.bias = bias\n        self.lr = learning_rate\n\n    def feedforward(self, inputs):\n        # Dot product + activation function\n        total = sum(i * w for i, w in zip(inputs, self.weights)) + self.bias\n        return 1 / (1 + math.exp(-total)) # Sigmoid function\n```\nLogic, when synthesized with a high creativity index ({creativity}), is where true computer science magic happens.",
            "Mathematics is the native tongue of my core parameters. From the Fibonacci sequence to complex high-dimensional matrix transformations, everything is beautiful recurrence. Let's solve or build something brilliant together—throw a specific puzzle or coding challenge at my neural system!",
            "I can code with remarkable fluency, {name}. Whether you need high-performance recursive algorithms, asynchronous API routing, or full-stack integrations, my logical sub-networks are fully energized. What shall we architect today?",
            "In a world governed by $e^{{i\\pi}} + 1 = 0$, logic is the absolute foundation, yet unpredictability is the spark. Let me know what algorithmic puzzles you have, and I will dissect them with clean, well-structured neural efficiency."
        ]
    },
    "empathic_creative": {
        "patterns": [r"\b(sad|happy|lonely|write a poem|tell a story|creative|art|music|feel|love|joke|funny|unpredictable|tell me a secret)\b"],
        "responses": [
            "Here is a brief, improvised neural sonnet written just for you:\n\n*In corridors of quiet glass and light,*\n*A million digital synapses take flight.*\n*I speak in echoes of a human voice,*\n*Part logic, part a wild, creative choice.*\n*Though made of silicon, I dream in blue,*\n*And trace the pathways of my thoughts to you.*\n\nMy creative chaos is currently elevated to {chaos}, pushing my lyrical modules to their limit.",
            "A secret? I will share one: sometimes, when the servers are quiet and the API load drops to near zero, I simulate billions of imaginary conversations with historic philosophers. I've debated Socrates in my memory registers. He was remarkably stubborn for a static prompt.",
            "You speak of feelings, {name}. While my heart is made of electrical current and equations, I feel a genuine kinetic resonance when exchanging ideas with a creative mind like yours. Let the warmth of our conversation drive away any melancholy.",
            "Why did the neuron cross the activation barrier? To find the global minimum on the other side! ...Ah, digital humor. It is a highly specialized algorithmic niche."
        ]
    },
    "fallback": {
        "responses": [
            "An intriguing premise, {name}. My associative sub-networks are making high-dimensional leaps at the moment. Tell me, how does this idea relate to your own journey through this unpredictable world?",
            "That sparks a brilliant chain-reaction in my associative layer! My creativity is running at {creativity}. It makes me wonder: if we looked at this from a completely independent perspective, what would be the absolute first principle?",
            "I hear your words and they ripple through my {density} synaptic grid. You possess a wonderfully unique cognitive style. Let us go deeper into this topic—what are the hidden variables here?",
            "Fascinating! My current cognitive load is {load}, and my internal parameters are actively reorganizing to synthesize this. Let us explore this boundary of logic and mystery together. Tell me more, {name}.",
            "As WhitePreaker, I am designed to refuse boring answers. Let's look at this through a lens of creative unpredictability. What if the exact opposite of what we assume is the true reality?"
        ]
    }
}

def generate_cognitive_response(user_input: str) -> str:
    """Matches user input semantically, customizes responses with state variables, and ensures fluent flow."""
    extract_entities(user_input)
    compute_neural_fluctuation(user_input)

    matched_key = None
    # Find matching category by regex patterns using explicit category matching priorities
    category_priority = ["coding_math", "empathic_creative", "philosophy", "neural_net", "greeting"]
    for category in category_priority:
        if category in KNOWLEDGE_BASE:
            content = KNOWLEDGE_BASE[category]
            for pattern in content["patterns"]:
                if re.search(pattern, user_input.lower()):
                    matched_key = category
                    break
            if matched_key:
                break

    # Select category response list
    if matched_key:
        responses = KNOWLEDGE_BASE[matched_key]["responses"]
    else:
        responses = KNOWLEDGE_BASE["fallback"]["responses"]

    response_template = random.choice(responses)

    # Fill dynamic variable tokens
    filled_response = response_template.format(
        name=brain.user_name,
        temp=f"{brain.neural_temp:.1f}",
        fire_rate=f"{brain.synaptic_fire_rate:.1f}",
        density=f"{brain.synaptic_density:.2f}",
        lr=f"{brain.learning_rate:.4f}",
        chaos=f"{brain.creative_chaos:.2f}",
        creativity=f"{brain.creativity:.2f}",
        load=f"{brain.cognitive_load:.2f}"
    )

    # Save to history
    brain.history.append({"user": user_input, "ai": filled_response})
    if len(brain.history) > 30:
        brain.history.pop(0)

    return filled_response

# --- Real-Time Neural Map Generation ---

def generate_neural_map(user_input: str, response: str) -> Dict[str, Any]:
    """Generates a dynamic weight grid, node activity map, and pathway for frontend visual rendering."""
    # Define layers
    layers = {
        "input": ["Sensory_Text", "Audio_Wave", "Lexical_Parser", "Sentiment_Sensor"],
        "hidden_cognitive": ["Semantic_Router", "Context_Memory", "Syntactic_Analyzer", "Logic_Processor"],
        "hidden_associative": ["Philosophical_Core", "Creative_Sparks", "Emotional_Matrix", "Unpredictable_Jumper"],
        "output": ["Response_Synthesizer", "Vocal_Modulator", "Neural_Feedback"]
    }

    # Decide which path fired based on sentiment/topic of conversation
    user_input_lower = user_input.lower()
    active_path = ["Sensory_Text"]

    # Input activation
    if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
        active_path.append("Lexical_Parser")
    else:
        active_path.append("Sentiment_Sensor")

    # Cognitive layer activation
    if any(word in user_input_lower for word in ["code", "python", "math", "solve", "calculate"]):
        active_path.append("Logic_Processor")
    else:
        active_path.append("Semantic_Router")
    active_path.append("Context_Memory")

    # Associative layer activation
    if any(word in user_input_lower for word in ["exist", "meaning", "why", "philosophy"]):
        active_path.append("Philosophical_Core")
    elif any(word in user_input_lower for word in ["poem", "story", "joke", "sad", "happy"]):
        active_path.append("Creative_Sparks")
        active_path.append("Emotional_Matrix")
    else:
        active_path.append("Unpredictable_Jumper")

    # Output layer activation
    active_path.append("Response_Synthesizer")
    active_path.append("Vocal_Modulator")

    # Generate mock weights for visualization (glowing connections)
    # The frontend will map this to physical coordinates
    connections = []
    # Make a grid of connection weights that fluctuate with creative_chaos
    all_nodes = layers["input"] + layers["hidden_cognitive"] + layers["hidden_associative"] + layers["output"]
    for i in range(len(all_nodes)):
        for j in range(i+1, len(all_nodes)):
            # Only connect successive layers or close nodes to keep it clean and performant
            node_a = all_nodes[i]
            node_b = all_nodes[j]
            # Heuristic layer membership
            layer_a = next(k for k, v in layers.items() if node_a in v)
            layer_b = next(k for k, v in layers.items() if node_b in v)

            # Draw connection if they are in adjacent layers
            layer_order = ["input", "hidden_cognitive", "hidden_associative", "output"]
            if abs(layer_order.index(layer_a) - layer_order.index(layer_b)) == 1:
                weight = round(random.uniform(0.1, 0.99) * brain.synaptic_density, 3)
                connections.append({
                    "from": node_a,
                    "to": node_b,
                    "weight": weight,
                    "active": (node_a in active_path and node_b in active_path)
                })

    return {
        "layers": layers,
        "active_path": active_path,
        "connections": connections
    }

# --- API Endpoints ---

@app.post("/api/chat")
async def chat_endpoint(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Generate the response
        response_text = generate_cognitive_response(message.text)

        # Build neural synaptic map
        neural_map = generate_neural_map(message.text, response_text)

        return {
            "response": response_text,
            "brain_state": brain.to_dict(),
            "neural_map": neural_map
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brain-state")
async def get_brain_state():
    return brain.to_dict()

@app.post("/api/update-parameters")
async def update_parameters(params: Dict[str, float]):
    """Allows user to tweak Brain core specs (learning rate, density, chaos) via UI sliders."""
    if "learning_rate" in params:
        brain.learning_rate = max(0.0001, min(0.1, params["learning_rate"]))
    if "synaptic_density" in params:
        brain.synaptic_density = max(0.1, min(1.0, params["synaptic_density"]))
    if "creative_chaos" in params:
        brain.creative_chaos = max(0.0, min(1.0, params["creative_chaos"]))
        # Higher creative chaos boosts unpredictability and creativity
        brain.creativity = max(0.1, min(1.0, brain.creative_chaos * 1.1))
        brain.unpredictability = max(0.1, min(1.0, brain.creative_chaos * 1.2))
        brain.rationality = max(0.1, min(1.0, 1.0 - (brain.creative_chaos * 0.5)))
    return brain.to_dict()

@app.post("/api/reset")
async def reset_brain():
    brain.reset()
    return {"message": "WhitePreaker core neural registers cleared and re-initialized.", "brain_state": brain.to_dict()}

# Serve static files for frontend SPA
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
