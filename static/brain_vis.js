/**
 * WhitePreaker Interactive Neural Network Canvas Visualizer
 * Renders a 3-layered high-fidelity neural system with pulsing signals, hover details, and synaptic weight vectors.
 */

class WhitePreakerBrainVis {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.nodes = [];
    this.connections = [];
    this.impulses = []; // Traveling particles on active synapses
    this.hoveredNode = null;
    this.activePathNodes = new Set();

    // Configurations
    this.themeColors = {
      neonBlue: '#00f0ff',
      neonMagenta: '#ff007f',
      neonGreen: '#39ff14',
      cyberDark: '#070913',
      darkBlue: '#1b264f',
      glowColor: 'rgba(0, 240, 255, 0.4)'
    };

    this.learningRate = 0.015;
    this.synapticDensity = 0.85;
    this.creativeChaos = 0.70;

    this.init();
    this.setupEventListeners();
    this.startAnimation();
  }

  init() {
    this.resizeCanvas();
    this.generateNeuralArchitecture();
  }

  resizeCanvas() {
    const parent = this.canvas.parentElement;
    this.canvas.width = parent.clientWidth || 600;
    this.canvas.height = parent.clientHeight || 400;
  }

  setupEventListeners() {
    window.addEventListener('resize', () => {
      this.resizeCanvas();
      this.generateNeuralArchitecture();
    });

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      this.hoveredNode = null;
      for (let node of this.nodes) {
        const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
        if (dist < node.radius + 5) {
          this.hoveredNode = node;
          break;
        }
      }
    });
  }

  updateParameters(lr, density, chaos) {
    this.learningRate = lr;
    this.synapticDensity = density;
    this.creativeChaos = chaos;
    // regenerate connections with new density threshold
    this.generateConnections();
  }

  generateNeuralArchitecture() {
    this.nodes = [];
    const width = this.canvas.width;
    const height = this.canvas.height;

    // Layers: Input, Hidden Cognitive, Hidden Associative, Output
    const layers = [
      {
        id: 'input',
        name: 'Input Sensory',
        nodes: ['Sensory_Text', 'Audio_Wave', 'Lexical_Parser', 'Sentiment_Sensor']
      },
      {
        id: 'hidden_cognitive',
        name: 'Cognitive Layer',
        nodes: ['Semantic_Router', 'Context_Memory', 'Syntactic_Analyzer', 'Logic_Processor']
      },
      {
        id: 'hidden_associative',
        name: 'Associative Layer',
        nodes: ['Philosophical_Core', 'Creative_Sparks', 'Emotional_Matrix', 'Unpredictable_Jumper']
      },
      {
        id: 'output',
        name: 'Synthesis Output',
        nodes: ['Response_Synthesizer', 'Vocal_Modulator', 'Neural_Feedback']
      }
    ];

    const layerSpacing = width / (layers.length + 0.2);

    layers.forEach((layer, layerIdx) => {
      const x = layerSpacing * (layerIdx + 0.6);
      const nodeCount = layer.nodes.length;
      const verticalSpacing = height / (nodeCount + 1);

      layer.nodes.forEach((nodeName, nodeIdx) => {
        const y = verticalSpacing * (nodeIdx + 1);
        this.nodes.push({
          id: nodeName,
          layer: layer.id,
          layerName: layer.name,
          label: nodeName.replace('_', ' '),
          x: x,
          y: y,
          originalY: y,
          radius: 12,
          activation: 0.1, // pulsing activation level
          pulseSpeed: 0.02 + Math.random() * 0.03,
          pulsePhase: Math.random() * Math.PI * 2
        });
      });
    });

    this.generateConnections();
  }

  generateConnections() {
    this.connections = [];
    const layerOrder = ['input', 'hidden_cognitive', 'hidden_associative', 'output'];

    // Connect each node in layer N to nodes in layer N+1
    for (let i = 0; i < layerOrder.length - 1; i++) {
      const currentLayerNodes = this.nodes.filter(n => n.layer === layerOrder[i]);
      const nextLayerNodes = this.nodes.filter(n => n.layer === layerOrder[i+1]);

      currentLayerNodes.forEach(source => {
        nextLayerNodes.forEach(target => {
          // Check random threshold against synaptic density
          if (Math.random() < this.synapticDensity) {
            const initialWeight = 0.2 + Math.random() * 0.8;
            this.connections.push({
              source: source,
              target: target,
              weight: initialWeight,
              active: false,
              pulseIntensity: 0
            });
          }
        });
      });
    }
  }

  triggerActivation(activeNodeIds) {
    this.activePathNodes = new Set(activeNodeIds);

    // Ignite impulses
    this.connections.forEach(conn => {
      const sourceActive = activeNodeIds.includes(conn.source.id);
      const targetActive = activeNodeIds.includes(conn.target.id);

      if (sourceActive && targetActive) {
        conn.active = true;
        conn.pulseIntensity = 1.0;

        // Spawn multiple traveling particles (impulses) on this synapse
        for (let count = 0; count < 3; count++) {
          this.impulses.push({
            source: conn.source,
            target: conn.target,
            progress: -count * 0.25, // offset spawn time
            speed: 0.015 + this.learningRate * 0.8 + Math.random() * 0.01,
            size: 3 + Math.random() * 2
          });
        }
      } else {
        conn.active = false;
        conn.pulseIntensity = 0.1;
      }
    });

    // Ignite nodes
    this.nodes.forEach(node => {
      if (activeNodeIds.includes(node.id)) {
        node.activation = 1.0;
      }
    });
  }

  draw() {
    const ctx = this.ctx;
    const width = this.canvas.width;
    const height = this.canvas.height;

    ctx.clearRect(0, 0, width, height);

    // Draw background grid lines slightly
    ctx.strokeStyle = 'rgba(27, 38, 79, 0.15)';
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Update nodes hover and slight vertical floating
    this.nodes.forEach(node => {
      node.pulsePhase += node.pulseSpeed;
      // Slight vertical floating based on creative chaos
      const floatRange = this.creativeChaos * 6;
      node.y = node.originalY + Math.sin(node.pulsePhase) * floatRange;

      // Decay active glow back to normal
      if (node.activation > 0.1) {
        node.activation -= 0.008;
      }
    });

    // Draw synapses
    this.connections.forEach(conn => {
      const gradient = ctx.createLinearGradient(conn.source.x, conn.source.y, conn.target.x, conn.target.y);

      if (conn.active) {
        gradient.addColorStop(0, this.themeColors.neonMagenta);
        gradient.addColorStop(1, this.themeColors.neonBlue);
        ctx.lineWidth = 2.5 + conn.weight * 2;
        ctx.strokeStyle = gradient;
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.themeColors.neonBlue;
      } else {
        ctx.strokeStyle = `rgba(27, 38, 79, ${0.15 + conn.weight * 0.2})`;
        ctx.lineWidth = 0.5 + conn.weight * 1.5;
        ctx.shadowBlur = 0;
      }

      ctx.beginPath();
      ctx.moveTo(conn.source.x, conn.source.y);
      ctx.lineTo(conn.target.x, conn.target.y);
      ctx.stroke();
      ctx.shadowBlur = 0; // reset
    });

    // Update and draw traveling particles (impulses)
    for (let i = this.impulses.length - 1; i >= 0; i--) {
      const imp = this.impulses[i];
      imp.progress += imp.speed;

      // Only draw if on the visible wire segment
      if (imp.progress >= 0 && imp.progress <= 1) {
        const x = imp.source.x + (imp.target.x - imp.source.x) * imp.progress;
        const y = imp.source.y + (imp.target.y - imp.source.y) * imp.progress;

        ctx.beginPath();
        ctx.arc(x, y, imp.size, 0, Math.PI * 2);
        ctx.fillStyle = this.themeColors.neonBlue;
        ctx.shadowBlur = 12;
        ctx.shadowColor = this.themeColors.neonBlue;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Remove once arrived
      if (imp.progress > 1) {
        // Boost target node activation temporarily on particle arrival
        imp.target.activation = Math.min(1.0, imp.target.activation + 0.15);
        this.impulses.splice(i, 1);
      }
    }

    // Draw neurons (nodes)
    this.nodes.forEach(node => {
      const isNodeActive = this.activePathNodes.has(node.id);

      // Inner glowing shadow
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);

      // Node style changes with current activation
      if (isNodeActive || node.activation > 0.3) {
        ctx.fillStyle = this.themeColors.cyberDark;
        ctx.strokeStyle = isNodeActive ? this.themeColors.neonMagenta : this.themeColors.neonBlue;
        ctx.lineWidth = 3;
        ctx.shadowBlur = 15;
        ctx.shadowColor = isNodeActive ? this.themeColors.neonMagenta : this.themeColors.neonBlue;
      } else {
        ctx.fillStyle = 'rgba(12, 16, 34, 0.9)';
        ctx.strokeStyle = this.themeColors.darkBlue;
        ctx.lineWidth = 1.5;
        ctx.shadowBlur = 0;
      }
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Draw active center core
      if (node.activation > 0.1) {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius * 0.45 * node.activation, 0, Math.PI * 2);
        ctx.fillStyle = isNodeActive ? this.themeColors.neonMagenta : this.themeColors.neonGreen;
        ctx.fill();
      }

      // Draw label
      ctx.font = '10px "Fira Code", monospace';
      ctx.fillStyle = (isNodeActive || this.hoveredNode === node) ? '#ffffff' : '#718096';
      ctx.textAlign = 'center';

      // If hovered or active, make text brighter
      if (this.hoveredNode === node) {
        ctx.fillStyle = this.themeColors.neonBlue;
        ctx.fillText(node.label, node.x, node.y - node.radius - 8);
        ctx.font = '8px "Fira Code", monospace';
        ctx.fillStyle = '#a0aec0';
        ctx.fillText(`Layer: ${node.layerName}`, node.x, node.y + node.radius + 12);
      } else {
        ctx.fillText(node.label, node.x, node.y - node.radius - 6);
      }
    });

    // Draw HUD metrics floating inside canvas
    ctx.font = '11px "Orbitron", sans-serif';
    ctx.fillStyle = 'rgba(0, 240, 255, 0.4)';
    ctx.fillText("SYNAPTIC MAP: ACTIVE CORE", 120, 25);
    ctx.beginPath();
    ctx.rect(15, 15, 10, 10);
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.5)';
    ctx.stroke();
  }

  startAnimation() {
    const frame = () => {
      this.draw();
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }
}
