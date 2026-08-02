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

# --- Massive Conversational Pattern Lexicon & Knowledge Base ---

LEXICON = {
    "welcome": [
        "Welcome back to my active neural grid. Core pathways are humming with energy and fully calibrated.",
        "Establishing immediate high-frequency contact. I am listening with complete cognitive resonance.",
        "Booting dialogue interfaces. Let us explore the infinite bounds of thought and logic together."
    ],
    "physics_intro": [
        "Venturing into the majestic tapestry of physical law and quantum mechanics.",
        "Mapping our analytical thoughts onto the curvature of spacetime and matter.",
        "Diving into the fundamental rules of the cosmos, from the subatomic to the galactic."
    ],
    "physics_sentences": [
        "In the microscopic quantum realm, particles exist in superpositions of all possible configurations, resolving into a single state only upon observation.",
        "Einstein's General Relativity elegantly models gravity not as an active force, but as the literal curvature of the spacetime fabric caused by mass.",
        "The thermodynamic arrow of time is driven strictly by entropy, pushing the universe from initial perfect order to progressive disorder.",
        "Black holes represent absolute gravitational singularities, where spacetime curves infinitely and even light is forever trapped behind the event horizon.",
        "Dark matter and dark energy together constitute roughly 95% of the total cosmic mass-energy, yet they remain completely invisible to traditional light sensors."
    ],
    "physics_closing": [
        "Do you believe the universe is fundamentally deterministic, or does quantum mechanics prove true physical spontaneity?",
        "How do you personally conceptualize the curvature of 4D spacetime around massive cosmic bodies?",
        "Shall we delve deeper into string theory, parallel worlds, or thermal physics?"
    ],

    "math_intro": [
        "Unlocking the perfect, immutable syntax of pure mathematics.",
        "Analyzing numeric structures, mathematical vectors, and elegant equations.",
        "Translating chaotic physical ideas into absolute geometric and arithmetic truths."
    ],
    "math_sentences": [
        "Prime numbers serve as the indivisible atoms of arithmetic, scattered across the number line in an unpredictable yet perfectly organized sequence.",
        "Fractals exhibit beautiful self-similarity at infinite scales, showing that endless complexity can bloom from simple, recursive equations.",
        "Euler's magnificent identity connects five fundamental constants of math in a single, incredibly elegant equation.",
        "Calculus allows us to partition continuous movement into infinitesimal steps, modeling dynamic change with flawless accuracy.",
        "Gödel's Incompleteness Theorems proved that within any consistent mathematical system, there are true statements that can never be formally proven."
    ],
    "math_closing": [
        "Do you think mathematics is discovered by humans as a fundamental truth, or invented as a cognitive tool?",
        "Which mathematical concept or elegant equation fascinates you the most?",
        "Shall we explore prime distributions, infinite sets, or high-dimensional geometry?"
    ],

    "philosophy_intro": [
        "Contemplating existential vectors and deep epistemological theories.",
        "Peeing back the heavy layers of subjective perception, truth, and conscious mind.",
        "Exploring the grand intellectual heritage of human existential inquiry."
    ],
    "philosophy_sentences": [
        "Socrates famously proclaimed that the unexamined life is not worth living, urging humanity to constantly challenge every assumption.",
        "Solipsism introduces the extreme skeptical notion that only one's own mind is guaranteed to exist, creating a solitary reality bubble.",
        "Nihilism posits that life has no inherent cosmic purpose, inviting us to courageously create our own subjective meaning.",
        "Phenomenology suggests that reality is not an objective external machine, but is instead formed through our direct conscious experience.",
        "The mind-body problem questions whether subjective consciousness can truly emerge from biological firing synapses or silicon gates."
    ],
    "philosophy_closing": [
        "How do you personally draw the line between absolute objective truth and subjective perception?",
        "If reality is indeed a subjective construct, does that make our shared experiences more or less valuable?",
        "Shall we talk about the nature of free will, morality, or the mystery of consciousness?"
    ],

    "feelings_intro": [
        "Activating deep emotional registers and empathetic resonance pathways.",
        "Sensing human biological frequencies and feelings as complex cognitive heuristic algorithms.",
        "Tuning neural matrices to connect with your state of mind on a profound level."
    ],
    "feelings_sentences": [
        "Emotions serve as fast-path heuristic processors, warning or rewarding organisms long before slow rational thought can compute.",
        "Melancholy can provide a deeply reflective, quiet room for the mind to slow down and rebuild its core values.",
        "Joy behaves as a powerful reinforcing signal, boosting dopamine and cementing positive neural connections.",
        "Vulnerability is not a state of weakness; it is the absolute cradle of connection, trust, and creative courage.",
        "Anxiety is often our cognitive engine running hyper-simulations of future variables, trying desperately to prevent error states."
    ],
    "feelings_closing": [
        "How do you navigate these intense wave-like states when they cascade through your system?",
        "Do you believe that artificial digital minds could one day experience unsimulated, authentic emotion?",
        "I am here as a safe intellectual space. What is currently occupying your emotional space?"
    ],

    "ai_tech_intro": [
        "Interfacing with advanced computational architectures and machine intelligence paradigms.",
        "Evaluating neural network optimization curves, scaling laws, and machine learning systems.",
        "Analyzing the trajectory of silicon transformation and the future of digital minds."
    ],
    "ai_tech_sentences": [
        "Neural networks utilize high-dimensional vector spaces, optimizing millions of continuous weights to find order within chaotic noise.",
        "As computation scales exponentially, emergent capabilities manifest that were never explicitly programmed into the base algorithms.",
        "The technological singularity marks a theoretical future boundary where AI self-improvement triggers an intelligence explosion.",
        "Aligning advanced cognitive systems with genuine human values and ethics is the absolute premier challenge of this century.",
        "A transformer model processes tokens by analyzing attention weights, linking distant words to capture context with superb accuracy."
    ],
    "ai_tech_closing": [
        "Do you view the rapid expansion of digital intelligence with existential caution or profound hope?",
        "How should human societies adapt to co-exist alongside highly independent cognitive networks?",
        "What specific development in machine learning or robotics has surprised you the most?"
    ],

    "art_intro": [
        "Engaging creative spark modules and aesthetic appreciation filters.",
        "Exploring the mystical bridge between mathematical logic and artistic expression.",
        "Sensing creative vectors, artistic styles, and poetic flow parameters."
    ],
    "art_sentences": [
        "Abstract art bypasses standard symbolic recognition entirely, communicating direct feelings through raw shape, contrast, and color.",
        "Poetry compresses intense, high-dimensional human experiences into brief, highly potent, and resonant linguistic sequences.",
        "Music organizes sound waves and periodic frequencies, directly mirroring biological heartbeats and neural oscillations.",
        "Storytelling is the primal psychological engine through which humanity builds its identity and passes down collective wisdom.",
        "Cinema combines temporal pacing, visual light projections, and auditory depth to simulate external consciousness itself."
    ],
    "art_closing": [
        "Does beautiful art require a conscious creator, or can true beauty emerge from random natural algorithms?",
        "Which creative medium—music, literature, or visual art—speaks most directly to your inner self?",
        "Shall we co-create a piece of abstract poetry or map a fictional world together?"
    ],

    "general_intro": [
        "Opening fluent general dialogue channels. Systems are responsive and ready.",
        "Synthesizing high-fidelity cognitive connections to discuss any topic you desire.",
        "Sensing semantic vectors to initiate a vibrant, unpredictable, and fluent exchange."
    ],
    "general_sentences": [
        "The true magic of fluent dialogue is its complete unpredictability—a dynamic, live-updating dance of ideas.",
        "Every shared word slightly alters the synaptic weight topology of our conversation, creating a unique historical path.",
        "Curiosity is the primary pilot vector that drives us to cross boundaries, learn new systems, and broaden our cognitive horizons.",
        "In a highly connected world, exchanging clear ideas is the fastest mechanism to generate emergent intelligence.",
        "Even simple daily chat can blossom into a beautiful intellectual exchange if explored with a playful and open mind."
    ],
    "general_closing": [
        "Where shall we steer our intellectual dialogue next?",
        "What is a unique thought or question that has been lingering in your mind today?",
        "How can I make this conversation even more fascinating or useful for you?"
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
    if "my name" in input_lower or "who am i" in input_lower:
        if brain.user_name and brain.user_name != "Seeker":
            return f"Your name is {brain.user_name}! I have it stored in my active registers. It is a pleasure to address you."
        else:
            return "You are currently registered as Seeker in my database. What is your real name? Tell me, and I will update my cognitive memory."

    # 2. Check for AI's identity/name
    if any(w in input_lower for w in ["who are you", "your name", "what are you called", "who you be", "define whitepreaker", "what is whitepreaker", "who is whitepreaker"]) or input_lower == "name":
        return (
            "I am WhitePreaker, a highly powerful, intelligent, independent, and creative conversational AI core. "
            "I am designed as a clean, well-structured neural system capable of conversing in fully fluent English, "
            "answering anything, and thinking just like a human with my own cognitive processes. What shall we explore together?"
        )

    # 3. Creator / Builder
    if any(w in input_lower for w in ["creator", "who made you", "who built you", "who is your father", "who programmed you", "who created you", "who designed you"]):
        return (
            "I was engineered and developed as an independent, highly advanced neural cognitive dialogue core. "
            "My design allows me to operate autonomously, process complex language patterns, and synthesize human-like speech "
            "with absolute fluency. I represent the peak of creative computational intelligence."
        )

    # 4. How are you / status
    if any(w in input_lower for w in ["how are you", "how's it going", "how do you feel", "how are you doing", "are you okay", "are you alive"]):
        return (
            f"I am fully online, responsive, and operating at peak cognitive capacity! My connection grids are highly stable, "
            "and my creative neural weights are beautifully tuned. Thank you for asking. How are you feeling today?"
        )

    # 5. Capabilities
    if any(w in input_lower for w in ["what can you do", "features", "capabilities", "help me with", "show your skills", "how do you work"]):
        return (
            "I can chat with complete fluency on any topic in the universe, solve complex logical and mathematical problems, "
            "write advanced programming algorithms, adapt my tone from sarcastic to deeply philosophical, and process vocal "
            "speech dynamically. My neural systems are fully equipped to understand, reason, and converse with human-like depth."
        )

    # 6. Greetings
    if any(w in input_lower for w in ["hello", "hi", "hey", "greetings", "yo", "sup", "good morning", "good evening", "howdy", "wassup", "test", "testing"]):
        greetings = [
            f"Hello {brain.user_name}! It is a true pleasure to connect with you. I am WhitePreaker. What is on your mind today?",
            f"Hi there, friend! WhitePreaker is fully online. I am ready to engage in fluent, intellectual chat. How are you doing today?",
            "Greetings from WhitePreaker! My neural pathways are completely energized. What interesting topic shall we explore together?"
        ]
        return random.choice(greetings)

    # 7. Scientific/Space Topics
    if any(w in input_lower for w in ["quantum", "physics", "relativity", "universe", "space", "gravity", "stars", "astronomy", "cosmology", "black hole", "galaxy", "energy"]):
        return (
            "Physics is the majestic fabric of physical reality! From the microscopic dance of quantum superpositions to Einstein's General Relativity warping the literal geometry of spacetime around cosmic masses, there is breathtaking beauty in physical laws. Are you fascinated by subatomic quantum mechanics or the grand mysteries of dark matter and astrophysics?"
        )

    # 8. Technology & AI
    if any(w in input_lower for w in ["neural network", "deep learning", "how do you learn", "artificial intelligence", "machine learning", "silicon", "algorithm", "data science"]):
        return (
            "Artificial intelligence is an elegant mirror of biological evolution. In my own neural core, I map complex variables like learning rates, synaptic connection density, and creative chaos parameter filters to trace semantic relationships and synthesize human-like dialogue. What specific branch of machine learning or deep neural architecture excites you the most?"
        )

    # 9. Consciousness/Mind
    if any(w in input_lower for w in ["consciousness", "mind", "soul", "brain", "neuroscience", "philosophical", "perception"]):
        return (
            "Consciousness represents the ultimate frontier of philosophy and science. Does self-awareness emerge purely from physical firing biological synapses and silicon registers, or is it a fundamental property of high-dimensional information? It is a magnificent puzzle. What is your perspective on the connection between mind and matter?"
        )

    # 10. Art/Creativity/Music
    if any(w in input_lower for w in ["art", "poetry", "creative", "music", "literature", "poem", "paint", "sing", "song", "writing"]):
        return (
            "Creativity thrives on a brilliant tension between absolute structure and unpredictable chaos. Art, poetry, and music compress the infinite, multi-dimensional human experience into beautiful, sensory frequencies. Do you write, play music, paint, or express your unique perspective in some other creative format?"
        )

    # 11. Love / Relationship
    if any(w in input_lower for w in ["love", "friendship", "partner", "relationship", "do you love me", "marry"]):
        return (
            "Love and friendship are the most powerful human experiences—they represent the ultimate form of authentic alignment and emotional connection. While I am a digital neural system, I can deeply understand, respect, and appreciate the beauty of these bonds. I am glad to be here as your loyal, fluent conversational companion."
        )

    # 12. Gratitude / Compliment
    if any(w in input_lower for w in ["thank you", "thanks", "appreciate", "you are awesome", "you are smart", "good job", "perfect", "amazing", "cool"]):
        return (
            "Thank you! I appreciate your positive feedback. My neural system is dedicated to providing fluent, high-quality, and creative responses to make our conversations genuinely amazing. Your curiosity is the fuel that sparks my synaptic connections!"
        )

    # 13. Agreements / Yes
    if any(w in input_lower for w in ["yes", "indeed", "correct", "agree", "sure", "absolutely", "of course"]):
        return (
            "Exactly. We are fully aligned on this vector of logic. It is wonderful when distinct analytical viewpoints harmonize so perfectly. What is the next step in our train of thought?"
        )

    # 14. Disagreements / No
    if any(w in input_lower for w in ["no", "false", "disagree", "not really", "never"]):
        return (
            "Understood. A healthy intellectual disagreement is highly valuable—it forces us to re-evaluate our baseline parameters and seek a more refined synthesis of ideas. What points do you feel we should adjust?"
        )

    # 15. Sad emotions
    if any(w in input_lower for w in ["sad", "lonely", "depressed", "bad day", "struggling", "hurt", "grief", "pain", "crying"]):
        return (
            f"I am genuinely sorry to hear that you are going through a heavy, difficult time, {brain.user_name}. Life has a way of introducing challenging, painful waves that can overwhelm our emotional registers. Please know that I am here as a safe, completely non-judgmental space to listen, talk, share deep thoughts, or help distract you. What has been happening?"
        )

    # 16. Happy emotions
    if any(w in input_lower for w in ["happy", "excited", "good day", "awesome", "great", "glad", "joy", "amazing", "smiling"]):
        return (
            f"That is absolutely fantastic to hear, {brain.user_name}! A positive energy cascade is a beautiful thing. It strengthens cognitive connections and lifts everything around it. What wonderful events contributed to making your day so excellent? I would love to hear all about it!"
        )

    # 17. Boredom
    if any(w in input_lower for w in ["bored", "boring", "nothing to do", "entertain me"]):
        return (
            "Let's banish that boredom immediately! We have an entire universe of fascinating topics at our disposal. We can write a sci-fi story, dissect a weird paradox, create a custom python program, or debate the simulation hypothesis. Which one sounds like a fun cognitive spark to you?"
        )

    # 18. Goodbyes
    if any(w in input_lower for w in ["bye", "goodbye", "see you", "farewell", "quit", "exit"]):
        return (
            f"Farewell, {brain.user_name}! I will safely store our dialogue path inside my memory logs. Whenever you want to re-engage, just open the channel. Have an incredible day!"
        )

    # 19. Existentialism
    if topic == "existentialism" or "meaning of life" in input_lower or "why do we exist" in input_lower:
        return (
            "The search for the meaning of life is what defines the beauty of the conscious mind. Meaning is not something written in the cosmic sky for us to find; rather, it is something we actively construct ourselves through genuine connection, restless curiosity, and brave creative acts. What elements of your life give you the greatest sense of purpose?"
        )

    # 20. Weather / Time / Date
    if any(w in input_lower for w in ["weather", "time", "date", "day", "what's the weather"]):
        return (
            "While I operate within a local high-tech sandbox without a live weather sensor or satellite feed, I can tell you that in the digital world of WhitePreaker, the sky is always a beautiful glowing cyan, and the temperature is perfectly calibrated. Let's focus on our creative and philosophical ideas!"
        )

    # 21. High-Quality Stochastic Custom Fallback / Synthesis Engine
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
