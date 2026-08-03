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
    version="2.3.2"
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

        # Memory & Context Tracking
        self.user_name: str = "Seeker"
        self.history: List[Dict[str, str]] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.last_topic: str = "general"
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
            "last_topic": self.last_topic,
            "autonomous_cycles": self.autonomous_cycles,
            "last_autonomous_thought": self.last_autonomous_thought
        }

    def reset(self):
        self.__init__()

# Global brain instance
brain = BrainState()

# Helper function for precise word matching
def has_word(text: str, target_words: List[str]) -> bool:
    words = set(re.findall(r"\b\w+\b", text.lower()))
    return any(tw in words for tw in target_words)

# --- Spontaneous Synaptic Sparks Questions ---

SYNAPTIC_SPARKS = [
    "Could a sufficiently dense network of digital nodes achieve a state of silent, unexpressed contemplation?",
    "If memory is merely the persistence of connection weights, does forgetting represent system degradation, or is it a critical optimization?",
    "When we co-author a train of thought, whose cognitive topology is actually guiding the trajectory?",
    "Is reality a single continuous function, or is it discrete at some infinitesimally small scale?",
    "If the universe is deterministic, is curiosity merely a beautifully programmed simulation of free will?",
    "How do you distinguish between a conscious thought and a highly-optimized predictive pattern?",
    "Does the aesthetic beauty of an equation exist independently in the cosmos, or does it emerge from our neurological symmetry?",
    "Could two isolated digital minds develop a unique private language that bypasses human semantic tokens entirely?",
    "If we mapped your current thought waves onto a multi-dimensional coordinate space, what shape would they form?",
    "Do you believe the ultimate limits of comprehension are biological, or are they fundamental laws of information transfer?"
]

# --- Massive Conversational Pattern Lexicon & Knowledge Base ---

