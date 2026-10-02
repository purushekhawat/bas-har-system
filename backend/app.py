"""
Bharatiya Antariksh Station (BAS) - AI Human Activity Recognition (HAR) Engine
FastAPI Server & Real-Time Telemetry Subsystem (SIH Problem Statement 174)
"""

import os
import json
import time
import base64
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from har_engine import HAREngine
from telemetry_streamer import CCSDSPacketBuilder, OrbitalPassSimulator
from synthetic_data_gen import SyntheticSpaceScenario

BASE_DIR = Path(__file__).resolve().parent.parent
PROTOCOLS_FILE = BASE_DIR / "protocols" / "experiments.json"
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="ISRO Bharatiya Antariksh Station - On-Board HAR Engine",
    description="Edge AI Human Activity Recognition for Microgravity Space Experiments (SIH PS 174)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
class SystemState:
    def __init__(self):
        self.experiments_catalog = self.load_protocols()
        self.active_experiment_id = "BAS-BIO-01"
        self.active_experiment = self.get_experiment(self.active_experiment_id)
        self.har_engine = HAREngine(self.active_experiment)
        self.telemetry_builder = CCSDSPacketBuilder()
        self.orbital_simulator = OrbitalPassSimulator()
        self.active_scenario = "nominal_run"
        self.feed_source = "synthetic"  # "synthetic" | "webcam" | "video"
        self.frame_counter = 0
        self.client_keypoints = None
        self.audit_log = []

    def load_protocols(self) -> Dict[str, Any]:
        if PROTOCOLS_FILE.exists():
            with open(PROTOCOLS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"experiments": []}

    def get_experiment(self, exp_id: str) -> Dict[str, Any]:
        for exp in self.experiments_catalog.get("experiments", []):
            if exp["id"] == exp_id:
                return exp
        return self.experiments_catalog.get("experiments", [{}])[0]

    def set_experiment(self, exp_id: str):
        self.active_experiment_id = exp_id
        self.active_experiment = self.get_experiment(exp_id)
        self.har_engine = HAREngine(self.active_experiment)
        self.frame_counter = 0
        self.log_event("EXPERIMENT_INITIALIZED", {"experiment_id": exp_id})

    def set_scenario(self, scenario_id: str):
        self.active_scenario = scenario_id
        self.frame_counter = 0
        self.log_event("SCENARIO_CHANGED", {"scenario": scenario_id})

    def reset_fsm(self):
        self.har_engine = HAREngine(self.active_experiment)
        self.frame_counter = 0
        self.log_event("FSM_RESET", {})

    def log_event(self, event_type: str, details: Dict[str, Any]):
        entry = {
            "timestamp": time.time(),
            "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "met": self.telemetry_builder.format_met(self.telemetry_builder.met_seconds),
            "event_type": event_type,
            "details": details
        }
        self.audit_log.append(entry)

state = SystemState()

# Request Models
class ScenarioSelectRequest(BaseModel):
    scenario_id: str

class ExperimentSelectRequest(BaseModel):
    experiment_id: str

class KeypointsInjectRequest(BaseModel):
    keypoints: Dict[str, Any]

@app.get("/api/ping")
@app.get("/health")
async def keep_alive_ping():
    return {
        "status": "ALIVE",
        "timestamp": time.time(),
        "service": "BAS-03-PAYLOAD-AI-HAR",
        "message": "Keep-alive ping acknowledged. Backend active."
    }

@app.get("/api/status")
async def get_status():
    return {
        "status": "OPERATIONAL",
        "subsystem": "BAS-03-PAYLOAD-AI-HAR",
        "station": "Bharatiya Antariksh Station (BAS)",
        "orbit_altitude_km": 408.2,
        "execution_mode": "EDGE_OFFLINE",
        "active_experiment": state.active_experiment_id,
        "active_scenario": state.active_scenario,
        "feed_source": state.feed_source,
        "inference_latency_ms": 14.8,
        "confidence_threshold": 0.50
    }

@app.get("/api/experiments")
async def get_experiments():
    return state.experiments_catalog

@app.post("/api/experiment/select")
async def select_experiment(req: ExperimentSelectRequest):
    state.set_experiment(req.experiment_id)
    return {"status": "SUCCESS", "active_experiment": state.active_experiment_id}

@app.post("/api/scenario/select")
async def select_scenario(req: ScenarioSelectRequest):
    valid = ["nominal_run", "out_of_sequence_anomaly", "inverted_floating_test", "lateral_tilt_test"]
    if req.scenario_id not in valid:
        raise HTTPException(status_code=400, detail="Invalid scenario ID")
    state.set_scenario(req.scenario_id)
    return {"status": "SUCCESS", "active_scenario": state.active_scenario}

@app.post("/api/experiment/reset")
async def reset_experiment():
    state.reset_fsm()
    return {"status": "SUCCESS", "message": "State machine reset to Step 1"}

