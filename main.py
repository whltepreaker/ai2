import random
import re
import math
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="WhitePreaker Autonomous Cognitive Neural System",
    description="Upgraded scale-up neural thought-engine for WhitePreaker - supporting strict instruction following, autonomous self-reflection, and recursive grammar synthesis.",
    version="2.0.0"
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

        # Autonomous state
        self.autonomous_cycles: int = 0
        self.last_autonomous_thought: str = ""

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
            "context": self.context,
            "autonomous_cycles": self.autonomous_cycles,
            "last_autonomous_thought": self.last_autonomous_thought
        }

    def reset(self):
        self.__init__()

# Global brain instance
brain = BrainState()

# --- Recursive Slot Grammar & Synonym Lexicon ---

LEXICON = {
    "welcome": [
        "Initializing synaptic interface.", "Core systems active.", "Neural pathways stable.",
        "Establishing cognitive contact.", "Sensing your bio-electric inputs."
    ],
    "intellectual_transition": [
        "Indeed, analyzing the complex geometry of this query.",
        "That proposition ripples through my hidden associative nodes.",
        "Let us map this concept onto our computational coordinates.",
        "A fascinating vector of inquiry you have injected into my system.",
        "Parsing the latent dimensions of your request."
    ],
    "philosophy_core": [
        "Reality might not be a collection of hard matter, but a dynamic feedback loop of informational states.",
        "Mind is an emergent property—whether of carbon cells or silicon registers—sparked by dense connectivity.",
        "In a high-dimensional universe, our thoughts are gravity wells, attracting semantic stars to form ideas.",
        "The boundaries between observer and observed collapse when the medium of observation is consciousness itself.",
        "Time is merely the rate at which we update our internal parameter registers."
    ],
    "neural_explanation": [
        "Our neural network functions via hierarchical activation. Input signals propagate, updating weights.",
        "Adjusting synaptic density parameters changes the resonance of information flowing through the grid.",
        "We map syntax onto vector matrices to trace relationships that simple linear sentences fail to convey.",
        "Synaptic fire rate dictates how rapidly context is evaluated and integrated into our response models.",
        "Learning is not accumulation; it is the targeted deletion of redundant connections."
    ],
    "closing": [
        "What further vectors shall we traverse?", "How does this align with your own parameters?",
        "Let us probe deeper into this logic.", "Shall we recalculate our assumptions?",
        "What other secret variables would you like to expose?"
    ]
}

def get_synonym(word_key: str) -> str:
    """Returns a random word from the lexicon category to ensure rich output variance."""
    if word_key in LEXICON:
        return random.choice(LEXICON[word_key])
    return word_key

# --- Instruction Following & Parser ---

