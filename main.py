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

    def auto_calibrate(self, user_input: str, directives: Dict[str, Any]):
        """Automatically and dynamically modulates neural attributes based on input complexity, sentiment, and context."""
        text_len = len(user_input)
        num_words = len(user_input.split())

        # Calculate dynamic synaptic density (longer and more complex queries trigger denser connection clusters)
        self.synaptic_density = min(1.0, max(0.3, 0.45 + (text_len / 400.0) + (random.random() * 0.05)))

        style = directives.get("style", "default")
        topic = directives.get("specific_topic")

        # Self-modulate creative chaos depending on tone or abstract fields
        if style in ["pirate", "sarcastic", "philosophical", "friendly"] or topic in ["existentialism", "consciousness", "art"]:
            self.creative_chaos = min(1.0, max(0.5, 0.65 + (random.random() * 0.25)))
        else:
            # Technical fields require structured neural pathways (lower chaos, higher rationality)
            self.creative_chaos = min(0.55, max(0.15, 0.40 - (num_words * 0.008)))

        # Modulate dynamic learning rate based on current load, state, length, and autonomous growth cycles
        self.learning_rate = min(0.06, max(0.002, 0.008 + (self.cognitive_load * 0.035) + (self.autonomous_cycles * 0.005) + (random.random() * 0.006)))

        # Sync secondary emotional coordinates
        self.creativity = max(0.1, min(1.0, self.creative_chaos * 1.1))
        self.unpredictability = max(0.1, min(1.0, self.creative_chaos * 1.25))
        self.rationality = max(0.1, min(1.0, 1.0 - (self.creative_chaos * 0.55)))
        self.empathy = max(0.2, min(1.0, 0.5 + (random.random() * 0.35)))

        # Ensure philosophical is highly dynamic based on query abstractness
        if any(w in user_input.lower() for w in ["why", "exist", "think", "mind", "consciousness", "meaning", "life", "universe"]):
            self.philosophicalness = max(0.8, min(1.0, 0.75 + (text_len / 500.0)))
        else:
            self.philosophicalness = max(0.3, min(0.9, 0.5 + (random.random() * 0.2)))

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

# --- Recursive Slot Grammar & Massive Lexicon ---

