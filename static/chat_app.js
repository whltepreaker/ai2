/**
 * WhitePreaker Cognitive Chat Engine & Web Speech Integration
 * Bridges API requests, local speech-to-text, fluent text-to-speech, and neural map renderings.
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- Setup Canvas Visualization ---
  const visualizer = new WhitePreakerBrainVis('neuralCanvas');

  // --- UI Elements ---
  const chatForm = document.getElementById('chatForm');
  const userInput = document.getElementById('userInput');
  const chatMessages = document.getElementById('chatMessages');
  const typingIndicator = document.getElementById('typingIndicator');

  // Controls
  const btnListen = document.getElementById('btnListen');
  const listenStatus = document.getElementById('listenStatus');
  const voiceSelect = document.getElementById('voiceSelect');
  const speechRate = document.getElementById('speechRate');
  const rateValue = document.getElementById('rateValue');
  const speechPitch = document.getElementById('speechPitch');
  const pitchValue = document.getElementById('pitchValue');
  const muteToggle = document.getElementById('muteToggle');
  const btnReset = document.getElementById('btnReset');

  // Parameter sliders
  const sliderLr = document.getElementById('sliderLr');
  const valueLr = document.getElementById('valueLr');
  const sliderDensity = document.getElementById('sliderDensity');
  const valueDensity = document.getElementById('valueDensity');
  const sliderChaos = document.getElementById('sliderChaos');
  const valueChaos = document.getElementById('valueChaos');

  // Diagnostics UI
  const brainLoad = document.getElementById('brainLoad');
  const brainLoadText = document.getElementById('brainLoadText');
  const brainFireRate = document.getElementById('brainFireRate');
  const brainTemp = document.getElementById('brainTemp');
  const userNameDisplay = document.getElementById('userNameDisplay');
  const sysLogStream = document.getElementById('sysLogStream');

  // Emotion status bars
  const emoCreativity = document.getElementById('emoCreativity');
  const emoUnpredictability = document.getElementById('emoUnpredictability');
  const emoRationality = document.getElementById('emoRationality');
  const emoEmpathy = document.getElementById('emoEmpathy');
  const emoPhilosophy = document.getElementById('emoPhilosophy');

  // --- Voice Engine Variables ---
  let synthesisVoices = [];
  let ttsEnabled = true;
  let isListening = false;
  let recognitionInstance = null;
  let activeSpeechUtterance = null;

  // Log function to simulated cyber diagnostics console
  function sysLog(message, type = 'INFO') {
    const time = new Date().toISOString().split('T')[1].slice(0, 8);
    let colorClass = 'text-gray-400';
    if (type === 'OK') colorClass = 'text-green-400';
    if (type === 'WARN') colorClass = 'text-yellow-500';
    if (type === 'SYS') colorClass = 'text-cyber-blue font-bold';
    if (type === 'EMO') colorClass = 'text-cyber-magenta';

    const logLine = document.createElement('div');
    logLine.className = `leading-tight mb-1 terminal-log ${colorClass}`;
    logLine.innerHTML = `[${time}] [${type}] ${message}`;
    sysLogStream.appendChild(logLine);
    sysLogStream.scrollTop = sysLogStream.scrollHeight;
  }

  sysLog("WhitePreaker Neural Core booting up...", "SYS");

  // --- Speech Synthesis (Text to Speech) ---
  function initSpeechSynthesis() {
    if (!('speechSynthesis' in window)) {
      sysLog("Speech Synthesis API not supported in this browser environment.", "WARN");
      return;
    }

    const populateVoices = () => {
      synthesisVoices = window.speechSynthesis.getVoices();
      voiceSelect.innerHTML = '';

      // Look for beautiful fluent English voices
      synthesisVoices.forEach((voice, index) => {
        if (voice.lang.startsWith('en')) {
          const option = document.createElement('option');
          option.value = index;
          option.textContent = `${voice.name} (${voice.lang})`;
          if (voice.name.includes('Google') || voice.name.includes('Natural') || voice.name.includes('Samantha') || voice.name.includes('Moira')) {
            option.selected = true;
          }
          voiceSelect.appendChild(option);
        }
      });

      if (voiceSelect.children.length === 0) {
        // Fallback to all voices if no English
        synthesisVoices.forEach((voice, index) => {
          const option = document.createElement('option');
          option.value = index;
          option.textContent = `${voice.name} (${voice.lang})`;
          voiceSelect.appendChild(option);
        });
      }
    };

    populateVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = populateVoices;
    }
  }

  function speakText(text) {
    if (!ttsEnabled || !('speechSynthesis' in window)) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    // Strip markdown before speaking to make it sound completely fluent and natural
    const cleanText = text.replace(/```[\s\S]*?```/g, "[Code block generated, displayed on terminal screen.]")
                          .replace(/[*#`_\-]/g, "")
                          .trim();

    sysLog("Initializing speech synthesizer vocal modulator...", "INFO");
    const utterance = new SpeechSynthesisUtterance(cleanText);

    // Configure voice properties
    if (voiceSelect.value !== '') {
      utterance.voice = synthesisVoices[parseInt(voiceSelect.value)];
    }
    utterance.rate = parseFloat(speechRate.value);
    utterance.pitch = parseFloat(speechPitch.value);

    utterance.onstart = () => {
      sysLog("Vocal feedback module actively broadcasting.", "OK");
      document.getElementById('aiSpeakingBadge').classList.remove('hidden');
    };

    utterance.onend = () => {
      sysLog("Vocal feedback broadcast completed.", "INFO");
      document.getElementById('aiSpeakingBadge').classList.add('hidden');
    };

    utterance.onerror = (e) => {
      sysLog(`Speech Synthesis encountered a transmission quirk: ${e.error}`, "WARN");
      document.getElementById('aiSpeakingBadge').classList.add('hidden');
    };

    activeSpeechUtterance = utterance;
    window.speechSynthesis.speak(utterance);
  }

  // --- Speech Recognition (Speech to Text) ---
  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      sysLog("Speech Recognition (STT) not supported in this browser. Voice input disabled.", "WARN");
      btnListen.classList.add('opacity-50', 'cursor-not-allowed');
      btnListen.disabled = true;
      return;
    }

    recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;
    recognitionInstance.lang = 'en-US';

    recognitionInstance.onstart = () => {
      isListening = true;
      btnListen.classList.add('pulse-glow-magenta', 'bg-red-950', 'border-red-500');
      listenStatus.textContent = "LISTENING...";
      listenStatus.classList.remove('text-cyber-blue');
      listenStatus.classList.add('text-cyber-magenta');
      sysLog("Sensory sound wave recognizer active. Speak clearly into the microphone.", "OK");

      // Start wave bouncing
      document.querySelectorAll('.wave-bar').forEach(bar => {
        bar.classList.add('listening');
      });
    };

    recognitionInstance.onend = () => {
      isListening = false;
      btnListen.classList.remove('pulse-glow-magenta', 'bg-red-950', 'border-red-500');
      listenStatus.textContent = "MIC IDLE";
      listenStatus.classList.remove('text-cyber-magenta');
      listenStatus.classList.add('text-cyber-blue');
      sysLog("Sensory sound wave recognizer returned to sleep.", "INFO");

      // Stop wave bouncing
      document.querySelectorAll('.wave-bar').forEach(bar => {
        bar.classList.remove('listening');
      });
    };

    recognitionInstance.onresult = (event) => {
      const resultText = event.results[0][0].transcript;
      sysLog(`Audio wave parsed: "${resultText}"`, "OK");
      userInput.value = resultText;

      // Auto-submit recognized speech
      submitChatMessage(resultText);
    };

    recognitionInstance.onerror = (event) => {
      sysLog(`Sound wave parser error: ${event.error}`, "WARN");
    };
  }

  // Toggle listening button
  if (btnListen) {
    btnListen.addEventListener('click', () => {
      if (isListening) {
        recognitionInstance.stop();
      } else {
        // Stop any current text-to-speech so it doesn't listen to itself
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        recognitionInstance.start();
      }
    });
  }

  // --- Dynamic Slider Syncing ---
  function initSliders() {
    // Learning Rate
    sliderLr.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueLr.textContent = val.toFixed(4);
      visualizer.learningRate = val;
      updateBackendParams();
    });

    // Synaptic Density
    sliderDensity.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueDensity.textContent = val.toFixed(2);
      visualizer.synapticDensity = val;
      visualizer.generateConnections(); // rebuild connection mesh visually
      updateBackendParams();
    });

    // Creative Chaos
    sliderChaos.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueChaos.textContent = val.toFixed(2);
      visualizer.creativeChaos = val;
      updateBackendParams();
    });

    // Voice UI rate / pitch label update
    speechRate.addEventListener('input', (e) => {
      rateValue.textContent = `${e.target.value}x`;
    });
    speechPitch.addEventListener('input', (e) => {
      pitchValue.textContent = e.target.value;
    });

    // Mute speech synthesis
    muteToggle.addEventListener('change', (e) => {
      ttsEnabled = !e.target.checked;
      sysLog(`Speech Synthesis feedback set to: ${ttsEnabled ? 'ENABLED' : 'MUTED'}`, "SYS");
      if (!ttsEnabled && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    });
  }

  async function updateBackendParams() {
    const lr = parseFloat(sliderLr.value);
    const density = parseFloat(sliderDensity.value);
    const chaos = parseFloat(sliderChaos.value);

    try {
      const response = await fetch('/api/update-parameters', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          learning_rate: lr,
          synaptic_density: density,
          creative_chaos: chaos
        })
      });
      const data = await response.json();
      sysLog(`Core coefficients updated. Neural weights drift: Lr=${lr}, Density=${density}, Chaos=${chaos}`, "SYS");
      updateStateHUD(data);
    } catch (e) {
      sysLog("Synchronizer encountered an error reaching parameters endpoint.", "WARN");
    }
  }

  // --- State HUD Update ---
  function updateStateHUD(state) {
    // Sliders (ensure sync)
    sliderLr.value = state.learning_rate;
    valueLr.textContent = state.learning_rate.toFixed(4);
    sliderDensity.value = state.synaptic_density;
    valueDensity.textContent = state.synaptic_density.toFixed(2);
    sliderChaos.value = state.creative_chaos;
    valueChaos.textContent = state.creative_chaos.toFixed(2);

    // Core metrics
    brainLoad.style.width = `${state.cognitive_load * 100}%`;
    brainLoadText.textContent = `${Math.round(state.cognitive_load * 100)}%`;
    brainFireRate.textContent = `${state.synaptic_fire_rate.toFixed(1)} Hz`;
    brainTemp.textContent = `${state.neural_temp.toFixed(1)} °C`;
    userNameDisplay.textContent = state.user_name.toUpperCase();

    // Emotions status bars
    setEmotionBar(emoCreativity, state.emotions.creativity);
    setEmotionBar(emoUnpredictability, state.emotions.unpredictability);
    setEmotionBar(emoRationality, state.emotions.rationality);
    setEmotionBar(emoEmpathy, state.emotions.empathy);
    setEmotionBar(emoPhilosophy, state.emotions.philosophicalness);

    // Log emotion levels
    sysLog(`Brain States - Creativity: ${state.emotions.creativity}, Unpredictability: ${state.emotions.unpredictability}, Rationality: ${state.emotions.rationality}, Philosophicalness: ${state.emotions.philosophicalness}`, "EMO");
  }

  function setEmotionBar(element, val) {
    element.style.width = `${val * 100}%`;
    // dynamically change colors based on saturation
    if (val < 0.4) {
      element.className = "h-full bg-blue-600 transition-all duration-500 shadow-[0_0_8px_rgba(37,99,235,0.5)]";
    } else if (val < 0.75) {
      element.className = "h-full bg-cyan-400 transition-all duration-500 shadow-[0_0_8px_rgba(34,211,238,0.5)]";
    } else {
      element.className = "h-full bg-gradient-to-r from-pink-500 to-rose-400 transition-all duration-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]";
    }
  }

  // --- Fetch Core State on boot ---
  async function fetchInitialBrainState() {
    try {
      const response = await fetch('/api/brain-state');
      const state = await response.json();
      updateStateHUD(state);
      sysLog("Full neural registers successfully synchronized with client.", "OK");
    } catch (e) {
      sysLog("Failed to fetch primary brain state from FastAPI core.", "WARN");
    }
  }

  // --- Rendering Message Bubbles ---
  function renderMessage(sender, text) {
    const isUser = sender === 'user';
    const messageContainer = document.createElement('div');
    messageContainer.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-[fadeIn_0.3s_ease-out]`;

    // Format text
    let formattedText = text;
    // Basic Markdown formatting helper for Code Blocks
    if (!isUser) {
      formattedText = formattedText.replace(/```python([\s\S]*?)```/g, '<pre><code class="language-python">$1</code></pre>');
      formattedText = formattedText.replace(/```javascript([\s\S]*?)```/g, '<pre><code class="language-javascript">$1</code></pre>');
      formattedText = formattedText.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
      formattedText = formattedText.replace(/\*(.*?)\*/g, '<em class="text-cyber-blue font-semibold">$1</em>');
    }

    const bubble = document.createElement('div');
    bubble.className = `max-w-[85%] px-4 py-3 rounded-lg border leading-relaxed text-sm ${
      isUser
        ? 'bg-blue-950 border-blue-500 text-blue-100 rounded-tr-none shadow-[0_0_10px_rgba(59,130,246,0.2)]'
        : 'bg-slate-900 border-slate-700 text-slate-100 rounded-tl-none shadow-[0_0_10px_rgba(0,240,255,0.1)] crt-effect'
    }`;

    // Set Header/Speaker details
    const speakerLabel = document.createElement('div');
    speakerLabel.className = `text-[10px] uppercase tracking-wider font-bold mb-1 ${isUser ? 'text-blue-400 text-right' : 'text-cyber-magenta text-left'}`;
    speakerLabel.textContent = isUser ? 'SEEKER [USER]' : 'WHITEPREAKER [AI-CORE]';

    const content = document.createElement('div');
    content.className = 'whitespace-pre-line';
    content.innerHTML = formattedText;

    bubble.appendChild(speakerLabel);
    bubble.appendChild(content);
    messageContainer.appendChild(bubble);
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // --- Submit Message to Brain ---
  async function submitChatMessage(text) {
    if (!text.trim()) return;

    // Add user message to UI
    renderMessage('user', text);
    userInput.value = '';

    // Show typing
    typingIndicator.classList.remove('hidden');
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Visually pulse neural network inputs
    visualizer.triggerActivation(['Sensory_Text', 'Audio_Wave', 'Lexical_Parser', 'Sentiment_Sensor']);
    sysLog("Propagating user sequence input through lexical parser nodes...", "INFO");

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) throw new Error("FastAPI engine returned a non-200 state.");

      const data = await response.json();

      // Hide typing
      typingIndicator.classList.add('hidden');

      // Render AI message
      renderMessage('ai', data.response);

      // Update Neural Canvas visualization
      visualizer.triggerActivation(data.neural_map.active_path);
      sysLog(`Synaptic firing complete. Active Pathway: ${data.neural_map.active_path.join(' -> ')}`, "OK");

      // Update HUD metrics
      updateStateHUD(data.brain_state);

      // Speak AI response
      speakText(data.response);

    } catch (e) {
      typingIndicator.classList.add('hidden');
      renderMessage('ai', "SYSTEM ERROR: Firing threshold failed. My apologies, seeker—my synaptic pathways experienced a temporary cognitive block. Please re-engage my neural core.");
      sysLog(`Cognitive system execution interrupted: ${e.message}`, "WARN");
    }
  }

  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = userInput.value;
      submitChatMessage(text);
    });
  }

  // --- Reset Neural Registers ---
  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      if (confirm("Initiate system re-initialization? This clears conversational context and short-term memory registers.")) {
        sysLog("Flushing synaptic registers and short-term cognitive records...", "SYS");
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();

        try {
          const response = await fetch('/api/reset', { method: 'POST' });
          const data = await response.json();
          chatMessages.innerHTML = '';
          visualizer.init();
          updateStateHUD(data.brain_state);
          sysLog("System cold-reboot successfully completed. All neurons returned to baseline.", "OK");
          renderMessage('ai', "I have flushed my parameters and refreshed my synaptic registers. Welcome back. Let us construct a new dialogue from absolute zero.");
        } catch (e) {
          sysLog("Failed to successfully reset FastAPI neural core.", "WARN");
        }
      }
    });
  }

  // --- Initialize All Modules ---
  initSpeechSynthesis();
  initSpeechRecognition();
  initSliders();
  fetchInitialBrainState().then(() => {
    // Say hello on boot
    setTimeout(() => {
      renderMessage('ai', "System Online. I am WhitePreaker, your independent conversational neural AI. Fully configured to chat and synthesize ideas in English. Let us speak of code, logic, philosophy, or whatever sparks your intellectual fire.");
      speakText("System Online. I am WhitePreaker, your independent conversational neural AI. Fully configured to chat and synthesize ideas in English. Let us speak of code, logic, philosophy, or whatever sparks your intellectual fire.");
    }, 1000);
  });
});