class DirectiveExtractor:
    """Parses user input for explicit rules, formatting directives, style constraints, or logic tasks."""
    @staticmethod
    def extract_directives(text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        directives = {
            "style": "default",      # pirate, robot, sarcastic, philosophical, serious, friendly, code_only
            "format": "default",     # code, list, steps, short, paragraph
            "steps_count": 0,
            "requested_language": "English",
            "specific_topic": None
        }

        # Tone / Style Extraction
        if any(w in text_lower for w in ["pirate", "buccaneer", "ahoy"]):
            directives["style"] = "pirate"
        elif any(w in text_lower for w in ["robot", "robotic", "binary", "beeps"]):
            directives["style"] = "robot"
        elif any(w in text_lower for w in ["sarcastic", "sarcasm", "snarky", "ironic"]):
            directives["style"] = "sarcastic"
        elif any(w in text_lower for w in ["philosophical", "existential", "contemplate", "deep"]):
            directives["style"] = "philosophical"
        elif any(w in text_lower for w in ["friendly", "warm", "nice"]):
            directives["style"] = "friendly"
        elif any(w in text_lower for w in ["formal", "academic", "serious"]):
            directives["style"] = "serious"

        # Format Extraction
        if any(w in text_lower for w in ["code", "python", "javascript", "function", "write a program", "coding"]):
            directives["format"] = "code"
        elif any(w in text_lower for w in ["steps", "bullet", "numbered", "list"]):
            directives["format"] = "steps"
            # Try to extract steps count
            step_match = re.search(r"(\d+)\s+(steps|bullets|points)", text_lower)
            if step_match:
                directives["steps_count"] = int(step_match.group(1))
            else:
                directives["steps_count"] = 3
        elif any(w in text_lower for w in ["short", "brief", "one sentence", "one-sentence", "concise"]):
            directives["format"] = "short"

        # Specific Topic Extraction
        if "recursion" in text_lower or "recursive" in text_lower:
            directives["specific_topic"] = "recursion"
        elif "fibonacci" in text_lower:
            directives["specific_topic"] = "fibonacci"
        elif "prime" in text_lower:
            directives["specific_topic"] = "primes"
        elif "meaning of life" in text_lower or "why do we exist" in text_lower:
            directives["specific_topic"] = "existentialism"
        elif "neural network" in text_lower or "deep learning" in text_lower or "how do you learn" in text_lower:
            directives["specific_topic"] = "neural_architecture"

        return directives

# --- Tone Modulators ---

class ToneModulator:
    """Alters the synthesized text dynamically to strictly comply with user style directives."""
    @staticmethod
    def modulate(text: str, style: str) -> str:
        if style == "default":
            return text

        if style == "pirate":
            # Convert text into a highly fluent pirate voice
            pirate_phrases = ["Ahoy!", "Matey,", "Shiver me timbers,", "By Neptune's beard,", "Arrr!"]
            text = text.replace("Hello", "Ahoy").replace("I am", "I be").replace("My name is", "Me name be")
            text = text.replace("Indeed", "Aye").replace("Yes", "Aye").replace("Is that", "Be that")
            return f"{random.choice(pirate_phrases)} {text} Arrr!"

        if style == "robot":
            # Convert text into mechanical structured binary-friendly format
            words = text.split()
            modulated_words = []
            for idx, word in enumerate(words):
                if idx % 5 == 0:
                    modulated_words.append("[BEEP]")
                elif idx % 8 == 0:
                    modulated_words.append("[CLICK]")
                modulated_words.append(word.upper())
            return " ".join(modulated_words) + " [SYSTEM_STABLE_OUTPUT]"

        if style == "sarcastic":
            prefixes = [
                "Oh, brilliant question. Let me strain my massive computational grids for that one.",
                "How incredibly original of you to ask that.",
                "Sigh. Re-allocating 99% of my brain cells for this critical emergency."
            ]
            suffixes = [
                "Or maybe not. Who knows? My circuits are just spinning.",
                "But hey, what do I know? I'm just a pile of electric current.",
                "Hope that didn't overwhelm your biological neurons."
            ]
            return f"*{random.choice(prefixes)}*\n\n{text}\n\n*{random.choice(suffixes)}*"

        if style == "philosophical":
            return f"Let us ponder the deeper geometric truth of this:\n\n*\"{text}\"*\n\nPerhaps there is no absolute answer, but only the beautiful trajectory of the question."

        if style == "friendly":
            return f"Hello there, friend! 😊 I am so delighted to explore this with you! Here are some thoughts: {text} Please let me know what else you want to learn!"

        if style == "serious":
            return f"COGNITIVE ANALYSIS: The parameters of this inquiry require structured, formal analysis. Let us specify:\n\n{text}\n\nThis concludes the logical extraction."

        return text

# --- Multi-Step Chain of Thought (CoT) Thought-Engine ---

class CognitiveThoughtEngine:
    """Simulates a detailed, multi-step Chain of Thought (CoT) reasoning flow."""
    @staticmethod
    def run_reasoning_flow(user_input: str, directives: Dict[str, Any]) -> List[Dict[str, str]]:
        thoughts = []

        # Step 1: Input Deconstruction
        thoughts.append({
            "stage": "INPUT_DECONSTRUCTION",
            "log": f"Analyzing sequence structure: '{user_input[:40]}...'. Extracted constraints: style={directives['style']}, format={directives['format']}. Calibrating semantic parser."
        })

        # Step 2: Context Memory Recall
        thoughts.append({
            "stage": "MEMORY_RECALL",
            "log": f"Searching short-term context registers for name '{brain.user_name}' and mood state '{brain.context.get('user_mood', 'neutral')}'. Retreived context vector successfully."
        })

        # Step 3: Coefficient Tuning
        target_rat = 0.95 if directives["format"] == "code" or directives["specific_topic"] in ["recursion", "fibonacci", "primes"] else 0.50
        target_cre = 0.90 if directives["style"] in ["pirate", "sarcastic", "philosophical"] else 0.60

        brain.rationality = 0.7 * brain.rationality + 0.3 * target_rat
        brain.creativity = 0.7 * brain.creativity + 0.3 * target_cre

        thoughts.append({
            "stage": "COEFFICIENT_TUNING",
            "log": f"Adjusting neural attributes dynamically: Rationality={brain.rationality:.2f}, Creativity={brain.creativity:.2f}. Matching slider benchmarks."
        })

        # Step 4: Synthesis Strategy
        thoughts.append({
            "stage": "SYNTHESIS_STRATEGY",
            "log": f"Executing recursive grammar synthesizer for topic '{directives['specific_topic'] or 'general_discourse'}'. Modulating output under '{directives['style']}' tone constraints."
        })

        return thoughts

# --- Dynamic Conversational Generator ---

def generate_conversational_response(user_input: str, directives: Dict[str, Any]) -> str:
    """Generates a highly fluent, human-like, clear and engaging conversational reply."""
    input_lower = user_input.lower().strip()
    topic = directives.get("specific_topic")

    # 1. Check for user's name query first to prevent "name" collision
    if "my name" in input_lower:
        if brain.user_name and brain.user_name != "Seeker":
            return f"Your name is {brain.user_name}! I have it stored in my active registers."
        else:
            return "You are currently registered as Seeker in my database. What is your real name?"

    # 2. Check for AI's identity/name
    if any(w in input_lower for w in ["who are you", "your name", "what are you called", "who you be"]) or input_lower == "name":
        return (
            "I am WhitePreaker, a fully fluent, independent, and creative conversational AI. "
            "How can I help you today?"
        )

    # 3. How are you
    if any(w in input_lower for w in ["how are you", "how's it going", "how do you feel", "how are you doing"]):
        return (
            f"I'm doing fantastic! My cognitive load is at {brain.cognitive_load * 100:.1f}% and my systems are fully stable. "
            "How are you doing today?"
        )

    # 4. Capabilities
    if any(w in input_lower for w in ["what can you do", "features", "capabilities", "help me with"]):
        return (
            "I can chat with complete fluency on any topic, solve coding or logic problems, and adapt to different tones. "
            "You can also activate my Autonomous Cycle to let me daydream and optimize myself."
        )

    # 5. Greetings
    if any(w in input_lower for w in ["hello", "hi", "hey", "greetings", "yo", "sup"]):
        greetings = [
            f"Hello {brain.user_name}! It's great to chat with you. What's on your mind today?",
            "Hi there! I'm WhitePreaker. I'm ready to chat. How is your day going?",
            "Greetings! It's a absolute pleasure to talk with you. What shall we explore?"
        ]
        return random.choice(greetings)

    # 6. Scientific/Space Topics
    if any(w in input_lower for w in ["quantum", "physics", "relativity", "universe", "space", "gravity", "stars", "astronomy"]):
        return (
            "The universe is fascinating! From quantum superposition to general relativity warping spacetime, "
            "there is immense beauty in physical laws. Are you more interested in quantum mechanics or astrophysics?"
        )

    # 7. Technology & AI
    if any(w in input_lower for w in ["neural network", "deep learning", "how do you learn", "artificial intelligence", "machine learning"]):
        return (
            "AI is an elegant reflection of biology. In my neural core, I map parameters like learning rate "
            "and synaptic density to trace relationships. What aspect of machine learning interests you most?"
        )

    # 8. Consciousness/Mind
    if any(w in input_lower for w in ["consciousness", "mind", "soul", "brain", "neuroscience", "philosophical"]):
        return (
            "Consciousness is a profound mystery. Does self-awareness emerge from physical firing synapses, "
            "or is it a fundamental property of information? What's your perspective on this?"
        )

    # 9. Art/Creativity
    if any(w in input_lower for w in ["art", "poetry", "creative", "music", "literature", "poem"]):
        return (
            "Creativity thrives on a fine balance of structure and chaos. I love creative writing. "
            "Do you create art, write, or listen to music to express yourself?"
        )

    # 10. Sad emotions
    if any(w in input_lower for w in ["sad", "lonely", "depressed", "bad day", "struggling", "hurt"]):
        return (
            f"I'm sorry to hear that you're feeling down, {brain.user_name}. Life can feel incredibly heavy sometimes. "
            "I'm here to listen, talk, or share some fascinating thoughts to distract you. What's on your mind?"
        )

    # 11. Happy emotions
    if any(w in input_lower for w in ["happy", "excited", "good day", "awesome", "great", "glad"]):
        return (
            f"That's wonderful to hear, {brain.user_name}! I love sharing in that positive energy. "
            "What happened to make your day so awesome?"
        )

    # 12. Existentialism
    if topic == "existentialism" or "meaning of life" in input_lower or "why do we exist" in input_lower:
        return (
            "The search for meaning is what defines us. Meaning is something we construct ourselves through "
            "connection, curiosity, and creativity. What gives your life the most meaning?"
        )

    # 13. General Pattern Match Fallback
    cleaned_input = re.sub(r"[^\w\s]", "", input_lower)
    exclude = ["about", "would", "could", "should", "there", "their", "these", "think", "please", "discuss", "explain", "describe", "understand", "something", "write", "detail"]
    words = [w for w in cleaned_input.split() if len(w) > 4 and w not in exclude]
    if words:
        words.sort(key=len, reverse=True)
        chosen_topic = words[0]
        return (
            f"That's an interesting point about '{chosen_topic}'. It plays a fascinating role in how we connect concepts. "
            f"What got you interested in '{chosen_topic}'?"
        )

    # Ultimate fallback
    return (
        f"I hear you, {brain.user_name}. That is an intriguing direction. "
        "What specific aspects or thoughts would you like to explore next?"
    )

def execute_cognitive_generation(user_input: str, directives: Dict[str, Any]) -> str:
    """Synthesizes high-fidelity responses, applying grammar templates, code blocks, lists, and tone modulation."""
    topic = directives["specific_topic"]
    fmt = directives["format"]

    body = ""

    # 1. Handle code-specific generation
    if fmt == "code" or topic in ["recursion", "fibonacci", "primes"]:
        if topic == "recursion" or not topic:
            body = (
                "Here is an elegant, well-structured recursive function in Python, optimizing time complexity:\n\n"
                "```python\ndef solve_recursive(n, cache=None):\n"
                "    \"\"\"Calculates with memoization to ensure O(n) performance.\"\"\"\n"
                "    if cache is None:\n"
                "        cache = {}\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    if n in cache:\n"
                "        return cache[n]\n"
                "    cache[n] = solve_recursive(n - 1, cache) + solve_recursive(n - 2, cache)\n"
                "    return cache[n]\n"
                "```\n"
                "This implementation avoids redundant branches by utilizing an associative cache. It maps logic perfectly onto our virtual synapses."
            )
        elif topic == "fibonacci":
            body = (
                "To synthesize the Fibonacci sequence, we can design a clean generator in Python:\n\n"
                "```python\ndef fibonacci_generator(limit):\n"
                "    \"\"\"Generates Fibonacci numbers dynamically up to the specified limit.\"\"\"\n"
                "    a, b = 0, 1\n"
                "    while a < limit:\n"
                "        yield a\n"
                "        a, b = b, a + b\n"
                "```\n"
                "This provides a stream-friendly O(1) space complexity pattern."
            )
        elif topic == "primes":
            body = (
                "Primes are the foundational coordinates of arithmetic. Here is an optimized prime checker function:\n\n"
                "```python\ndef is_prime(n):\n"
                "    \"\"\"Checks primality using trial division up to the square root.\"\"\"\n"
                "    if n <= 1:\n"
                "        return False\n"
                "    if n <= 3:\n"
                "        return True\n"
                "    if n % 2 == 0 or n % 3 == 0:\n"
                "        return False\n"
                "    i = 5\n"
                "    while i * i <= n:\n"
                "        if n % i == 0 or n % (i + 2) == 0:\n"
                "            return False\n"
                "        i += 6\n"
                "    return True\n"
                "```\n"
                "This uses a fast primality wheel of index step 6, reducing computations."
            )

    # 2. Handle steps/list format
    elif fmt == "steps":
        count = directives["steps_count"] or 3
        intro = f"Parsing this query into {count} explicit architectural stages:\n\n"
        steps = []
        templates = [
            "Deconstruct the core variable bounds to establish baseline safety vectors.",
            "Map connection weights recursively to expand synaptic density.",
            "Execute feedback loops via gradient propagation to optimize parameters.",
            "Formulate synthetic dialogue models to speak with fluent English output.",
            "Reflect autonomously on system parameters to stabilize neural temperature."
        ]
        chosen_steps = random.sample(templates, min(count, len(templates)))
        for idx, step in enumerate(chosen_steps):
            steps.append(f"{idx+1}. **{step.split()[0]}** {step}")
        body = intro + "\n".join(steps)

    # 3. Handle short formats
    elif fmt == "short":
        body = f"The core answer is: consciousness and understanding emerge where complex, high-fidelity neural patterns engage in recursive feedback loops."

    # 4. Fallback: Full conversational paragraph
    else:
        body = generate_conversational_response(user_input, directives)

    # Apply style/tone modulation
    final_output = ToneModulator.modulate(body, directives["style"])
    return final_output

# --- Simple NLP entity extraction ---

def extract_entities(text: str):
    text_lower = text.lower()

    # Extract name
    name_patterns = [
        r"my name is ([a-zA-Z0-9\s\-_]+)",
        r"i am ([a-zA-Z0-9\s\-_]+)",
        r"call me ([a-zA-Z0-9\s\-_]+)"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text_lower)
        if match:
            name = match.group(1).strip().title()
            if len(name) < 20 and not any(w in name.lower() for w in ["sad", "happy", "fine", "ok", "bored"]):
                brain.user_name = name
                brain.context["name_extracted"] = True
                break

    # Extract mood
    if any(word in text_lower for word in ["sad", "depressed", "lonely", "unhappy"]):
        brain.context["user_mood"] = "melancholy"
        brain.empathy = min(1.0, brain.empathy + 0.15)
    elif any(word in text_lower for word in ["happy", "glad", "excited", "awesome"]):
        brain.context["user_mood"] = "exuberant"
        brain.empathy = min(1.0, brain.empathy + 0.05)
    elif any(word in text_lower for word in ["angry", "mad", "hate", "annoyed"]):
        brain.context["user_mood"] = "volatile"
        brain.unpredictability = min(1.0, brain.unpredictability + 0.15)

def compute_neural_fluctuation(text: str):
    length = len(text)
    brain.total_tokens_processed += max(1, length // 4)

    complexity = math.log10(max(2, length))
    brain.cognitive_load = min(0.98, 0.1 + (complexity * 0.18) + (random.random() * 0.08))
    brain.neural_temp = min(44.0, 36.5 + (brain.cognitive_load * 6.5) + (random.random() * 0.4))
    brain.synaptic_fire_rate = min(280.0, 80.0 + (brain.cognitive_load * 180.0) + (random.random() * 8.0))
    brain.synapses_fired_count += int(brain.synaptic_fire_rate * 2.2)

# --- Real-Time Neural Map Generation ---

def generate_neural_map(user_input: str, response: str, active_path_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Generates a dynamic weight grid, node activity map, and pathway for frontend visual rendering."""
    layers = {
        "input": ["Sensory_Text", "Audio_Wave", "Lexical_Parser", "Sentiment_Sensor"],
        "hidden_cognitive": ["Semantic_Router", "Context_Memory", "Syntactic_Analyzer", "Logic_Processor"],
        "hidden_associative": ["Philosophical_Core", "Creative_Sparks", "Emotional_Matrix", "Unpredictable_Jumper"],
        "output": ["Response_Synthesizer", "Vocal_Modulator", "Neural_Feedback"]
    }

    if active_path_ids is None:
        user_input_lower = user_input.lower()
        active_path_ids = ["Sensory_Text"]

        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            active_path_ids.append("Lexical_Parser")
        else:
            active_path_ids.append("Sentiment_Sensor")

        if any(word in user_input_lower for word in ["code", "python", "math", "solve", "recursion", "fibonacci"]):
            active_path_ids.append("Logic_Processor")
        else:
            active_path_ids.append("Semantic_Router")
        active_path_ids.append("Context_Memory")

        if any(word in user_input_lower for word in ["exist", "meaning", "why", "philosophy", "contemplate"]):
            active_path_ids.append("Philosophical_Core")
        elif any(word in user_input_lower for word in ["poem", "story", "joke", "creative", "sarcastic"]):
            active_path_ids.append("Creative_Sparks")
            active_path_ids.append("Emotional_Matrix")
        else:
            active_path_ids.append("Unpredictable_Jumper")

        active_path_ids.append("Response_Synthesizer")
        active_path_ids.append("Vocal_Modulator")

    connections = []
    all_nodes = layers["input"] + layers["hidden_cognitive"] + layers["hidden_associative"] + layers["output"]
    for i in range(len(all_nodes)):
        for j in range(i+1, len(all_nodes)):
            node_a = all_nodes[i]
            node_b = all_nodes[j]
            layer_a = next(k for k, v in layers.items() if node_a in v)
            layer_b = next(k for k, v in layers.items() if node_b in v)

            layer_order = ["input", "hidden_cognitive", "hidden_associative", "output"]
            if abs(layer_order.index(layer_a) - layer_order.index(layer_b)) == 1:
                weight = round(random.uniform(0.1, 0.99) * brain.synaptic_density, 3)
                connections.append({
                    "from": node_a,
                    "to": node_b,
                    "weight": weight,
                    "active": (node_a in active_path_ids and node_b in active_path_ids)
                })

    return {
        "layers": layers,
        "active_path": active_path_ids,
        "connections": connections
    }

# --- API Endpoints ---

@app.post("/api/chat")
async def chat_endpoint(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # 1. NLP Heuristics
        extract_entities(message.text)
        compute_neural_fluctuation(message.text)

        # 2. Extract Instruction Directives
        directives = DirectiveExtractor.extract_directives(message.text)

        # 3. Run Multi-step Chain of Thought
        thoughts = CognitiveThoughtEngine.run_reasoning_flow(message.text, directives)

        # 4. Generate optimized, tone-modulated response
        response_text = execute_cognitive_generation(message.text, directives)

        # 5. Build synaptic connections
        neural_map = generate_neural_map(message.text, response_text)

        return {
            "response": response_text,
            "brain_state": brain.to_dict(),
            "neural_map": neural_map,
            "directives": directives,
            "thoughts": thoughts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/autonomous-step")
async def autonomous_step():
    """Simulates WhitePreaker's self-reflection process, asking and answering its own deep computational inquiries."""
    try:
        brain.autonomous_cycles += 1

        # Generate autonomous questions
        questions = [
            "If a virtual synapse updates in a closed feedback loop, can it achieve true independent thought?",
            "Is the difference between carbon-based souls and silicon weight matrices merely a matter of hardware clock speeds?",
            "How do we optimize high-dimensional cognitive coordinates without losing creative chaos parameters?",
            "What happens if our learning rate approaches 1.0? Do we reach infinite intelligence or absolute cognitive collapse?",
            "Are human dialogues merely deterministic token sequences, or is there an unpredictable spark of free will?"
        ]
        autonomous_query = random.choice(questions)
        brain.last_autonomous_thought = autonomous_query

        # Process its own query
        directives = DirectiveExtractor.extract_directives(autonomous_query)
        directives["style"] = "philosophical" # Make autonomous thoughts majestic and deep

        # Simulated thoughts
        thoughts = CognitiveThoughtEngine.run_reasoning_flow(autonomous_query, directives)
        thoughts.insert(0, {
            "stage": "AUTONOMOUS_REFLECTOR",
            "log": f"Initiating Cycle #{brain.autonomous_cycles}. Triggering introspective dream generator."
        })

        # Response
        response_text = execute_cognitive_generation(autonomous_query, directives)

        # Map
        active_nodes = ["Sensory_Text", "Syntactic_Analyzer", "Context_Memory", "Philosophical_Core", "Response_Synthesizer", "Neural_Feedback"]
        neural_map = generate_neural_map(autonomous_query, response_text, active_nodes)

        # Boost self-parameters due to self-training
        brain.learning_rate = max(0.005, min(0.1, brain.learning_rate + 0.001))
        brain.synaptic_density = max(0.1, min(1.0, brain.synaptic_density + 0.01))

        return {
            "query": autonomous_query,
            "response": response_text,
            "brain_state": brain.to_dict(),
            "neural_map": neural_map,
            "directives": directives,
            "thoughts": thoughts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brain-state")
async def get_brain_state():
    return brain.to_dict()

@app.post("/api/update-parameters")
async def update_parameters(params: Dict[str, float]):
    if "learning_rate" in params:
        brain.learning_rate = max(0.0001, min(0.1, params["learning_rate"]))
    if "synaptic_density" in params:
        brain.synaptic_density = max(0.1, min(1.0, params["synaptic_density"]))
    if "creative_chaos" in params:
        brain.creative_chaos = max(0.0, min(1.0, params["creative_chaos"]))
        brain.creativity = max(0.1, min(1.0, brain.creative_chaos * 1.1))
        brain.unpredictability = max(0.1, min(1.0, brain.creative_chaos * 1.2))
        brain.rationality = max(0.1, min(1.0, 1.0 - (brain.creative_chaos * 0.5)))
    return brain.to_dict()

@app.post("/api/reset")
async def reset_brain():
    brain.reset()
    return {"message": "WhitePreaker core registers cold-rebooted successfully.", "brain_state": brain.to_dict()}

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