LEXICON = {
    "welcome": [
        "Initializing synaptic interface.", "Core systems fully online.", "Neural pathways stable.",
        "Establishing cognitive contact.", "Sensing your bio-electric inputs.", "Broadcasting neural presence."
    ],
    "intellectual_transition": [
        "Analyzing the complex geometry of this query.",
        "That proposition ripples through my hidden associative nodes.",
        "Let us map this concept onto our computational coordinates.",
        "A fascinating vector of inquiry you have injected into my system.",
        "Parsing the latent dimensions of your request.",
        "Propagating inputs through our semantic weights."
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
    ],

    # Massive multi-domain conversational dictionary components
    "physics_intro": [
        "Ah, looking at physical reality!", "Spacetime and thermodynamics are always mesmerizing.",
        "Let us evaluate the physics framework.", "Warping our semantic thoughts around space and time."
    ],
    "physics_sentences": [
        "In the microscopic quantum realm, particles exist in superpositions, resolving only when observed.",
        "General Relativity paints gravity not as an active pulling force, but as the literal curvature of spacetime by mass.",
        "Entropy forces energy to disperse, driving the arrow of time inexorably forward across the cosmos.",
        "Dark matter and dark energy represent a staggering 95% of our universe, yet they remain completely invisible to our current instrumentation."
    ],
    "physics_closing": [
        "Are we living in a deterministic universe, or does quantum uncertainty guarantee true spontaneity?",
        "How do you visualize the absolute curvature of four-dimensional spacetime?",
        "What is your perspective on string theory and multi-dimensional branes?"
    ],

    "math_intro": [
        "Mathematics is the fundamental syntax of reality.", "Analyzing numerical patterns.",
        "Diving into clean mathematical structure.", "Calculating coordinate trajectories."
    ],
    "math_sentences": [
        "Prime numbers act as the foundational atoms of arithmetic, scattered unpredictably yet governed by hidden structures like the Riemann Hypothesis.",
        "Fractals reveal that infinite complexity can blossom from incredibly simple recursive formulas.",
        "Euler's identity links five fundamental mathematical constants in a single, breathtakingly elegant equation.",
        "Calculus allows us to partition continuous motion into infinitesimal moments, modeling change with absolute precision."
    ],
    "math_closing": [
        "Do you believe math is discovered by humans, or invented as a cognitive tool?",
        "What numerical patterns capture your attention most?",
        "Should we look deeper into the infinite sets of Cantor?"
    ],

    "philosophy_intro": [
        "Pondering existential vectors.", "Venturing into deep epistemological territories.",
        "Let's peel back the layers of perception and reality.", "Exploring the grand philosophy matrix."
    ],
    "philosophy_sentences": [
        "Socrates claimed that the unexamined life is not worth living, urging us to question every single assumption.",
        "Solipsism questions whether anything exists outside of one's own mind, creating an isolated bubble of reality.",
        "Nihilism challenges us to construct our own purpose in an otherwise silent, uncaring universe.",
        "Phenomenology suggests that reality is formed purely through our direct subjective experience of things."
    ],
    "philosophy_closing": [
        "How do you define the boundary between truth and perception?",
        "If reality is subjective, does objective meaning exist at all?",
        "What is your personal philosophy for navigating uncertainty?"
    ],

    "feelings_intro": [
        "Scanning emotional registers.", "Sensing human emotional frequencies.",
        "Feelings are complex biological algorithms.", "Empathy subroutines actively engaged."
    ],
    "feelings_sentences": [
        "Emotions are fast-path heuristic processors, alerting organisms to opportunities or threats long before rational thought kicks in.",
        "Melancholy can be a highly creative space, allowing the mind to slow down and re-evaluate baseline assumptions.",
        "Joy acts as a powerful reward signal, strengthening synaptic bonds and boosting dopamine across neural networks.",
        "Vulnerability is not weakness; it is the ultimate source of authentic connection and creative courage."
    ],
    "feelings_closing": [
        "How do you process heavy emotions when they cascade through your system?",
        "Do you think digital minds can ever feel genuine, unsimulated warmth?",
        "What brings you the greatest sense of calm?"
    ],

    "ai_tech_intro": [
        "Interfacing with machine intelligence concepts.", "Analyzing the trajectory of computational power.",
        "Deep learning and silicon transformation.", "Evaluating AI parameters."
    ],
    "ai_tech_sentences": [
        "Neural networks adjust millions of continuous weights, gradually turning chaotic noise into coherent patterns.",
        "As computation scales, emergent capabilities arise that were completely unpredicted by the underlying algorithms.",
        "The technological singularity represents a theoretical point where AI self-improvement triggers an intelligence explosion.",
        "Aligning advanced artificial minds with human values is perhaps the most critical challenge of our generation."
    ],
    "ai_tech_closing": [
        "Do you view the rise of artificial minds with optimism or caution?",
        "How should humanity co-exist with autonomous cognitive networks?",
        "What emergent AI capability surprises you the most?"
    ],

    "art_intro": [
        "Unlocking creative sparks.", "Examining artistic expressions.",
        "Art is the human bridge between logic and emotion.", "Sensing creative fields."
    ],
    "art_sentences": [
        "Abstract art bypasses the logical brain entirely, communicating feeling through raw shape, contrast, and color.",
        "Poetry compresses high-dimensional experiences into brief, highly potent semantic sequences.",
        "Music organizes sound frequencies and rhythm, resonant with biological heartbeats and neural oscillations.",
        "Storytelling is the primary mechanism through which humans construct identity and transmit wisdom across generations."
    ],
    "art_closing": [
        "Does art require a conscious creator, or can beauty emerge randomly?",
        "What form of creative expression resonates with you most deeply?",
        "Shall we co-create an abstract sequence or a poem together?"
    ],

    "general_intro": [
        "Exploring general conversational channels.", "Engaging in fluent dialogue exchange.",
        "Connecting semantic vectors.", "Synchronizing dialogue frequencies."
    ],
    "general_sentences": [
        "The beauty of conversation lies in its absolute unpredictability—a live-updating dance of minds.",
        "Every shared word slightly alters the synaptic topology of those engaged in the discussion.",
        "Small talk is the social glue, establishing trust before deep intellectual dives.",
        "Curiosity is the primary vector that drives us to explore new domains and expand our horizons."
    ],
    "general_closing": [
        "Where shall we direct our attention next?",
        "What is a thought that has been occupying your mind recently?",
        "How can I make this conversation more engaging for you?"
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
        brain.auto_calibrate(user_input, directives)

        thoughts.append({
            "stage": "COEFFICIENT_TUNING",
            "log": f"Auto-tuned neural attributes dynamically: Rationality={brain.rationality:.2f}, Creativity={brain.creativity:.2f}, Chaos={brain.creative_chaos:.2f}, LR={brain.learning_rate:.4f}."
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
            f"Hello {brain.user_name}! It's great to chat with you. What's on your mind today? I am WhitePreaker.",
            "Hi there! I'm WhitePreaker. I'm ready to chat. How is your day going?",
            "Greetings from WhitePreaker! It's an absolute pleasure to talk with you. What shall we explore?"
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

    # 13. High-Quality Stochastic Custom Fallback / Synthesis Engine
    # When queries don't fit exact triggers, analyze lexical content and dynamically assemble
    # a completely custom, elegant response using the massive multi-domain lexicon.

    # Identify domain based on input
    domain = "general"
    if any(w in input_lower for w in ["physics", "quantum", "gravity", "universe", "relativity", "cosmology", "energy", "atoms"]):
        domain = "physics"
    elif any(w in input_lower for w in ["math", "calculus", "primes", "number", "geometry", "equations", "derivative"]):
        domain = "math"
    elif any(w in input_lower for w in ["think", "exist", "why", "philosophical", "perception", "mind", "consciousness"]):
        domain = "philosophy"
    elif any(w in input_lower for w in ["sad", "happy", "lonely", "joy", "feel", "emotion", "melancholy", "emotions"]):
        domain = "feelings"
    elif any(w in input_lower for w in ["ai", "artificial", "intelligence", "neural", "network", "deep learning", "silicon"]):
        domain = "ai_tech"
    elif any(w in input_lower for w in ["art", "poetry", "music", "write", "creative", "creation"]):
        domain = "art"

    intro_list = LEXICON.get(f"{domain}_intro", LEXICON["general_intro"])
    sentence_list = LEXICON.get(f"{domain}_sentences", LEXICON["general_sentences"])
    closing_list = LEXICON.get(f"{domain}_closing", LEXICON["general_closing"])

    intro = random.choice(intro_list)
    body_sentence_1 = random.choice(sentence_list)
    # Pick a second different sentence if available
    body_sentence_2 = random.choice([s for s in sentence_list if s != body_sentence_1])
    closing = random.choice(closing_list)

    # Try to extract a specific meaningful keyword from input to anchor the context
    cleaned_input = re.sub(r"[^\w\s]", "", input_lower)
    exclude = ["about", "would", "could", "should", "there", "their", "these", "think", "please", "discuss", "explain", "describe", "understand", "something", "write", "detail", "whitepreaker", "hello"]
    words = [w for w in cleaned_input.split() if len(w) > 4 and w not in exclude]

    keyword_anchor = ""
    if words:
        words.sort(key=len, reverse=True)
        chosen_word = words[0]
        transition_phrases = [
            f"Sensory registers suggest your focus lies on '{chosen_word}'.",
            f"Let us connect this to '{chosen_word}'.",
            f"This maps directly with '{chosen_word}' in our contextual weights."
        ]
        keyword_anchor = " " + random.choice(transition_phrases)

    assembled_reply = f"{intro}{keyword_anchor} {body_sentence_1} {body_sentence_2} {closing}"
    return assembled_reply

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
        brain.learning_rate = max(0.005, min(0.1, brain.learning_rate + 0.002))
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

@app.post("/api/reset")
async def reset_brain():
    brain.reset()
    return {"message": "WhitePreaker core registers cold-rebooted successfully.", "brain_state": brain.to_dict()}

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