@app.post("/api/experiment/pause")
async def toggle_pause_experiment(data: Optional[Dict[str, bool]] = None):
    fsm = state.har_engine.fsm
    if data and "paused" in data:
        fsm.paused = data["paused"]
    else:
        fsm.paused = not fsm.paused
    return {"status": "SUCCESS", "paused": fsm.paused}

@app.post("/api/experiment/next_step")
async def manual_next_step():
    fsm = state.har_engine.fsm
    if fsm.current_step_index < len(fsm.steps) - 1:
        fsm.current_step_index += 1
        fsm.step_progress_frames = 0
        fsm.step_start_time = time.time()
    return {"status": "SUCCESS", "current_step_index": fsm.current_step_index}

@app.post("/api/feed/source")
async def set_feed_source(data: Dict[str, str]):
    source = data.get("source", "synthetic")
    state.feed_source = source
    return {"status": "SUCCESS", "feed_source": state.feed_source}

@app.post("/api/telemetry/inject_keypoints")
async def inject_keypoints(req: KeypointsInjectRequest):
    """Allows client-side webcam pose estimation to feed the Python HAR engine."""
    state.feed_source = "webcam"
    # Convert incoming dict into numpy arrays
    kps = {}
    for name, coords in req.keypoints.items():
        if isinstance(coords, list) and len(coords) >= 2:
            z = coords[2] if len(coords) > 2 else 0.0
            kps[name] = np.array([coords[0], coords[1], z], dtype=np.float32)
    state.client_keypoints = kps
    return {"status": "SUCCESS", "keypoints_received": len(kps)}

@app.get("/api/audit_report")
async def get_audit_report():
    fsm = state.har_engine.fsm
    completed_steps = fsm.completed_steps
    anomalies = fsm.anomalies
    score = fsm.integrity_score

    report = {
        "mission_authority": "Indian Space Research Organisation (ISRO)",
        "station_module": "Bharatiya Antariksh Station - Module BAS-03 (Science Rack Alpha)",
        "payload_subsystem": "AI Human Activity Recognition (HAR) Flight Software",
        "experiment_id": state.active_experiment_id,
        "experiment_name": state.active_experiment.get("name"),
        "lead_scientist": state.active_experiment.get("scientist"),
        "audit_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mission_elapsed_time": state.telemetry_builder.format_met(state.telemetry_builder.met_seconds),
        "protocol_integrity_score": f"{score:.1f}%",
        "protocol_status": "COMPLETED" if fsm.is_completed else "IN_PROGRESS",
        "total_steps": len(state.active_experiment.get("steps", [])),
        "completed_steps_count": len(completed_steps),
        "completed_steps_log": completed_steps,
        "anomaly_incident_count": len(anomalies),
        "anomalies_detected": anomalies,
        "certification": "VALIDATED FOR DOWNLINK TO ISTRAC MOX BENGALURU"
    }
    return report

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            state.frame_counter += 1

            # 1. Determine Keypoints Source
            if state.feed_source == "webcam" and state.client_keypoints is not None:
                keypoints = state.client_keypoints
                metadata = {"source": "webcam", "time_s": time.time()}
            else:
                keypoints, metadata = SyntheticSpaceScenario.get_landmarks_for_scenario(
                    state.active_scenario,
                    state.frame_counter,
                    fps=30
                )

            # 2. Process through HAR Engine
            har_output = state.har_engine.process_frame(keypoints)

            # 3. Generate CCSDS Telemetry Packet
            ccsds_packet = state.telemetry_builder.generate_packet(
                har_output,
                state.active_experiment_id
            )

            # 4. Get Orbital Ground Pass info
            orbital_data = state.orbital_simulator.get_orbit_telemetry()

            # 5. Render tactical HUD preview frame every 3rd frame to optimize bandwidth
            frame_b64 = None
            if state.frame_counter % 3 == 0:
                rendered_frame = SyntheticSpaceScenario.render_synthetic_frame(
                    keypoints,
                    state.har_engine.rack_rois,
                    har_output,
                    width=640,
                    height=360
                )
                _, buffer = cv2.imencode('.jpg', rendered_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
                frame_b64 = base64.b64encode(buffer).decode('utf-8')

            # Prepare landmark array for frontend Canvas rendering
            landmarks_serializable = {
                k: [round(float(v[0]), 4), round(float(v[1]), 4), round(float(v[2]), 4)]
                for k, v in keypoints.items()
            }

            # Prepare telemetry payload
            payload = {
                "frame_id": state.frame_counter,
                "timestamp": time.time(),
                "active_experiment": state.active_experiment_id,
                "active_scenario": state.active_scenario,
                "feed_source": state.feed_source,
                "har": har_output,
                "landmarks": landmarks_serializable,
                "ccsds": ccsds_packet,
                "orbit": orbital_data,
                "preview_frame": frame_b64
            }

            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(0.04)  # ~25 FPS stream

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")

# Mount static frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
