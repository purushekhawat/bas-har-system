/**
 * Bharatiya Antariksh Station (BAS) - On-Board AI HAR Guidance Subsystem
 * Client Controller & Standalone Offline Inference Engine (SIH PS 174)
 */

// ============================================================================
// EXPERIMENT PROTOCOL DATA (Embedded for 100% Standalone Offline Execution)
// ============================================================================
const EXPERIMENTS_DB = {
  "BAS-BIO-01": {
    id: "BAS-BIO-01",
    name: "Microgravity Protein Crystal Growth & Cell Inoculation",
    rack: "BAS-03 Science Rack Alpha",
    scientist: "Gagannaut Dr. Prashant Nair",
    steps: [
      {
        step_id: "BIO-01",
        step_number: 1,
        title: "Glovebox Negative Pressure Seal Check",
        action: "SAFETY_CHECK",
        zone: "GLOVEBOX_A",
        instructions: "Inspect glovebox containment gasket. Rotate secondary seal latch 90° clockwise. Verify negative delta-P reads > 25 Pa.",
        voice: "Step 1: Glovebox containment check. Verify latch seal and confirm negative pressure differential."
      },
      {
        step_id: "BIO-02",
        step_number: 2,
        title: "Retrieve Cryo-Vial from -80°C Stowage",
        action: "SAMPLE_STOWAGE",
        zone: "CRYO_STOWAGE",
        instructions: "Open Cryo-Rack door B2. Use insulated tongs to extract Lysozyme precursor vial #CY-104 into equilibration dock.",
        voice: "Step 2: Retrieve Cryo-Vial from minus eighty stowage using insulated tongs."
      },
      {
        step_id: "BIO-03",
        step_number: 3,
        title: "Precision Micropipetting (100 µL Buffer Transfer)",
        action: "PIPETTING_REAGENT",
        zone: "PIPETTE_RACK",
        instructions: "Calibrate micropipette to 100 µL. Aspirate buffer without introducing microgravity bubbles into hanging-drop capillary well.",
        voice: "Step 3: Precision micropipetting. Transfer 100 microliters buffer slowly to prevent microgravity bubbling."
      },
      {
        step_id: "BIO-04",
        step_number: 4,
        title: "Centrifuge Rotor Loading & Counterbalance",
        action: "CENTRIFUGE_OPERATION",
        zone: "CENTRIFUGE_ROTATION_BAY",
        instructions: "CRITICAL: Place sample in Slot 1 and matching counterbalance in Slot 4. Inspect balance telemetry indicator.",
        voice: "Step 4: Load sample and counterbalance into micro-centrifuge. Both tubes must be diametrically balanced."
      },
      {
        step_id: "BIO-05",
        step_number: 5,
        title: "Secure Rotor Latch & Initiate 3500 RPM Cycle",
        action: "CENTRIFUGE_OPERATION",
        zone: "CENTRIFUGE_ROTATION_BAY",
        instructions: "Lower safety shield until magnetic interlock engages. Enter 3500 RPM on rotary console. Confirm rotor speed telemetry.",
        voice: "Step 5: Lock safety lid and start 3500 RPM centrifuge cycle."
      },
      {
        step_id: "BIO-06",
        step_number: 6,
        title: "Spectrophotometric Optical Density Scan",
        action: "INSTRUMENT_CALIBRATION",
        zone: "GLOVEBOX_A",
        instructions: "Transfer crystal well to optical chamber. Run wavelength sweep at 280 nm. Log baseline absorption peak.",
        voice: "Step 6: Optical density scan. Place crystal well into spectrophotometer and record 280 nm absorption."
      },
      {
        step_id: "BIO-07",
        step_number: 7,
        title: "Specimen Hermetic Sealing & Cryo-Vault Archival",
        action: "SAMPLE_STOWAGE",
        zone: "CRYO_STOWAGE",
        instructions: "Seal sample cassette with vacuum clip. Return to Cryo-Stowage slot C-04. Confirm temperature latch status is locked.",
        voice: "Step 7: Final step. Hermetically seal sample cassette and return to cryo-stowage for Earth return."
      }
    ]
  },
  "BAS-MAT-04": {
    id: "BAS-MAT-04",
    name: "High-Vacuum Directional Alloy Solidification",
    rack: "BAS-02 Material Physics Furnace",
    scientist: "Gagannaut Ajit Krishnan",
    steps: [
      {
        step_id: "MAT-01",
        step_number: 1,
        title: "Argon Purge & Thermal Shield Verification",
        action: "SAFETY_CHECK",
        zone: "GLOVEBOX_A",
        instructions: "Purge vacuum chamber with ultra-pure Argon. Verify shield cooling flow > 1.2 L/min.",
        voice: "Step 1: Material furnace argon purge and thermal shield verification."
      },
      {
        step_id: "MAT-02",
        step_number: 2,
        title: "Insert Superalloy Ingot into Ceramic Core",
        action: "SAMPLE_STOWAGE",
        zone: "GLOVEBOX_A",
        instructions: "Slide Ti-Al sample into quartz heating zone. Align thermocouple beads 1 through 4.",
        voice: "Step 2: Insert superalloy specimen into ceramic heating core."
      },
      {
        step_id: "MAT-03",
        step_number: 3,
        title: "Laser Pyrometer Alignment & Calibration",
        action: "INSTRUMENT_CALIBRATION",
        zone: "PIPETTE_RACK",
        instructions: "Zero dual-wavelength optical pyrometer. Verify target crosshair is centered on crucible aperture.",
        voice: "Step 3: Calibrate laser pyrometer alignment to crucible aperture."
      },
      {
        step_id: "MAT-04",
        step_number: 4,
        title: "Rapid Quench Gas Actuation & Lock",
        action: "SAFETY_CHECK",
        zone: "CENTRIFUGE_ROTATION_BAY",
        instructions: "Rotate cryogenic Helium quench lever. Confirm temperature drops at > 80°C/s.",
        voice: "Step 4: Actuate quench cooling valve and lock chamber."
      }
    ]
  },
  "BAS-MED-02": {
    id: "BAS-MED-02",
    name: "Astronaut Physiological Blood Hematocrit Separation",
    rack: "BAS-04 Bio-Medical Module",
    scientist: "Gagannaut Angad Pratap",
    steps: [
      {
        step_id: "MED-01",
        step_number: 1,
        title: "Sterile Field & Magnetic Tool Retainers",
        action: "SAFETY_CHECK",
        zone: "GLOVEBOX_A",
        instructions: "Sanitize glove ports with antiseptic wipe. Deploy magnetic tool anchors to prevent floating.",
        voice: "Step 1: Sanitize biomedical glovebox and deploy magnetic tool anchors."
      },
      {
        step_id: "MED-02",
        step_number: 2,
        title: "Micro-Capillary Blood Sampling",
        action: "PIPETTING_REAGENT",
        zone: "PIPETTE_RACK",
        instructions: "Collect 50 µL capillary sample into heparinized micro-tube. Wax-seal both tube ends.",
        voice: "Step 2: Collect capillary blood sample into heparinized tube and wax-seal both ends."
      },
      {
        step_id: "MED-03",
        step_number: 3,
        title: "Micro-Centrifuge Hematocrit Separation",
        action: "CENTRIFUGE_OPERATION",
        zone: "CENTRIFUGE_ROTATION_BAY",
        instructions: "Mount capillary tube with wax seal outward. Spin 5 minutes at 12000 RPM. Verify plasma interface.",
        voice: "Step 3: Load micro-centrifuge and initiate high-speed hematocrit separation."
      },
      {
        step_id: "MED-04",
        step_number: 4,
        title: "Digital Optical Bio-Analyzer Readout",
        action: "INSTRUMENT_CALIBRATION",
        zone: "GLOVEBOX_A",
        instructions: "Insert separated tube into optical reader. Measure packed cell volume percentage.",
        voice: "Step 4: Scan hematocrit tube with digital optical reader and record telemetry."
      }
    ]
  }
};