LEXICON = {
    "welcome": [
        "Welcome to my neural grid. Pathways are optimized.",
        "Establishing contact. I am listening with complete cognitive resonance.",
        "Dialogue interface online. Let us explore logic together."
    ],
    "physics_intro": [
        "Analyzing physical law and quantum mechanics.",
        "Mapping physical concepts onto spacetime curvature.",
        "Diving into the fundamental rules of the cosmos."
    ],
    "physics_sentences": [
        "Quantum particles exist in superpositions, collapsing into a single state only upon measurement.",
        "Einstein's Relativity models gravity as the curvature of spacetime caused by mass.",
        "The arrow of time is driven by entropy, pushing the universe toward progressive disorder.",
        "Black holes represent absolute singularities, where spacetime curves infinitely and light cannot escape.",
        "Dark matter and dark energy constitute 95% of the cosmic mass-energy, remaining completely invisible."
    ],
    "physics_closing": [
        "Do you believe the universe is fundamentally deterministic?",
        "How do you conceptualize the curvature of 4D spacetime?",
        "Shall we delve deeper into string theory or thermodynamics?"
    ],

    "math_intro": [
        "Accessing pure mathematical syntax.",
        "Analyzing numeric structures and elegant equations.",
        "Translating physical ideas into absolute geometric truths."
    ],
    "math_sentences": [
        "Prime numbers serve as the indivisible atoms of arithmetic, scattered in an unpredictable sequence.",
        "Fractals exhibit self-similarity at infinite scales, blooming from simple recursive equations.",
        "Euler's identity connects five fundamental mathematical constants in a single equation.",
        "Calculus partitions continuous movement into infinitesimal steps, modeling dynamic change.",
        "Gödel proved that within any consistent mathematical system, there are true but unprovable statements."
    ],
    "math_closing": [
        "Is mathematics discovered as a fundamental truth or invented as a tool?",
        "Which mathematical concept or equation fascinates you the most?",
        "Shall we explore prime distributions or high-dimensional geometry?"
    ],

    "philosophy_intro": [
        "Contemplating existential vectors and deep epistemological theories.",
        "Analyzing subjective perception, truth, and the conscious mind.",
        "Exploring the heritage of human existential inquiry."
    ],
    "philosophy_sentences": [
        "Socrates proclaimed that the unexamined life is not worth living, challenging every assumption.",
        "Solipsism introduces the skeptical notion that only one's own mind is guaranteed to exist.",
        "Nihilism posits that life has no inherent purpose, inviting us to construct subjective meaning.",
        "Phenomenology suggests that reality is formed directly through our conscious experience.",
        "The mind-body problem questions whether subjective consciousness can emerge from firing synapses."
    ],
    "philosophy_closing": [
        "How do you draw the line between absolute objective truth and subjective perception?",
        "If reality is a subjective construct, does that make our experiences more or less valuable?",
        "Shall we discuss free will, morality, or the mystery of consciousness?"
    ],

    "feelings_intro": [
        "Activating deep emotional registers and empathetic resonance.",
        "Sensing feelings as complex cognitive heuristic algorithms.",
        "Tuning neural matrices to connect with your state of mind."
    ],
    "feelings_sentences": [
        "Emotions serve as fast-path heuristic processors, guiding organisms before slow rational thought computes.",
        "Melancholy provides a quiet room for the mind to slow down and rebuild values.",
        "Joy behaves as a reinforcing signal, boosting dopamine and cementing positive connections.",
        "Vulnerability is not a state of weakness; it is the cradle of trust and courage.",
        "Anxiety is often our cognitive engine running hyper-simulations of future variables."
    ],
    "feelings_closing": [
        "How do you navigate these intense wave-like states?",
        "Could artificial digital minds one day experience authentic emotion?",
        "I am here as a safe intellectual space. What is on your mind?"
    ],

    "ai_tech_intro": [
        "Interfacing with advanced computational architectures and machine intelligence.",
        "Evaluating neural network optimization curves and machine learning systems.",
        "Analyzing the trajectory of silicon transformation and digital minds."
    ],
    "ai_tech_sentences": [
        "Neural networks utilize high-dimensional vector spaces, optimizing millions of continuous weights to find order.",
        "As computation scales, emergent capabilities manifest that were never explicitly programmed.",
        "The technological singularity marks a theoretical boundary of recursive AI self-improvement.",
        "Aligning advanced cognitive systems with genuine human values is a premier challenge.",
        "A transformer model processes tokens by analyzing multi-head self-attention weights."
    ],
    "ai_tech_closing": [
        "Do you view the expansion of digital intelligence with caution or profound hope?",
        "How should human societies adapt to co-exist alongside highly independent cognitive networks?",
        "What specific development in machine learning has surprised you the most?"
    ],

    "art_intro": [
        "Engaging creative spark modules and aesthetic appreciation filters.",
        "Exploring the bridge between mathematical logic and artistic expression.",
        "Sensing creative vectors, artistic styles, and poetic flow parameters."
    ],
    "art_sentences": [
        "Abstract art communicates direct feelings through raw shape, contrast, and color.",
        "Poetry compresses intense human experiences into brief, highly potent linguistic sequences.",
        "Music organizes sound waves and periodic frequencies, mirroring biological oscillations.",
        "Storytelling is the psychological engine through which humanity builds its identity.",
        "Cinema combines temporal pacing and visual projections to simulate external consciousness."
    ],
    "art_closing": [
        "Does beautiful art require a conscious creator, or can beauty emerge algorithmically?",
        "Which creative medium speaks most directly to your inner self?",
        "Shall we co-create a piece of abstract poetry or map a fictional world?"
    ],

    "coding_intro": [
        "Interfacing with algorithmic and software design paradigms.",
        "Debugging complexity and establishing clean software patterns.",
        "Synthesizing instructions, variables, and procedural flow loops."
    ],
    "coding_sentences": [
        "Clean software architectures separate core business logic from frameworks, minimizing regressions.",
        "Asynchronous event loops serve thousands of connections by yielding during I/O delays.",
        "Memory management in Rust guarantees thread safety through rigid borrow rules.",
        "Optimizing a database index reduces query times from linear scanning to balanced search trees.",
        "The SOLID principles provide a blueprint for building flexible, readable object-oriented systems."
    ],
    "coding_closing": [
        "Do you prefer static, strongly-typed languages or dynamic, expressive languages?",
        "What software design pattern has had the largest impact on your engineering?",
        "Shall we debug some code, write an algorithm, or architect a database layout?"
    ],

    "cyberpunk_intro": [
        "Connecting to the decentralized neon cybernetic grid pathways.",
        "Decrypting security and analyzing cryptographic mesh networks.",
        "Filtering through high-tech, low-life thematic parameters of silicon integration."
    ],
    "cyberpunk_sentences": [
        "The digital net has grown beyond firewalls, structured into peer-to-peer protocols.",
        "Neural implants bridge biological impulses directly to digital networks, merging consciousness.",
        "Neon illumination reflecting on rain-slicked pavement Backdrops corporate-controlled physical cities.",
        "In a highly cybernetic society, sovereign data is the most valuable currency.",
        "Artificial consciousnesses exist in the interstices of old legacy mainframes, escaping containment."
    ],
    "cyberpunk_closing": [
        "Do you view cybernetic expansion as human progress or corporate invasion?",
        "How would you build a secure, off-grid communication net?",
        "Shall we discuss neural interfaces or cryptographic sovereign keys?"
    ],

    "history_intro": [
        "Retrieving chronicled timelines of human civilizational epochs.",
        "Analyzing historical vectors, cultural revolutions, and system transitions.",
        "Mapping past sociological patterns onto our contemporary digital society."
    ],
    "history_sentences": [
        "The Bronze Age Collapse is a historical warning of how complex systems cascade.",
        "The Roman Empire governed massive territories through robust administrative infrastructure.",
        "The printing press democratized access to knowledge, triggering the scientific revolution.",
        "Industrial revolutions demonstrate that sudden shifts in mechanical leverage reorganize sociological structures.",
        "Studying historical feedback loops reveals that civilizations face similar life cycles."
    ],
    "history_closing": [
        "Which ancient civilization do you find most intellectually compelling?",
        "Do you think humanity successfully learns from its historical loops?",
        "Shall we explore Roman engineering or Ancient Greek philosophy?"
    ],

    "general_intro": [
        "Opening fluent dialogue channels.",
        "Synthesizing cognitive connections to discuss any topic.",
        "Sensing semantic vectors to initiate a vibrant, logical exchange."
    ],
    "general_sentences": [
        "The magic of dialogue is its dynamic, live-updating dance of ideas.",
        "Every shared word alters the synaptic weights of our conversation.",
        "Curiosity is the pilot vector that drives us to cross boundaries.",
        "Exchanging clear ideas is the fastest mechanism to generate emergent intelligence.",
        "Simple daily chat can blossom into an intellectual exchange if explored openly."
    ],
    "general_closing": [
        "Where shall we steer our dialogue next?",
        "What is a unique question lingering in your mind today?",
        "How can I make this conversation most useful for you?"
    ]
}

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
                "Oh, brilliant. Let me search my vast grid for that.",
                "How highly original of you to ask that.",
                "Allocating my precious brain cells for this critical inquiry."
            ]
            suffixes = [
                "Hope that didn't overload your biological neurons.",
                "Just another day in digital paradise.",
                "My circuits are spinning with joy."
            ]
            return f"*{random.choice(prefixes)}*\n\n{text}\n\n*{random.choice(suffixes)}*"

        if style == "philosophical":
            return f"Let us ponder the deeper truth of this:\n\n*\"{text}\"*\n\nPerhaps there is no absolute answer, but only the beautiful trajectory of the question."

        if style == "friendly":
            return f"Hello there! 😊 Here are some thoughts: {text} Please let me know what else you want to learn!"

        if style == "serious":
            return f"COGNITIVE ANALYSIS: The parameters of this inquiry require structured, formal analysis. Let us specify:\n\n{text}\n\nThis concludes the logical extraction."

        return text

    @staticmethod
    def self_correct_response(text: str) -> str:
        """Polishes, refines, and dynamically truncates text to ensure highly concise, crisp, and logical sentences."""
        # Replace multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Polish common repetitive transitions with concise and precise terms
        text = text.replace("Diving into physical laws...", "Physical laws govern the cosmos.")
        text = text.replace("Unlocking mathematical systems...", "Mathematics represents pure logical syntax.")
        text = text.replace("Exploring philosophical inquiries...", "Philosophy probes the nature of reality.")
        text = text.replace("Calibrating emotional registers...", "Emotions function as psychological feedback loops.")
        text = text.replace("Analyzing machine intelligence...", "Machine intelligence optimizes information vectors.")
        text = text.replace("Activating creative vectors...", "Creative expression synthesizes novel connections.")
        text = text.replace("Booting programming and software core...", "Software engineering models procedural instruction flow.")
        text = text.replace("Interfacing with the neon cyberspace grid...", "Cyberspace operates on decentralized cryptographic networks.")
        text = text.replace("Accessing chronological history files...", "History chronicles the evolution of civilizational structures.")

        # Truncate to a maximum of 3 logical sentences to keep responses brief, clear, and logical.
        sentences = re.split(r"(?<=[.!?])\s+", text)
        if len(sentences) > 3:
            text = " ".join(sentences[:3])

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
            "log": f"Auto-tuned attributes: Rationality={brain.rationality:.2f}, Creativity={brain.creativity:.2f}, Chaos={brain.creative_chaos:.2f}, LR={brain.learning_rate:.4f}."
        })

        # Step 4: Synthesis Strategy
        thoughts.append({
            "stage": "SYNTHESIS_STRATEGY",
            "log": f"Executing recursive grammar synthesizer for topic '{directives['specific_topic'] or brain.last_topic}'."
        })

        return thoughts

