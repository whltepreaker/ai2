/**
 * WhitePreaker Cognitive Chat Engine & Web Speech Integration
 * Bridges API requests, local speech-to-text, fluent text-to-speech, and neural map renderings.
 * Fully supports Autonomous Cycle Mode, Chain of Thought mapping, and direct constraint tracking.
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- Setup Canvas Visualization ---
  const visualizer = new WhitePreakerBrainVis('neuralCanvas');

  // --- UI Elements ---
  const chatForm = document.getElementById('chatForm');
  const userInput = document.getElementById('userInput');
  const chatMessages = document.getElementById('chatMessages');
  const typingIndicator = document.getElementById('typingIndicator');

  // Controls & Buttons
  const btnListen = document.getElementById('btnListen');
  const listenStatus = document.getElementById('listenStatus');
  const voiceSelect = document.getElementById('voiceSelect');
  const speechRate = document.getElementById('speechRate');
  const rateValue = document.getElementById('rateValue');
  const speechPitch = document.getElementById('speechPitch');
  const pitchValue = document.getElementById('pitchValue');
  const muteToggle = document.getElementById('muteToggle');
  const btnReset = document.getElementById('btnReset');
  const btnAutonomous = document.getElementById('btnAutonomous');
  const autoText = document.getElementById('autoText');
  const autoIndicator = document.getElementById('autoIndicator');

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

  // Directives HUD
  const hudStyle = document.getElementById('hudStyle');
  const hudFormat = document.getElementById('hudFormat');
  const hudTopic = document.getElementById('hudTopic');

  // Thought Chain blocks
  const thoughtStep1 = document.getElementById('thoughtStep1');
  const thoughtStep2 = document.getElementById('thoughtStep2');
  const thoughtStep3 = document.getElementById('thoughtStep3');
  const thoughtStep4 = document.getElementById('thoughtStep4');

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

  // Autonomous Cycle State
  let isAutonomousActive = false;
  let autonomousInterval = null;

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

  sysLog("WhitePreaker Autonomous Neural Core V2 booting up...", "SYS");

  // --- Speech Synthesis (Text to Speech) ---
  function initSpeechSynthesis() {
    if (!('speechSynthesis' in window)) {
      sysLog("Speech Synthesis API not supported in this browser environment.", "WARN");
      return;
    }

    const populateVoices = () => {
      synthesisVoices = window.speechSynthesis.getVoices();
      voiceSelect.innerHTML = '';

      synthesisVoices.forEach((voice, index) => {
        if (voice.lang.startsWith('en')) {
          const option = document.createElement('option');
          option.value = index;
          option.textContent = `${voice.name} (${voice.lang})`;
          if (voice.name.includes('Google') || voice.name.includes('Natural') || voice.name.includes('Samantha') || voice.name.includes('Moira') || voice.name.includes('Microsoft Samantha')) {
            option.selected = true;
          }
          voiceSelect.appendChild(option);
        }
      });

      if (voiceSelect.children.length === 0) {
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

    window.speechSynthesis.cancel();

    const cleanText = text.replace(/```[\s\S]*?```/g, "[Generated code displayed on screen]")
                          .replace(/[*#`_\-]/g, "")
                          .trim();

    sysLog("Calibrating speech synthesis output channel...", "INFO");
    const utterance = new SpeechSynthesisUtterance(cleanText);

    if (voiceSelect.value !== '') {
      utterance.voice = synthesisVoices[parseInt(voiceSelect.value)];
    }
    utterance.rate = parseFloat(speechRate.value);
    utterance.pitch = parseFloat(speechPitch.value);

    utterance.onstart = () => {
      sysLog("Vocal synthesizer active and broadcasting.", "OK");
      document.getElementById('aiSpeakingBadge').classList.remove('hidden');
    };

    utterance.onend = () => {
      sysLog("Vocal feedback broadcast completed successfully.", "INFO");
      document.getElementById('aiSpeakingBadge').classList.add('hidden');
    };

    utterance.onerror = (e) => {
      sysLog(`Speech Synthesis encountered a minor transmission block: ${e.error}`, "WARN");
      document.getElementById('aiSpeakingBadge').classList.add('hidden');
    };

    window.speechSynthesis.speak(utterance);
  }

  // --- Speech Recognition (Speech to Text) ---
  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      sysLog("Speech Recognition (STT) not supported. Voice trigger disabled.", "WARN");
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
      sysLog("Audio wave input active. Speak into device microphone.", "OK");

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
      sysLog("Audio wave input disabled.", "INFO");

      document.querySelectorAll('.wave-bar').forEach(bar => {
        bar.classList.remove('listening');
      });
    };

    recognitionInstance.onresult = (event) => {
      const resultText = event.results[0][0].transcript;
      sysLog(`Transcribed audio wave: "${resultText}"`, "OK");
      userInput.value = resultText;
      submitChatMessage(resultText);
    };

    recognitionInstance.onerror = (event) => {
      sysLog(`Vocal wave processing error: ${event.error}`, "WARN");
    };
  }

  if (btnListen) {
    btnListen.addEventListener('click', () => {
      if (isListening) {
        recognitionInstance.stop();
      } else {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        recognitionInstance.start();
      }
    });
  }

  // --- Parameter Sliders Sync ---
  function initSliders() {
    sliderLr.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueLr.textContent = val.toFixed(4);
      visualizer.learningRate = val;
      updateBackendParams();
    });

    sliderDensity.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueDensity.textContent = val.toFixed(2);
      visualizer.synapticDensity = val;
      visualizer.generateConnections();
      updateBackendParams();
    });

    sliderChaos.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      valueChaos.textContent = val.toFixed(2);
      visualizer.creativeChaos = val;
      updateBackendParams();
    });

    speechRate.addEventListener('input', (e) => {
      rateValue.textContent = `${e.target.value}x`;
    });
    speechPitch.addEventListener('input', (e) => {
      pitchValue.textContent = e.target.value;
    });

    muteToggle.addEventListener('change', (e) => {
      ttsEnabled = !e.target.checked;
      sysLog(`Speech Synthesis system feedback: ${ttsEnabled ? 'ENABLED' : 'MUTED'}`, "SYS");
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
      updateStateHUD(data);
    } catch (e) {
      sysLog("Sync endpoint connection interrupted.", "WARN");
    }
  }

  // --- Update HUD State & Status Elements ---
  function updateStateHUD(state) {
    sliderLr.value = state.learning_rate;
    valueLr.textContent = state.learning_rate.toFixed(4);
    sliderDensity.value = state.synaptic_density;
    valueDensity.textContent = state.synaptic_density.toFixed(2);
    sliderChaos.value = state.creative_chaos;
    valueChaos.textContent = state.creative_chaos.toFixed(2);

    brainLoad.style.width = `${state.cognitive_load * 100}%`;
    brainLoadText.textContent = `${Math.round(state.cognitive_load * 100)}%`;
    brainFireRate.textContent = `${state.synaptic_fire_rate.toFixed(1)} Hz`;
    brainTemp.textContent = `${state.neural_temp.toFixed(1)} °C`;
    userNameDisplay.textContent = state.user_name.toUpperCase();

    setEmotionBar(emoCreativity, state.emotions.creativity);
    setEmotionBar(emoUnpredictability, state.emotions.unpredictability);
    setEmotionBar(emoRationality, state.emotions.rationality);
    setEmotionBar(emoEmpathy, state.emotions.empathy);
    setEmotionBar(emoPhilosophy, state.emotions.philosophicalness);
  }

  function setEmotionBar(element, val) {
    element.style.width = `${val * 100}%`;
    if (val < 0.4) {
      element.className = "h-full bg-blue-600 transition-all duration-500 shadow-[0_0_8px_rgba(37,99,235,0.5)]";
    } else if (val < 0.75) {
      element.className = "h-full bg-cyan-400 transition-all duration-500 shadow-[0_0_8px_rgba(34,211,238,0.5)]";
    } else {
      element.className = "h-full bg-gradient-to-r from-pink-500 to-rose-400 transition-all duration-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]";
    }
  }

  function renderThoughts(thoughts) {
    if (!thoughts || thoughts.length < 4) return;
    thoughtStep1.textContent = thoughts[0].log;
    thoughtStep2.textContent = thoughts[1].log;
    thoughtStep3.textContent = thoughts[2].log;
    thoughtStep4.textContent = thoughts[3].log;

    sysLog("Chain of thought successfully visualised.", "OK");
  }

  function renderDirectives(directives) {
    if (!directives) return;
    hudStyle.textContent = directives.style.toUpperCase();
    hudFormat.textContent = directives.format.toUpperCase();
    hudTopic.textContent = (directives.specific_topic || "GENERAL").toUpperCase();
  }

  // --- Message Rendering ---
  function renderMessage(sender, text, isAutonomousQuestion = false) {
    const isUser = sender === 'user';
    const messageContainer = document.createElement('div');
    messageContainer.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-[fadeIn_0.3s_ease-out]`;

    let formattedText = text;
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
        : isAutonomousQuestion
          ? 'bg-violet-950/60 border-violet-500 text-violet-100 rounded-tl-none shadow-[0_0_10px_rgba(167,139,250,0.3)]'
          : 'bg-slate-900 border-slate-700 text-slate-100 rounded-tl-none shadow-[0_0_10px_rgba(0,240,255,0.1)] crt-effect'
    }`;

    const speakerLabel = document.createElement('div');
    speakerLabel.className = `text-[10px] uppercase tracking-wider font-bold mb-1 ${
      isUser
        ? 'text-blue-400 text-right'
        : isAutonomousQuestion
          ? 'text-violet-400 text-left'
          : 'text-cyber-magenta text-left'
    }`;

    speakerLabel.textContent = isUser
      ? 'SEEKER [USER]'
      : isAutonomousQuestion
        ? 'WHITEPREAKER [AUTONOMOUS REFLECTION QUERY]'
        : 'WHITEPREAKER [AI-CORE]';

    const content = document.createElement('div');
    content.className = 'whitespace-pre-line';
    content.innerHTML = formattedText;

    bubble.appendChild(speakerLabel);
    bubble.appendChild(content);
    messageContainer.appendChild(bubble);
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // --- Submit Message ---
  async function submitChatMessage(text) {
    if (!text.trim()) return;

    renderMessage('user', text);
    userInput.value = '';

    typingIndicator.classList.remove('hidden');
    chatMessages.scrollTop = chatMessages.scrollHeight;

    visualizer.triggerActivation(['Sensory_Text', 'Audio_Wave', 'Lexical_Parser', 'Sentiment_Sensor']);
    sysLog("Firing lexical parsers. Evaluating constraint patterns...", "INFO");

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) throw new Error("Error connecting with model endpoint.");
      const data = await response.json();

      typingIndicator.classList.add('hidden');
      renderMessage('ai', data.response);

      visualizer.triggerActivation(data.neural_map.active_path);
      updateStateHUD(data.brain_state);
      renderThoughts(data.thoughts);
      renderDirectives(data.directives);
      speakText(data.response);

    } catch (e) {
      typingIndicator.classList.add('hidden');
      renderMessage('ai', "SYSTEM COGNITIVE ERROR: Connection with the main computational core failed. Let us try again.");
      sysLog(`Cognitive exception triggered: ${e.message}`, "WARN");
    }
  }

  // --- Autonomous Step trigger ---
  async function triggerAutonomousStep() {
    typingIndicator.classList.remove('hidden');
    sysLog("Autonomous reflection trigger fired. Initiating cognitive daydream cycle...", "SYS");

    try {
      const response = await fetch('/api/autonomous-step', { method: 'POST' });
      if (!response.ok) throw new Error("Internal Server Error during self-reflection.");
      const data = await response.json();

      typingIndicator.classList.add('hidden');

      // Render self-proposed question
      renderMessage('ai', data.query, true);

      // Short delay, then render answer
      setTimeout(() => {
        renderMessage('ai', data.response);
        visualizer.triggerActivation(data.neural_map.active_path);
        updateStateHUD(data.brain_state);
        renderThoughts(data.thoughts);
        renderDirectives(data.directives);
        speakText(data.response);
      }, 1500);

    } catch (e) {
      typingIndicator.classList.add('hidden');
      sysLog(`Autonomous step failed: ${e.message}`, "WARN");
    }
  }

  // --- Toggle Autonomous Mode ---
  if (btnAutonomous) {
    btnAutonomous.addEventListener('click', () => {
      isAutonomousActive = !isAutonomousActive;

      if (isAutonomousActive) {
        btnAutonomous.className = "cyber-btn border border-green-500 bg-green-950/40 text-green-400 px-4 py-1.5 rounded flex items-center gap-2 font-bold transition pulse-glow";
        autoText.textContent = "AUTONOMOUS CYCLE: ACTIVE";
        sysLog("Autonomous Self-Reflection state successfully ENGAGED.", "SYS");

        // Trigger immediately
        triggerAutonomousStep();

        // Start cycle every 10 seconds
        autonomousInterval = setInterval(triggerAutonomousStep, 10000);
      } else {
        btnAutonomous.className = "cyber-btn border border-pink-600 bg-pink-950/20 text-pink-500 hover:bg-pink-950/60 px-4 py-1.5 rounded flex items-center gap-2 font-bold transition";
        autoText.textContent = "AUTONOMOUS CYCLE: OFF";
        sysLog("Autonomous Self-Reflection state successfully DISENGAGED.", "SYS");

        if (autonomousInterval) {
          clearInterval(autonomousInterval);
          autonomousInterval = null;
        }
      }
    });
  }

  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // If autonomous mode is active, warn user
      if (isAutonomousActive) {
        sysLog("User override detected during autonomous loop. Pausing cycle to receive sensory input.", "WARN");
      }
      const text = userInput.value;
      submitChatMessage(text);
    });
  }

  // --- Reset registers ---
  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      if (confirm("Reset current neural matrices and erase temporary dialogue records?")) {
        sysLog("Flushing neural memory buffers...", "SYS");
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();

        // Turn off autonomous if active
        if (isAutonomousActive) {
          btnAutonomous.click();
        }

        try {
          const response = await fetch('/api/reset', { method: 'POST' });
          const data = await response.json();
          chatMessages.innerHTML = '';
          visualizer.init();
          updateStateHUD(data.brain_state);
          sysLog("Cold reboot sequence completed successfully.", "OK");
          renderMessage('ai', "Neural core flushed and baseline weights restored. Operators registers are clear. Speak to me, seeker.");
        } catch (e) {
          sysLog("Failed to post reset register command.", "WARN");
        }
      }
    });
  }

  // --- Boot Initialization ---
  initSpeechSynthesis();
  initSpeechRecognition();
  initSliders();

  fetch('/api/brain-state')
    .then(r => r.json())
    .then(state => {
      updateStateHUD(state);
      sysLog("Cognitive core synchronized.", "OK");
      setTimeout(() => {
        renderMessage('ai', "System Online. I am WhitePreaker, your independent conversational neural AI. Optimized for autonomous instruction following and self-reflection loops. Interfacing complete. Let us begin.");
        speakText("System Online. I am WhitePreaker, your independent conversational neural AI. Optimized for autonomous instruction following and self-reflection loops. Interfacing complete. Let us begin.");
      }, 1000);
    });
});