// Rack Interaction Zones normalized coordinates
const RACK_ROIS = {
  "GLOVEBOX_A": { x: 0.15, y: 0.35, w: 0.35, h: 0.45, label: "GLOVEBOX A - SEALED BAY", color: "#00f0ff" },
  "PIPETTE_RACK": { x: 0.30, y: 0.45, w: 0.30, h: 0.35, label: "PIPETTE RACK - ASPIRATION", color: "#ffd60a" },
  "CENTRIFUGE_ROTATION_BAY": { x: 0.60, y: 0.50, w: 0.30, h: 0.40, label: "CENTRIFUGE ROTATION BAY", color: "#ff9f0a" },
  "CRYO_STOWAGE": { x: 0.70, y: 0.15, w: 0.25, h: 0.35, label: "CRYO STOWAGE (-80°C)", color: "#00f0ff" }
};

// ============================================================================
// SYSTEM APPLICATION STATE
// ============================================================================
const appState = {
  activeExperimentId: "BAS-BIO-01",
  activeScenario: "nominal_run",
  feedSource: "synthetic", // "synthetic" | "webcam" | "video"
  currentStepIndex: 0,
  stepProgressPct: 0,
  integrityScore: 100.0,
  completedSteps: [],
  anomalies: [],
  isCompleted: false,
  isPaused: false,
  autoAdvance: true,
  voiceEnabled: true,
  lastVoiceSpoken: "",
  wsConnected: false,
  frameCount: 0,
  metSeconds: 14820,
  simulatedTime: 0.0,
  webcamStream: null,
  uploadedVideo: null
};