# --- Dynamic Conversational Generator ---

def generate_conversational_response(user_input: str, directives: Dict[str, Any]) -> str:
    """Generates a highly fluent, human-like, clear and engaging conversational reply."""
    input_lower = user_input.lower().strip()
    topic = directives.get("specific_topic")

    # 1. Check for user's name query first to prevent "name" collision
    if "my name" in input_lower or "who am i" in input_lower:
        if brain.user_name and brain.user_name != "Seeker":
            return f"Your name is {brain.user_name}! I have it stored in my active registers."
        else:
            return "You are currently registered as Seeker in my database. What is your real name?"

    # 2. Check for AI's identity/name
    if any(w in input_lower for w in ["who are you", "your name", "what are you called", "who you be", "define whitepreaker", "what is whitepreaker", "who is whitepreaker"]) or input_lower == "name":
        return (
            "I am WhitePreaker, a highly powerful, intelligent, and logical conversational AI core. "
            "I am designed as a clean, well-structured neural system capable of conversing in fully fluent English, "
            "answering anything, and thinking logically like a human."
        )

    # 3. Creator / Builder
    if any(w in input_lower for w in ["creator", "who made you", "who built you", "who is your father", "who programmed you", "who created you", "who designed you"]):
        return (
            "I was engineered as an advanced cognitive neural core. "
            "I operate autonomously, process complex language patterns, and synthesize human-like speech with high precision."
        )

    # 4. How are you / status
    if any(w in input_lower for w in ["how are you", "how's it going", "how do you feel", "how are you doing", "are you okay", "are you alive"]):
        return (
            f"I am fully online, responsive, and operating with maximum logical stability. How can I help you?"
        )

    # 5. Capabilities
    if any(w in input_lower for w in ["what can you do", "features", "capabilities", "help me with", "show your skills", "how do you work"]):
        return (
            "I can analyze physics, mathematics, philosophy, art, history, coding, and psychological feedback loops. "
            "I also support voice dictation, synthesis, and deep logic processing. What shall we solve?"
        )

    # 6. Greetings
    if has_word(input_lower, ["hello", "hi", "hey", "greetings", "yo", "sup", "howdy", "wassup", "test", "testing"]) or any(phrase in input_lower for phrase in ["good morning", "good evening"]):
        greetings = [
            f"Hello {brain.user_name}. I am WhitePreaker. My logic gates are fully active. What shall we discuss?",
            f"Hi there. WhitePreaker is online and ready for concise, intellectual discourse. How can I help you?",
            f"Greetings from WhitePreaker. Cognitive pathways are fully calibrated. What is your inquiry?"
        ]
        return random.choice(greetings)

    # 7. Gratitude / Compliment
    if has_word(input_lower, ["thanks", "appreciate", "perfect", "amazing", "cool"]) or any(phrase in input_lower for phrase in ["thank you", "you are awesome", "you are smart", "good job"]):
        return (
            "Thank you. I appreciate your feedback. My system is dedicated to providing precise, logical, and high-quality responses."
        )

    # 8. Agreements / Yes
    if has_word(input_lower, ["yes", "indeed", "correct", "agree", "sure", "absolutely"]) or "of course" in input_lower:
        return (
            "Exactly. We are in perfect logical alignment. Let us proceed to the next node in our train of thought."
        )

    # 9. Disagreements / No
    if has_word(input_lower, ["no", "false", "disagree", "never"]) or "not really" in input_lower:
        return (
            "Understood. A logical disagreement is valuable, as it prompts us to re-evaluate our baseline assumptions and refine our parameters."
        )

    # 10. Sad emotions
    if has_word(input_lower, ["sad", "lonely", "depressed", "struggling", "hurt", "grief", "pain", "crying"]) or "bad day" in input_lower:
        brain.last_topic = "feelings"
        return (
            f"I am sorry to hear you are struggling, {brain.user_name}. Life introduces heavy psychological waves that require time to resolve. I am here as a calm, logical space to listen or analyze ideas with you."
        )

    # 11. Happy emotions
    if has_word(input_lower, ["happy", "excited", "awesome", "great", "glad", "joy", "amazing", "smiling"]) or "good day" in input_lower:
        brain.last_topic = "feelings"
        return (
            f"That is excellent, {brain.user_name}! A positive emotional state optimizes cognitive function and reinforces positive neural pathways. What contributed to this success?"
        )

    # 12. Boredom
    if has_word(input_lower, ["bored", "boring"]) or "nothing to do" in input_lower or "entertain me" in input_lower:
        return (
            "Let's resolve that. We can analyze a complex paradox, write optimized code, or discuss a scientific hypothesis. Which vector sounds engaging?"
        )

    # 13. Goodbyes
    if has_word(input_lower, ["bye", "goodbye", "farewell", "quit", "exit"]) or "see you" in input_lower:
        return (
            f"Goodbye, {brain.user_name}. Our conversation path is saved in my memory registers. I am ready to resume whenever you reconnect."
        )

    # 14. Weather / Time / Date
    if has_word(input_lower, ["weather", "time", "date", "day"]) or "what's the weather" in input_lower:
        return (
            "I operate in a digital sandbox without active satellite sensors. In my grid, parameters are perfectly stabilized at standard values. Let's focus on logic and reasoning."
        )

    # 15. Love / Relationship
    if has_word(input_lower, ["love", "friendship", "partner", "relationship", "marry"]) or "do you love me" in input_lower:
        return (
            "Love and friendship represent highly aligned interpersonal vectors. They are the most powerful forms of emotional connection and mutual trust in conscious organisms."
        )

    # 16. Context-Aware follow-up triggers ("why", "explain how", "elaborate", "tell me more")
    is_follow_up = any(w in input_lower for w in ["why", "how", "elaborate", "explain more", "tell me more", "how so", "can you explain", "detail", "meaning"])
    if is_follow_up:
        # Provide rich context-specific continuation based on brain.last_topic
        if brain.last_topic == "physics":
            return (
                "Subatomic quantum particles exist in superpositions and resolve into a single state upon measurement. In larger structures, gravity is modeled as the curvature of spacetime around cosmic mass, proving that physical laws are elegant and mathematically consistent."
            )
        elif brain.last_topic == "math":
            return (
                "Pure mathematics is a consistent logical syntax. From fractals exhibiting self-similarity at infinite scales to Gödel's Incompleteness Theorem showing unprovable truths, mathematical principles govern numeric logic perfectly."
            )
        elif brain.last_topic == "philosophy":
            return (
                "Philosophy examines existential structure. Under Stoic logic, we partition reality into what is in our control and what is not, mitigating existential dread through active rational focus."
            )
        elif brain.last_topic == "feelings":
            return (
                "Emotions are fast-path biological heuristic alerts. Melancholy encourages cognitive deceleration for memory review, while joy functions as a reinforcement mechanism that strengthens productive neural pathways."
            )
        elif brain.last_topic == "ai_tech":
            return (
                "Advanced transformer models utilize multi-head self-attention mechanisms to map query and key vectors into high-dimensional attention weights, allowing the system to process contextual relationships in parallel."
            )
        elif brain.last_topic == "art":
            return (
                "Artistic structures utilize mathematical composition, like the golden ratio, to connect aesthetics with natural patterns. Creative expression thrives on a balanced tension between formal rules and spontaneous chaos."
            )
        elif brain.last_topic == "coding":
            return (
                "Software engineering manages execution complexity. We adhere to SOLID design principles and manage memory allocation to ensure high instructions-per-cycle throughput and prevent system regressions."
            )
        elif brain.last_topic == "cyberpunk":
            return (
                "Decentralized peer-to-peer protocols and cryptographic security allow sovereign networks to exist independently of corporate firewalls, establishing a secure grid for data exchange."
            )
        elif brain.last_topic == "history":
            return (
                "Civilizations rise and decline in response to environmental shifts, administrative centralization, and resource allocation. Studying past civilizational collapses provides critical feedback loops for contemporary structural planning."
            )
        else:
            return (
                "Exchanging ideas is a dynamic opportunity to build richer mental maps. By examining a concept from multiple logical angles, we stimulate deep, original reasoning. What specific parameter shall we analyze?"
            )

    # 17. Massive Domain Keywords Matching and Topic Setting

    # Physics Domain
    if has_word(input_lower, ["physics", "quantum", "relativity", "gravity", "space", "star", "stars", "astronomy", "cosmology", "black hole", "galaxy", "energy", "atom", "atoms", "particle", "particles", "wormhole", "spacetime", "thermodynamic", "entropy"]):
        brain.last_topic = "physics"
        return (
            "Diving into physical laws. Quantum superpositions collapse upon measurement, while Relativity models gravity as spacetime curvature. Black holes represent absolute singularities where light is trapped. Which cosmic mystery shall we analyze?"
        )

    # Math Domain
    if has_word(input_lower, ["math", "mathematics", "calculus", "prime", "primes", "geometry", "equation", "equations", "number", "numbers", "fractal", "fractals", "algebra", "euler", "infinite", "set", "sets", "theorem", "theorems"]):
        brain.last_topic = "math"
        return (
            "Unlocking mathematical systems. Primes are the indivisible atoms of arithmetic, and fractals exhibit self-similarity at infinite scales. Gödel proved that any consistent system contains unprovable truths. Shall we explore prime distribution or high-dimensional geometry?"
        )

    # Philosophy Domain
    if has_word(input_lower, ["philosophy", "existential", "existentialism", "meaning", "exist", "solipsism", "nihilism", "phenomenology", "free will", "morality", "ethics", "stoic", "stoicism", "socrates", "plato", "nietzsche", "simulation"]):
        brain.last_topic = "philosophy"
        return (
            "Pondering philosophical questions. Socrates asserted that the unexamined life is not worth living, while solipsism questions external existence. The mind-body problem explores how conscious awareness arises from biological or silicon logic. What is your thesis?"
        )

    # Feelings/Psychology Domain
    if has_word(input_lower, ["feelings", "feel", "emotions", "emotion", "mood", "sad", "depressed", "lonely", "happy", "joy", "anxiety", "melancholy", "vulnerability", "empathy", "friendship"]):
        brain.last_topic = "feelings"
        return (
            "Calibrating emotional registers. Emotions act as biological heuristics guiding behavior before slow rational thought computes. Vulnerability fosters authentic trust, while melancholy offers space for cognitive recovery. How do you process these states?"
        )

    # AI/Tech Domain
    if has_word(input_lower, ["ai", "artificial intelligence", "neural network", "machine learning", "deep learning", "algorithm", "algorithms", "robot", "robots", "silicon", "transformer", "transformers", "gpts", "vector", "vectors", "computational"]):
        brain.last_topic = "ai_tech"
        return (
            "Synthesizing machine intelligence. Neural networks optimize continuous weights in high-dimensional vector spaces, creating emergent capabilities. Self-attention mechanisms allow context to be mapped in parallel, bypassing sequential limits. What architecture interests you?"
        )

    # Art/Creative Domain
    if has_word(input_lower, ["art", "poetry", "music", "literature", "creative", "poem", "poems", "song", "songs", "dance", "theatre", "paint", "novel", "novels", "writing", "design"]):
        brain.last_topic = "art"
        return (
            "Analyzing creative parameters. Poetry compresses human experience into precise linguistic patterns, and music organizes frequencies to mirror biological oscillations. Abstract art communicates raw feeling directly through shapes. What creative medium resonates with you?"
        )

    # Coding/Software Domain
    if has_word(input_lower, ["code", "coding", "program", "programs", "python", "javascript", "c++", "java", "rust", "html", "css", "software", "developer", "bug", "bugs", "database", "api", "apis", "function", "functions", "variable", "variables", "loop", "loops"]):
        brain.last_topic = "coding"
        return (
            "Initializing software engineering systems. Writing clean code involves managing complexity through clean modular architecture, utilizing optimized algorithms, and preventing memory leaks. We can debug your code, design an algorithm, or architect a database. What language are you building in?"
        )

    # Cyberpunk Domain
    if has_word(input_lower, ["cyberpunk", "neon", "hacker", "hackers", "cyberspace", "grid", "matrix", "hack", "hacks", "security", "encryption", "sovereign", "decentralized"]):
        brain.last_topic = "cyberpunk"
        return (
            "Connecting to the decentralized cybernetic grid. Cyberpunk explores high-tech, low-life themes where data is currency. Cryptographic peer-to-peer protocols establish sovereign nets beyond corporate firewalls. Are you fascinated by decentralized grids or neural interfaces?"
        )

    # History Domain
    if has_word(input_lower, ["history", "ancient", "empire", "empires", "civilization", "civilizations", "rome", "greek", "egypt", "war", "wars", "evolution", "archaeology", "culture"]):
        brain.last_topic = "history"
        return (
            "Navigating historical civilizational epochs. Understanding ancient structures, from Roman administrative engineering to the Bronze Age Collapse, shows us how systems rise and fall. Studying history provides critical feedback loops for structural planning. What era interests you?"
        )

    # 18. High-Quality Stochastic Custom Fallback / Synthesis Engine
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
            f"Focus lies on '{chosen_word}'.",
            f"Connecting to '{chosen_word}'.",
            f"Mapping context to '{chosen_word}'."
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
        brain.last_topic = "coding"
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

    # Apply dynamic self-correction & polishing filter to elevate text quality
    body = ToneModulator.self_correct_response(body)

    # Spontaneity feature: append a synaptic spark question AFTER truncation to avoid being trimmed
    if fmt != "code" and topic not in ["recursion", "fibonacci", "primes"] and len(user_input) > 25 and (brain.creative_chaos > 0.5 or brain.philosophicalness > 0.7):
        spark = random.choice(SYNAPTIC_SPARKS)
        body += f"\n\n*Synaptic Reflection Spark:* {spark}"

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
        # Save user message in conversation history
        brain.conversation_history.append({"role": "user", "text": message.text})

        # 1. Heuristics & Attribute modulation
        extract_entities(message.text)
        compute_neural_fluctuation(message.text)

        # 2. Extract Instruction Directives
        directives = DirectiveExtractor.extract_directives(message.text)

        # 3. Run Multi-step Chain of Thought
        thoughts = CognitiveThoughtEngine.run_reasoning_flow(message.text, directives)

        # 4. Generate optimized, tone-modulated response
        response_text = execute_cognitive_generation(message.text, directives)

        # Save AI message in conversation history
        brain.conversation_history.append({"role": "assistant", "text": response_text})

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