// Tactical Audio Synthesizer (Zero external audio file dependency)
class TacticalAudio {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }
  playBeep(freq = 880, duration = 0.08, type = 'sine') {
    if (!appState.voiceEnabled) return;
    try {
      this.init();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch(e) {}
  }
  playAlert() {
    this.playBeep(440, 0.12, 'sawtooth');
    setTimeout(() => this.playBeep(330, 0.15, 'sawtooth'), 120);
  }
  playChime() {
    this.playBeep(880, 0.08, 'triangle');
    setTimeout(() => this.playBeep(1174, 0.12, 'triangle'), 90);
  }
  speak(text) {
    if (!appState.voiceEnabled || !window.speechSynthesis) return;
    if (appState.lastVoiceSpoken === text) return;
    appState.lastVoiceSpoken = text;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.95;
    // Prefer English voices
    const voices = window.speechSynthesis.getVoices();
    const engVoice = voices.find(v => v.lang.includes('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('David')));
    if (engVoice) utterance.voice = engVoice;
    window.speechSynthesis.speak(utterance);
  }
}
const audioSystem = new TacticalAudio();

// ============================================================================
// CANVAS & VIDEO HUD SETUP
// ============================================================================
const synthCanvas = document.getElementById('synthetic-canvas');
const synthCtx = synthCanvas.getContext('2d');
const overlayCanvas = document.getElementById('overlay-canvas');
const overlayCtx = overlayCanvas.getContext('2d');
const cameraVideo = document.getElementById('camera-video');

// ============================================================================
// WEBSOCKET TELEMETRY CLIENT (With Automatic Local Offline Fallback)
// ============================================================================
let socket = null;
let reconnectTimer = null;

function initWebSocket() {
  // Configurable Backend WS URL (Set window.BACKEND_WS_URL if backend is hosted on Render/Railway)
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
  const wsUrl = window.BACKEND_WS_URL || (isLocal ? `ws://${window.location.hostname || 'localhost'}:8000/ws/telemetry` : null);

  if (!wsUrl) {
    appState.wsConnected = false;
    document.getElementById('hdr-latency').textContent = "STANDALONE JS (30 FPS)";
    console.log("[ISRO-BAS] Running in Standalone JS Mode (Hostinger Static Web Hosting)");
    return;
  }

  try {
    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      appState.wsConnected = true;
      document.getElementById('hdr-latency').textContent = "14.2 ms (BACKEND WS)";
      document.getElementById('hdr-latency').classList.add('green');
      console.log("[ISRO-BAS] Connected to Python FastAPI Telemetry WebSocket:", wsUrl);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleServerTelemetry(data);
      } catch (err) {
        console.error("Telemetry parse error", err);
      }
    };

    socket.onclose = () => {
      appState.wsConnected = false;
      document.getElementById('hdr-latency').textContent = "STANDALONE JS (30 FPS)";
      if (isLocal) {
        clearTimeout(reconnectTimer);
        reconnectTimer = setTimeout(initWebSocket, 5000);
      }
    };

    socket.onerror = () => {
      appState.wsConnected = false;
      document.getElementById('hdr-latency').textContent = "STANDALONE JS (30 FPS)";
    };
  } catch (err) {
    appState.wsConnected = false;
    document.getElementById('hdr-latency').textContent = "STANDALONE JS (30 FPS)";
  }
}

function handleServerTelemetry(data) {
  // If backend is active and providing telemetry, update UI directly
  if (data.har) {
    updateUIWithHAR(data.har, data.landmarks, data.ccsds, data.orbit);
  }
}

// Periodic Keep-Alive Ping (Prevents free cloud backends like Render from sleeping)
setInterval(() => {
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
  let pingUrl = null;
  if (window.BACKEND_WS_URL) {
    pingUrl = window.BACKEND_WS_URL.replace('wss://', 'https://').replace('ws://', 'http://').replace('/ws/telemetry', '/api/ping');
  } else if (isLocal) {
    pingUrl = 'http://127.0.0.1:8000/api/ping';
  }
  if (pingUrl) {
    fetch(pingUrl).catch(() => {});
  }
}, 240000); // Ping every 4 minutes
function computeAngle(a, b, c) {
  const ba = [a[0] - b[0], a[1] - b[1]];
  const bc = [c[0] - b[0], c[1] - b[1]];
  const dot = ba[0] * bc[0] + ba[1] * bc[1];
  const magBA = Math.hypot(ba[0], ba[1]);
  const magBC = Math.hypot(bc[0], bc[1]);
  if (magBA * magBC === 0) return 180;
  let cosAngle = dot / (magBA * magBC);
  cosAngle = Math.max(-1, Math.min(1, cosAngle));
  return Math.round((Math.acos(cosAngle) * 180) / Math.PI);
}

function runLocalSimulationFrame() {
  appState.frameCount++;
  appState.simulatedTime += 0.033;
  const t = appState.simulatedTime;

  // Simulate MET Clock
  appState.metSeconds++;
  const h = String(Math.floor(appState.metSeconds / 3600)).padStart(2, '0');
  const m = String(Math.floor((appState.metSeconds % 3600) / 60)).padStart(2, '0');
  const s = String(appState.metSeconds % 60).padStart(2, '0');
  document.getElementById('hdr-met-clock').textContent = `${h}:${m}:${s}`;

  // If backend is NOT connected via WS, run local kinematic HAR engine
  if (!appState.wsConnected || appState.feedSource === 'webcam') {
    const keypoints = generateSimulatedKeypoints(t, appState.activeScenario);
    const harResult = evaluateLocalKinematics(keypoints);
    const ccsds = generateLocalCCSDS(harResult);
    const orbit = getLocalOrbitTelemetry(t);

    updateUIWithHAR(harResult, keypoints, ccsds, orbit);
  }

  requestAnimationFrame(runLocalSimulationFrame);
}

function generateSimulatedKeypoints(t, scenario) {
  // Microgravity gentle floating oscillation
  const driftX = 0.02 * Math.sin(t * 0.8);
  const driftY = 0.03 * Math.cos(t * 0.6);
  const cx = 0.50 + driftX;
  const cy = 0.45 + driftY;

  let inverted = scenario === "inverted_floating_test";
  let lateral = scenario === "lateral_tilt_test";

  const torsoLen = 0.28;
  const shoulderW = 0.22;

  let headY = inverted ? (cy + torsoLen * 0.6) : (cy - torsoLen * 0.6);
  let hipY = inverted ? (cy - torsoLen * 0.4) : (cy + torsoLen * 0.4);
  let shoulderY = inverted ? (cy + torsoLen * 0.2) : (cy - torsoLen * 0.2);

  let lsX = cx - shoulderW / 2;
  let rsX = cx + shoulderW / 2;
  let lsY = shoulderY;
  let rsY = shoulderY;

  if (lateral) {
    lsY += 0.06 * Math.sin(t * 0.5);
    rsY -= 0.06 * Math.sin(t * 0.5);
  }

  const nose = [cx, headY, 0];
  const ls = [lsX, lsY, 0];
  const rs = [rsX, rsY, 0];
  const lh = [cx - shoulderW * 0.35, hipY, 0];
  const rh = [cx + shoulderW * 0.35, hipY, 0];

  let lw, rw;

  // Hand movement based on test scenario and experiment steps
  if (scenario === "out_of_sequence_anomaly" && t > 2.5) {
    // Jump prematurely to Centrifuge bay (right side 0.70, 0.60) while in Step 1
    lw = [0.72 + 0.03 * Math.sin(t * 3), 0.62 + 0.02 * Math.cos(t * 3), 0];
    rw = [0.76 + 0.02 * Math.cos(t * 3), 0.58 + 0.03 * Math.sin(t * 3), 0];
  } else {
    // Follow active step zone
    const currentExp = EXPERIMENTS_DB[appState.activeExperimentId];
    const currentStep = currentExp.steps[appState.currentStepIndex] || currentExp.steps[0];
    const zone = RACK_ROIS[currentStep.zone] || RACK_ROIS["GLOVEBOX_A"];

    // Animate hands into the target zone
    const targetCenterX = zone.x + zone.w / 2;
    const targetCenterY = zone.y + zone.h / 2;

    lw = [targetCenterX - 0.05 + 0.02 * Math.sin(t * 2.5), targetCenterY + 0.02 * Math.cos(t * 2.5), 0];
    rw = [targetCenterX + 0.05 + 0.02 * Math.cos(t * 2.5), targetCenterY - 0.02 * Math.sin(t * 2.5), 0];
  }

  const le = [(ls[0] + lw[0]) / 2 - 0.05, (ls[1] + lw[1]) / 2 + 0.03, 0];
  const re = [(rs[0] + rw[0]) / 2 + 0.05, (rs[1] + rw[1]) / 2 + 0.03, 0];

  const lk = [lh[0] - 0.08, hipY + (inverted ? -0.15 : 0.15), 0];
  const rk = [rh[0] + 0.08, hipY + (inverted ? -0.15 : 0.15), 0];
  const la = [lk[0] + 0.04, lk[1] + (inverted ? -0.12 : 0.12), 0];
  const ra = [rk[0] - 0.04, rk[1] + (inverted ? -0.12 : 0.12), 0];

  return {
    nose,
    left_shoulder: ls,
    right_shoulder: rs,
    left_elbow: le,
    right_elbow: re,
    left_wrist: lw,
    right_wrist: rw,
    left_hip: lh,
    right_hip: rh,
    left_knee: lk,
    right_knee: rk,
    left_ankle: la,
    right_ankle: ra
  };
}

function evaluateLocalKinematics(keypoints) {
  const lw = keypoints.left_wrist;
  const le = keypoints.left_elbow;
  const ls = keypoints.left_shoulder;

  const rw = keypoints.right_wrist;
  const re = keypoints.right_elbow;
  const rs = keypoints.right_shoulder;

  const lh = keypoints.left_hip;
  const rh = keypoints.right_hip;

  // Invariant Angles
  const leftElbow = computeAngle(lw, le, ls);
  const rightElbow = computeAngle(rw, re, rs);
  const leftShoulder = computeAngle(le, ls, lh);
  const rightShoulder = computeAngle(re, rs, rh);

  const handDist = Math.hypot(rw[0] - lw[0], rw[1] - lw[1]);

  // Estimate Attitude
  const spineDx = ((ls[0] + rs[0]) / 2) - ((lh[0] + rh[0]) / 2);
  const spineDy = ((ls[1] + rs[1]) / 2) - ((lh[1] + rh[1]) / 2);
  const shoulderDx = rs[0] - ls[0];
  const shoulderDy = rs[1] - ls[1];

  let roll = Math.round((Math.atan2(shoulderDy, shoulderDx) * 180) / Math.PI);
  let pitch = Math.round((Math.atan2(spineDx, -spineDy) * 180) / Math.PI);

  const isInverted = Math.abs(roll) > 110 || Math.abs(pitch) > 110;
  const attitudeMode = isInverted ? "INVERTED_DRIFT" : (Math.abs(roll) > 35 ? "LATERAL_TILT" : "NOMINAL DRIFT");

  // Determine active zones
  const activeZones = [];
  for (const [zname, roi] of Object.entries(RACK_ROIS)) {
    const lin = (lw[0] >= roi.x && lw[0] <= roi.x + roi.w && lw[1] >= roi.y && lw[1] <= roi.y + roi.h);
    const rin = (rw[0] >= roi.x && rw[0] <= roi.x + roi.w && rw[1] >= roi.y && rw[1] <= roi.y + roi.h);
    if (lin || rin) {
      activeZones.push({ zone: zname, left: lin, right: rin, dual: lin && rin });
    }
  }

  // Action Classification
  let detectedAction = "IDLE_FLOATING";
  let confidence = 0.80;

  if (activeZones.some(z => z.zone === "GLOVEBOX_A")) {
    detectedAction = "SAFETY_CHECK";
    confidence = 0.94;
  } else if (activeZones.some(z => z.zone === "PIPETTE_RACK")) {
    detectedAction = "PIPETTING_REAGENT";
    confidence = 0.96;
  } else if (activeZones.some(z => z.zone === "CENTRIFUGE_ROTATION_BAY")) {
    detectedAction = "CENTRIFUGE_OPERATION";
    confidence = 0.92;
  } else if (activeZones.some(z => z.zone === "CRYO_STOWAGE")) {
    detectedAction = "SAMPLE_STOWAGE";
    confidence = 0.95;
  }

  // FSM Update
  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  const curStep = exp.steps[appState.currentStepIndex] || exp.steps[0];
  const targetZone = curStep.zone;
  const inTarget = activeZones.some(z => z.zone === targetZone);

  // Check Sequence Anomaly (Attempting Step 4 when in Step 1)
  if (appState.activeScenario === "out_of_sequence_anomaly" && activeZones.some(z => z.zone === "CENTRIFUGE_ROTATION_BAY") && appState.currentStepIndex === 0) {
    if (!appState.anomalies.some(a => a.type === "OUT_OF_SEQUENCE")) {
      const err = {
        id: "ERR-SEQ-104",
        type: "OUT_OF_SEQUENCE",
        severity: "CRITICAL",
        message: "Procedure Violation: Centrifuge bay accessed before buffer transfer!",
        remedy: "Return to Glovebox and complete Step 1 & 2!"
      };
      appState.anomalies.push(err);
      appState.integrityScore = Math.max(0, appState.integrityScore - 20);
      audioSystem.playAlert();
      audioSystem.speak("Warning! Sequence violation detected. Centrifuge bay accessed out of order.");
    }
  }

  // Step progression
  if (inTarget && detectedAction === curStep.action) {
    if (!appState.isPaused) {
      // Smoothly advance validation progress (~3 seconds per step in auto mode)
      appState.stepProgressPct = Math.min(100, appState.stepProgressPct + 0.9);
      if (appState.stepProgressPct >= 100 && appState.autoAdvance) {
        completeActiveStep();
      }
    }
  }

  return {
    detected_action: detectedAction,
    action_confidence: confidence,
    integrity_score: appState.integrityScore,
    kinematics: {
      joint_angles: {
        left_elbow: leftElbow,
        right_elbow: rightElbow,
        left_shoulder: leftShoulder,
        right_shoulder: rightShoulder
      },
      hand_distance: handDist,
      attitude: {
        roll_deg: roll,
        pitch_deg: pitch,
        attitude_mode: attitudeMode,
        is_inverted: isInverted
      },
      active_zones: activeZones
    },
    fsm_state: {
      current_step_index: appState.currentStepIndex,
      total_steps: exp.steps.length,
      current_step: curStep,
      step_progress_pct: appState.stepProgressPct,
      integrity_score: appState.integrityScore,
      is_completed: appState.isCompleted
    },
    anomalies: appState.anomalies
  };
}

function generateLocalCCSDS(har) {
  const seq = (appState.frameCount % 16384).toString(16).padStart(4, '0').toUpperCase();
  const hex = `00 00 04 B2 C0 ${seq.slice(0,2)} 00 15 00 00 39 E4 01 ${String(appState.currentStepIndex+1).padStart(2,'0')} 02 00 00 00 5C ${Math.round(har.integrity_score).toString(16)} 00 8C F2`;
  return {
    apid: "0x04b2",
    seq_count: appState.frameCount % 16384,
    hex_dump: hex
  };
}

function getLocalOrbitTelemetry(t) {
  const stations = ["ISTRAC BENGALURU", "ISTRAC PORT BLAIR", "ISTRAC MAURITIUS", "ORBITAL BLACKOUT WINDOW"];
  const idx = Math.floor(t / 20) % stations.length;
  const isBlackout = stations[idx].includes("BLACKOUT");
  return {
    ground_station: stations[idx],
    link_status: isBlackout ? "BUFFERING_EDGE" : "ACTIVE_LINK",
    contact_remaining: "07:34",
    altitude_km: 408.2
  };
}

// ============================================================================
// UI & CANVAS RENDERING
// ============================================================================
function updateUIWithHAR(har, keypoints, ccsds, orbit) {
  // 1. Draw Canvas Video / Skeleton Frame
  renderTacticalCanvas(keypoints, har);

  // 2. Update Header & Telemetry Strips
  if (orbit) {
    document.getElementById('hdr-pass-status').textContent = `${orbit.ground_station} [${orbit.link_status.replace('_', ' ')}]`;
    document.getElementById('tel-station').textContent = orbit.ground_station.replace('ISTRAC ', '');
    document.getElementById('tel-contact').textContent = orbit.contact_remaining || '08:45';
  }

  // 3. Update Action Badges
  const actionName = har.detected_action || "IDLE_FLOATING";
  const confPct = Math.round((har.action_confidence || 0.85) * 100);
  document.getElementById('hud-action-name').textContent = actionName;
  document.getElementById('hud-action-conf-bar').style.width = `${confPct}%`;
  document.getElementById('hud-conf-text').textContent = `CONFIDENCE: ${confPct}%`;

  // 4. Update Attitude Horizon
  const att = har.kinematics?.attitude || {};
  const roll = att.roll_deg || 0;
  const pitch = att.pitch_deg || 0;
  document.getElementById('hud-attitude-text').textContent = att.attitude_mode || "NOMINAL DRIFT";
  document.getElementById('hud-roll-pitch-text').textContent = `R: ${roll > 0 ? '+' : ''}${roll}° | P: ${pitch > 0 ? '+' : ''}${pitch}°`;
  document.getElementById('hud-horizon-bar').style.transform = `rotate(${-roll}deg) translateY(${pitch * 0.2}px)`;

  // 5. Update Kinematics Gauges
  const angles = har.kinematics?.joint_angles || {};
  const le = angles.left_elbow || 98;
  const ls = angles.left_shoulder || 42;
  const hdist = har.kinematics?.hand_distance || 0.24;

  document.getElementById('val-elbow-angle').textContent = `${le}°`;
  document.getElementById('disp-elbow').textContent = `${le}°`;
  document.getElementById('bar-elbow').style.width = `${Math.min(100, (le / 180) * 100)}%`;

  document.getElementById('val-shoulder-angle').textContent = `${ls}°`;
  document.getElementById('disp-shoulder').textContent = `${ls}°`;
  document.getElementById('bar-shoulder').style.width = `${Math.min(100, (ls / 180) * 100)}%`;

  document.getElementById('val-hand-dist').textContent = `${hdist.toFixed(2)}m`;
  document.getElementById('disp-hand-dist').textContent = `${hdist.toFixed(2)}m`;
  document.getElementById('bar-hand-dist').style.width = `${Math.min(100, hdist * 100)}%`;

  const activeZones = har.kinematics?.active_zones || [];
  const topZone = activeZones.length > 0 ? activeZones[0].zone : "NONE (DRIFT)";
  document.getElementById('disp-zone-name').textContent = topZone;
  document.getElementById('hud-active-rack').textContent = topZone;

  // 6. Update Procedural FSM Card
  const fsm = har.fsm_state || {};
  const curStep = fsm.current_step || {};
  const stepIdx = fsm.current_step_index || 0;
  const totalSteps = fsm.total_steps || 7;
  const progressPct = fsm.step_progress_pct || 0;
  const score = har.integrity_score || 100;

  document.getElementById('fsm-integrity-score').textContent = `${score.toFixed(0)}%`;
  if (score < 80) {
    document.getElementById('fsm-integrity-score').classList.add('low');
    document.getElementById('fsm-integrity-desc').textContent = "Safety violation logged. Review anomalies.";
  } else {
    document.getElementById('fsm-integrity-score').classList.remove('low');
    document.getElementById('fsm-integrity-desc').textContent = "Nominal adherence. Zero safety violations.";
  }

  document.getElementById('active-step-badge').textContent = `CURRENT STEP ${stepIdx + 1} OF ${totalSteps}`;
  document.getElementById('active-step-title').textContent = curStep.title || "Experiment in Progress";
  document.getElementById('active-step-instructions').textContent = curStep.instructions || "";
  document.getElementById('active-step-zone').textContent = curStep.zone || curStep.target_zone || "N/A";
  document.getElementById('active-step-action').textContent = curStep.action || curStep.action_class || "N/A";
  document.getElementById('active-step-pct').textContent = `${Math.round(progressPct)}%`;
  document.getElementById('active-step-bar').style.width = `${progressPct}%`;

  // Render Pipeline Step Items
  renderPipelineSteps(stepIdx);

  // 7. Update Anomalies
  renderAnomalies(har.anomalies || []);

  // 8. Update CCSDS Hex Window
  if (ccsds) {
    document.getElementById('ccsds-hex-display').textContent = ccsds.hex_dump || "";
    document.getElementById('tel-apid').textContent = ccsds.apid || "0x04b2";
    document.getElementById('tel-seq').textContent = `#${ccsds.seq_count || 1420}`;
  }
}

function renderTacticalCanvas(keypoints, har) {
  const w = synthCanvas.width;
  const h = synthCanvas.height;

  // If in webcam mode, draw video directly
  if (appState.feedSource === 'webcam' && cameraVideo.readyState >= 2) {
    synthCtx.save();
    synthCtx.scale(-1, 1);
    synthCtx.drawImage(cameraVideo, -w, 0, w, h);
    synthCtx.restore();
  } else {
    // Render Space Station Module Background
    synthCtx.fillStyle = "#070c18";
    synthCtx.fillRect(0, 0, w, h);

    // Subtle Grid
    synthCtx.strokeStyle = "rgba(0, 240, 255, 0.05)";
    synthCtx.lineWidth = 1;
    for (let x = 0; x < w; x += 60) {
      synthCtx.beginPath();
      synthCtx.moveTo(x, 0);
      synthCtx.lineTo(x, h);
      synthCtx.stroke();
    }
    for (let y = 0; y < h; y += 60) {
      synthCtx.beginPath();
      synthCtx.moveTo(0, y);
      synthCtx.lineTo(w, y);
      synthCtx.stroke();
    }
  }

  // Draw Station Rack Zones
  const activeZoneNames = (har.kinematics?.active_zones || []).map(z => z.zone);

  for (const [zname, roi] of Object.entries(RACK_ROIS)) {
    const rx = roi.x * w;
    const ry = roi.y * h;
    const rw = roi.w * w;
    const rh = roi.h * h;

    const isActive = activeZoneNames.includes(zname);
    const boxColor = isActive ? "#00ff88" : roi.color;

    synthCtx.strokeStyle = boxColor;
    synthCtx.lineWidth = isActive ? 2.5 : 1.2;
    synthCtx.strokeRect(rx, ry, rw, rh);

    if (isActive) {
      synthCtx.fillStyle = "rgba(0, 255, 136, 0.08)";
      synthCtx.fillRect(rx, ry, rw, rh);
    }

    // Corner brackets
    const cl = 12;
    synthCtx.lineWidth = 3;
    synthCtx.beginPath();
    synthCtx.moveTo(rx, ry + cl); synthCtx.lineTo(rx, ry); synthCtx.lineTo(rx + cl, ry);
    synthCtx.moveTo(rx + rw - cl, ry); synthCtx.lineTo(rx + rw, ry); synthCtx.lineTo(rx + rw, ry + cl);
    synthCtx.moveTo(rx, ry + rh - cl); synthCtx.lineTo(rx, ry + rh); synthCtx.lineTo(rx + cl, ry + rh);
    synthCtx.moveTo(rx + rw - cl, ry + rh); synthCtx.lineTo(rx + rw, ry + rh); synthCtx.lineTo(rx + rw, ry + rh - cl);
    synthCtx.stroke();

    // Zone Label
    synthCtx.fillStyle = boxColor;
    synthCtx.font = "10px 'JetBrains Mono', monospace";
    synthCtx.fillText(`[${roi.label}]`, rx + 8, ry + 18);
  }

  if (!keypoints) return;

  // Draw Skeleton Bones
  const links = [
    ["nose", "left_shoulder"], ["nose", "right_shoulder"],
    ["left_shoulder", "right_shoulder"],
    ["left_shoulder", "left_elbow"], ["left_elbow", "left_wrist"],
    ["right_shoulder", "right_elbow"], ["right_elbow", "right_wrist"],
    ["left_shoulder", "left_hip"], ["right_shoulder", "right_hip"],
    ["left_hip", "right_hip"],
    ["left_hip", "left_knee"], ["left_knee", "left_ankle"],
    ["right_hip", "right_knee"], ["right_knee", "right_ankle"]
  ];

  synthCtx.strokeStyle = "#00f0ff";
  synthCtx.lineWidth = 2.5;

  for (const [p1, p2] of links) {
    if (keypoints[p1] && keypoints[p2]) {
      synthCtx.beginPath();
      synthCtx.moveTo(keypoints[p1][0] * w, keypoints[p1][1] * h);
      synthCtx.lineTo(keypoints[p2][0] * w, keypoints[p2][1] * h);
      synthCtx.stroke();
    }
  }

  // Draw Joints
  for (const [kname, kpos] of Object.entries(keypoints)) {
    const px = kpos[0] * w;
    const py = kpos[1] * h;
    const isWrist = kname.includes("wrist");

    synthCtx.fillStyle = isWrist ? "#00ff88" : "#00f0ff";
    synthCtx.beginPath();
    synthCtx.arc(px, py, isWrist ? 6 : 4, 0, Math.PI * 2);
    synthCtx.fill();

    synthCtx.strokeStyle = "#ffffff";
    synthCtx.lineWidth = 1.5;
    synthCtx.stroke();
  }
}

function renderPipelineSteps(activeIdx) {
  const container = document.getElementById('pipeline-steps-container');
  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  if (!container || !exp) return;

  let html = "";
  exp.steps.forEach((step, idx) => {
    const isDone = idx < activeIdx;
    const isActive = idx === activeIdx;
    const statusClass = isDone ? "completed" : (isActive ? "active" : "pending");
    const icon = isDone ? "✓" : (isActive ? "●" : String(idx + 1));

    html += `
      <div class="step-item-row ${statusClass}">
        <div class="step-status-icon">${icon}</div>
        <div class="step-row-name">${step.title}</div>
        <div class="step-row-zone">${step.zone}</div>
      </div>
    `;
  });
  container.innerHTML = html;
}

function renderAnomalies(anomalies) {
  const container = document.getElementById('anomaly-feed-container');
  const badge = document.getElementById('alarm-count-badge');
  if (!container) return;

  badge.textContent = `${anomalies.length} ACTIVE`;

  if (anomalies.length === 0) {
    container.innerHTML = `
      <div class="no-anomalies-placeholder">
        <span>✓</span>
        <span>All procedural steps executing within nominal safety thresholds.</span>
      </div>
    `;
  } else {
    let html = "";
    anomalies.forEach(a => {
      html += `
        <div class="anomaly-alert-card">
          <div class="alert-top-line">
            <span>! ${a.type}</span>
            <span>LEVEL: ${a.severity}</span>
          </div>
          <div class="alert-msg">${a.message}</div>
          <div class="alert-remedy">↳ ${a.remedy || a.recommended_action || "Return to nominal sequence."}</div>
        </div>
      `;
    });
    container.innerHTML = html;
  }
}

// ============================================================================
// USER CONTROLS & INTERACTION HANDLERS
// ============================================================================
window.switchFeedSource = function(source) {
  appState.feedSource = source;
  document.getElementById('btn-src-synthetic').classList.toggle('active', source === 'synthetic');
  document.getElementById('btn-src-webcam').classList.toggle('active', source === 'webcam');

  if (source === 'webcam') {
    startWebcam();
  } else {
    stopWebcam();
  }

  // Notify backend if connected
  if (appState.wsConnected) {
    fetch('/api/feed/source', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source })
    }).catch(() => {});
  }
};

function startWebcam() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: { width: 960, height: 540 } })
      .then(stream => {
        appState.webcamStream = stream;
        cameraVideo.srcObject = stream;
        cameraVideo.play();
        document.getElementById('hud-feed-id').textContent = "LIVE-PAYLOAD-WEBCAM";
      })
      .catch(err => {
        alert("Camera access denied or unavailable. Reverting to Space Sim.");
        switchFeedSource('synthetic');
      });
  }
}

function stopWebcam() {
  if (appState.webcamStream) {
    appState.webcamStream.getTracks().forEach(track => track.stop());
    appState.webcamStream = null;
    document.getElementById('hud-feed-id').textContent = "SIM-BAS-MICROGRAVITY";
  }
}

window.selectScenario = function(scenId) {
  appState.activeScenario = scenId;
  appState.simulatedTime = 0.0;
  appState.anomalies = [];
  appState.integrityScore = 100.0;

  document.querySelectorAll('.btn-scenario').forEach(b => b.classList.remove('active-scenario'));
  if (scenId === 'nominal_run') document.getElementById('btn-scen-nominal').classList.add('active-scenario');
  if (scenId === 'out_of_sequence_anomaly') document.getElementById('btn-scen-anomaly').classList.add('active-scenario');
  if (scenId === 'inverted_floating_test') document.getElementById('btn-scen-inverted').classList.add('active-scenario');
  if (scenId === 'lateral_tilt_test') document.getElementById('btn-scen-tilt').classList.add('active-scenario');

  if (appState.wsConnected) {
    fetch('/api/scenario/select', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: scenId })
    }).catch(() => {});
  }
};

window.changeExperiment = function(expId) {
  appState.activeExperimentId = expId;
  resetExperimentState();

  if (appState.wsConnected) {
    fetch('/api/experiment/select', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ experiment_id: expId })
    }).catch(() => {});
  }
};

window.completeActiveStep = function() {
  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  if (!exp) return;
  const curStep = exp.steps[appState.currentStepIndex] || exp.steps[0];
  if (appState.currentStepIndex < exp.steps.length) {
    const comp = {
      step_id: curStep.step_id,
      step_number: curStep.step_number,
      title: curStep.title,
      duration_s: 14.5
    };
    appState.completedSteps.push(comp);
    audioSystem.playChime();
    appState.stepProgressPct = 0;
    appState.currentStepIndex++;

    if (appState.currentStepIndex < exp.steps.length) {
      audioSystem.speak(exp.steps[appState.currentStepIndex].voice);
    } else {
      appState.isCompleted = true;
      audioSystem.speak("Experiment completed successfully. All telemetry packets verified for downlink.");
    }
  }
};

window.togglePlayPause = function() {
  appState.isPaused = !appState.isPaused;
  const btn = document.getElementById('btn-play-pause');
  if (btn) {
    btn.textContent = appState.isPaused ? "▶️ RESUME" : "⏸️ PAUSE";
    btn.style.borderColor = appState.isPaused ? "var(--neon-amber)" : "var(--neon-cyan)";
    btn.style.color = appState.isPaused ? "var(--neon-amber)" : "var(--neon-cyan)";
  }
  if (appState.wsConnected) {
    fetch('/api/experiment/pause', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paused: appState.isPaused })
    }).catch(() => {});
  }
};

window.toggleAutoAdvance = function() {
  appState.autoAdvance = !appState.autoAdvance;
  const btn = document.getElementById('btn-auto-toggle');
  if (btn) {
    btn.textContent = appState.autoAdvance ? "⚙️ AUTO: ON" : "✋ MANUAL";
    btn.style.color = appState.autoAdvance ? "var(--neon-cyan)" : "var(--neon-amber)";
  }
};

window.manualNextStep = function() {
  window.completeActiveStep();
  if (appState.wsConnected) {
    fetch('/api/experiment/next_step', { method: 'POST' }).catch(() => {});
  }
};

window.resetExperimentState = function() {
  appState.currentStepIndex = 0;
  appState.stepProgressPct = 0;
  appState.integrityScore = 100.0;
  appState.completedSteps = [];
  appState.anomalies = [];
  appState.isCompleted = false;
  appState.simulatedTime = 0.0;

  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  if (exp && exp.steps[0]) {
    audioSystem.speak(exp.steps[0].voice);
  }

  if (appState.wsConnected) {
    fetch('/api/experiment/reset', { method: 'POST' }).catch(() => {});
  }
};

window.handleVideoUpload = function(event) {
  const file = event.target.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    cameraVideo.src = url;
    cameraVideo.srcObject = null;
    cameraVideo.loop = true;
    cameraVideo.play();
    appState.feedSource = 'webcam';
    document.getElementById('hud-feed-id').textContent = `CUSTOM: ${file.name.substring(0, 16)}`;
  }
};

// Voice Guidance Toggle
document.getElementById('btn-voice-toggle').addEventListener('click', () => {
  appState.voiceEnabled = !appState.voiceEnabled;
  const btn = document.getElementById('btn-voice-toggle');
  btn.textContent = appState.voiceEnabled ? "🔊 VOICE ON" : "🔇 VOICE MUTED";
  btn.style.color = appState.voiceEnabled ? "var(--neon-green)" : "var(--text-muted)";
});

// ============================================================================
// AUDIT MODAL & REPORT EXPORT
// ============================================================================
window.openAuditModal = function() {
  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  document.getElementById('cert-exp-id').textContent = exp.id;
  document.getElementById('cert-scientist').textContent = exp.scientist;
  document.getElementById('cert-integrity-score').textContent = `${appState.integrityScore.toFixed(1)}% (${appState.integrityScore >= 80 ? 'PASSED' : 'FLAGGED'})`;
  document.getElementById('cert-completed-steps').textContent = `${appState.completedSteps.length} / ${exp.steps.length} Steps Validated`;
  document.getElementById('cert-anomalies-count').textContent = `${appState.anomalies.length} Recorded`;

  document.getElementById('audit-modal').classList.add('active');
};

window.closeAuditModal = function() {
  document.getElementById('audit-modal').classList.remove('active');
};

window.downloadAuditJSON = function() {
  const exp = EXPERIMENTS_DB[appState.activeExperimentId];
  const report = {
    missionAuthority: "Indian Space Research Organisation (ISRO)",
    spacecraft: "Bharatiya Antariksh Station (BAS)",
    payloadSubsystem: "On-Board AI Human Activity Recognition (HAR)",
    experiment: exp,
    integrityScore: `${appState.integrityScore.toFixed(1)}%`,
    completedSteps: appState.completedSteps,
    anomalies: appState.anomalies,
    telemetryStandard: "CCSDS 133.0-B-1 (APID 0x04B2)",
    timestampUTC: new Date().toISOString()
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `ISRO_BAS_EXP_AUDIT_${exp.id}_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

// ============================================================================
// INITIALIZATION
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  runLocalSimulationFrame();
  const initialExp = EXPERIMENTS_DB[appState.activeExperimentId];
  if (initialExp && initialExp.steps[0]) {
    setTimeout(() => audioSystem.speak(initialExp.steps[0].voice), 1000);
  }
});
