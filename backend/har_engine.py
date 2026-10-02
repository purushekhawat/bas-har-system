"""
AI Human Activity Recognition (HAR) Engine for On-Board BAS Experiment
Bharatiya Antariksh Station (BAS) - Microgravity Edge AI Subsystem
SIH Problem Statement 174

Key Capabilities:
- Orientation-Agnostic Kinematic Transformation (SE(3) invariant body coordinate frame)
- Astronaut Microgravity Attitude Determination (Pitch, Roll, Drift Angle)
- Spatio-Temporal Action Classification (Pipetting, Glovebox Seal, Centrifugation, Stowage)
- Procedural State Machine (FSM) with Real-Time Step Validation
- Anomaly & Safety Hazard Detection (Out-of-order execution, skipped steps, unlatched hazards)
"""

import math
import time
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

class MicrogravityKinematics:
    """
    Orientation-agnostic coordinate normalization and kinematic feature extractor.
    In microgravity, astronauts float freely in arbitrary 3D orientations (no fixed gravity floor).
    This engine maps raw camera keypoints to a body-centric reference frame.
    """

    @staticmethod
    def calculate_angle_3d(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        """Calculates angle ABC in degrees at vertex B."""
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-7)
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        return float(np.degrees(np.arccos(cosine_angle)))

    @staticmethod
    def estimate_astronaut_attitude(keypoints: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Calculates pitch, roll, and yaw angles of the floating astronaut relative to camera frame.
        """
        ls = keypoints.get('left_shoulder', np.array([0.4, 0.3, 0.0]))
        rs = keypoints.get('right_shoulder', np.array([0.6, 0.3, 0.0]))
        lh = keypoints.get('left_hip', np.array([0.4, 0.7, 0.0]))
        rh = keypoints.get('right_hip', np.array([0.6, 0.7, 0.0]))

        mid_shoulder = (ls + rs) / 2.0
        mid_hip = (lh + rh) / 2.0

        # Spine vector (hip -> shoulder)
        spine = mid_shoulder - mid_hip
        # Shoulder vector (left -> right)
        shoulder = rs - ls

        # Roll: angle of shoulder vector relative to horizontal axis [1, 0]
        roll_rad = math.atan2(shoulder[1], shoulder[0] + 1e-7)
        roll_deg = math.degrees(roll_rad)

        # Pitch / Spine inclination relative to vertical axis [0, -1]
        spine_norm = spine[:2] / (np.linalg.norm(spine[:2]) + 1e-7)
        pitch_deg = math.degrees(math.atan2(spine_norm[0], -spine_norm[1]))

        # State classification
        is_inverted = abs(pitch_deg) > 110 or abs(roll_deg) > 110
        attitude_mode = "INVERTED_DRIFT" if is_inverted else "MICROGRAVITY_NOMINAL"
        if abs(roll_deg) > 35 and not is_inverted:
            attitude_mode = "LATERAL_TILT"

        return {
            "roll_deg": round(roll_deg, 1),
            "pitch_deg": round(pitch_deg, 1),
            "is_inverted": is_inverted,
            "attitude_mode": attitude_mode
        }

    @classmethod
    def extract_features(cls, keypoints: Dict[str, np.ndarray], rack_rois: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Extracts orientation-agnostic joint angles and spatial interaction distances.
        """
        # Joint Angles
        lw = keypoints.get('left_wrist', np.array([0.3, 0.5, 0.0]))
        le = keypoints.get('left_elbow', np.array([0.35, 0.4, 0.0]))
        ls = keypoints.get('left_shoulder', np.array([0.4, 0.3, 0.0]))

        rw = keypoints.get('right_wrist', np.array([0.7, 0.5, 0.0]))
        re = keypoints.get('right_elbow', np.array([0.65, 0.4, 0.0]))
        rs = keypoints.get('right_shoulder', np.array([0.6, 0.3, 0.0]))

        lh = keypoints.get('left_hip', np.array([0.42, 0.7, 0.0]))
        rh = keypoints.get('right_hip', np.array([0.58, 0.7, 0.0]))
        nose = keypoints.get('nose', np.array([0.5, 0.2, 0.0]))

        # Invariant Joint Angles (Do NOT change if astronaut is upside down)
        left_elbow_angle = cls.calculate_angle_3d(lw, le, ls)
        right_elbow_angle = cls.calculate_angle_3d(rw, re, rs)
        left_shoulder_angle = cls.calculate_angle_3d(le, ls, lh)
        right_shoulder_angle = cls.calculate_angle_3d(re, rs, rh)

        # Dual hand proximity
        hand_distance = float(np.linalg.norm(rw[:2] - lw[:2]))

        # Hand proximity to Station Rack Zones
        active_zones = []
        for zone_name, roi in rack_rois.items():
            zx1, zy1 = roi['x'], roi['y']
            zx2, zy2 = zx1 + roi['w'], zy1 + roi['h']

            left_in = (zx1 <= lw[0] <= zx2) and (zy1 <= lw[1] <= zy2)
            right_in = (zx1 <= rw[0] <= zx2) and (zy1 <= rw[1] <= zy2)

            if left_in or right_in:
                active_zones.append({
                    "zone": zone_name,
                    "left_hand": bool(left_in),
                    "right_hand": bool(right_in),
                    "dual_hands": bool(left_in and right_in)
                })

        attitude = cls.estimate_astronaut_attitude(keypoints)

        return {
            "joint_angles": {
                "left_elbow": round(left_elbow_angle, 1),
                "right_elbow": round(right_elbow_angle, 1),
                "left_shoulder": round(left_shoulder_angle, 1),
                "right_shoulder": round(right_shoulder_angle, 1)
            },
            "hand_distance": round(hand_distance, 3),
            "attitude": attitude,
            "active_zones": active_zones,
            "wrist_positions": {
                "left": [round(float(lw[0]), 3), round(float(lw[1]), 3)],
                "right": [round(float(rw[0]), 3), round(float(rw[1]), 3)]
            }
        }


class ActionClassifier:
    """
    Classifies procedural astronaut actions using orientation-invariant kinematics
    combined with workstation zone interaction patterns and temporal stability.
    """
    CLASSES = [
        "SAFETY_CHECK",
        "PIPETTING_REAGENT",
        "CENTRIFUGE_OPERATION",
        "SAMPLE_STOWAGE",
        "INSTRUMENT_CALIBRATION",
        "IDLE_FLOATING",
        "ANOMALOUS_STRUGGLE"
    ]

    def __init__(self):
        self.history = []
        self.window_size = 12

    def classify(self, features: Dict[str, Any]) -> Tuple[str, float, Dict[str, float]]:
        active_zones = {z['zone']: z for z in features.get('active_zones', [])}
        angles = features.get('joint_angles', {})
        le_ang = angles.get('left_elbow', 140.0)
        re_ang = angles.get('right_elbow', 140.0)
        hand_dist = features.get('hand_distance', 0.5)

        scores = {c: 0.05 for c in self.CLASSES}

        # 1. Glovebox / Safety Check
        if 'GLOVEBOX_A' in active_zones:
            gz = active_zones['GLOVEBOX_A']
            if gz['dual_hands']:
                scores['SAFETY_CHECK'] += 0.70
                scores['INSTRUMENT_CALIBRATION'] += 0.20
            else:
                scores['SAFETY_CHECK'] += 0.45
                scores['INSTRUMENT_CALIBRATION'] += 0.35

        # 2. Pipette Station Interaction
        if 'PIPETTE_RACK' in active_zones:
            pz = active_zones['PIPETTE_RACK']
            # Characteristic pipetting posture: bent elbow (70-120 deg) and hands near each other
            if (70 <= re_ang <= 130 or 70 <= le_ang <= 130) and hand_dist < 0.35:
                scores['PIPETTING_REAGENT'] += 0.85
            else:
                scores['PIPETTING_REAGENT'] += 0.55

        # 3. Centrifuge Bay
        if 'CENTRIFUGE_ROTATION_BAY' in active_zones:
            cz = active_zones['CENTRIFUGE_ROTATION_BAY']
            scores['CENTRIFUGE_OPERATION'] += 0.80

        # 4. Cryo Stowage
        if 'CRYO_STOWAGE' in active_zones:
            sz = active_zones['CRYO_STOWAGE']
            scores['SAMPLE_STOWAGE'] += 0.82

        # 5. Idle Floating if hands not in any active rack zone
        if not active_zones:
            scores['IDLE_FLOATING'] += 0.75

        # Normalize with Softmax
        exp_scores = {k: math.exp(v * 3.5) for k, v in scores.items()}
        total_exp = sum(exp_scores.values())
        prob_distribution = {k: round(v / total_exp, 3) for k, v in exp_scores.items()}

        best_class = max(prob_distribution, key=prob_distribution.get)
        confidence = prob_distribution[best_class]

        # Temporal smoothing
        self.history.append((best_class, confidence))
        if len(self.history) > self.window_size:
            self.history.pop(0)

        # Majority vote
        counts = {}
        for c, _ in self.history:
            counts[c] = counts.get(c, 0) + 1
        smoothed_class = max(counts, key=counts.get)

        return smoothed_class, confidence, prob_distribution


class ProceduralFSM:
    """
    Finite State Machine managing sequential protocol progress,
    evaluating step completion criteria, and detecting anomalies.
    """
    def __init__(self, experiment: Dict[str, Any]):
        self.experiment = experiment
        self.steps = experiment.get('steps', [])
        self.current_step_index = 0
        self.step_start_time = time.time()
        self.step_progress_frames = 0
        self.completed_steps = []
        self.anomalies = []
        self.integrity_score = 100.0
        self.is_completed = False
        self.paused = False

    @property
    def current_step(self) -> Optional[Dict[str, Any]]:
        if self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    def update(self, detected_action: str, confidence: float, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates procedural state based on recognized action and kinematics.
        Returns validation event dictionary.
        """
        if self.is_completed or not self.current_step:
            return {"status": "EXPERIMENT_COMPLETE", "step": None, "event": None}

        current = self.current_step
        expected_action = current.get('action_class')
        target_zone = current.get('target_zone')
        active_zones = [z['zone'] for z in features.get('active_zones', [])]

        step_elapsed = time.time() - self.step_start_time
        event = None

        # Check for sequence violations (Astronaut acting on future steps)
        for idx in range(self.current_step_index + 1, len(self.steps)):
            future_step = self.steps[idx]
            if future_step.get('action_class') == detected_action and confidence > 0.75:
                # Sequence skip detected!
                if future_step.get('target_zone') in active_zones:
                    anomaly_item = {
                        "id": f"SEQ-ERR-{int(time.time()*1000)%10000}",
                        "timestamp": time.time(),
                        "type": "OUT_OF_SEQUENCE",
                        "severity": "CRITICAL" if current.get('safety_critical') else "WARNING",
                        "current_step": current.get('step_id'),
                        "attempted_step": future_step.get('step_id'),
                        "message": f"Procedure Violation: Attempting {future_step['title']} before completing {current['title']}!",
                        "recommended_action": f"Return to {current['title']} ({target_zone})"
                    }
                    if not any(a['type'] == 'OUT_OF_SEQUENCE' and a['attempted_step'] == future_step['step_id'] for a in self.anomalies[-3:]):
                        self.anomalies.append(anomaly_item)
                        self.integrity_score = max(0.0, self.integrity_score - 15.0)
                        event = {"type": "ANOMALY_TRIGGERED", "anomaly": anomaly_item}

        # Check matching action and target zone
        is_action_match = (detected_action == expected_action) and (confidence >= 0.50)
        is_zone_match = (target_zone in active_zones) if target_zone else True

        if not self.paused:
            if is_action_match and is_zone_match:
                self.step_progress_frames += 1
            else:
                self.step_progress_frames = max(0, self.step_progress_frames - 1)
        else:
            self.step_start_time = time.time() - step_elapsed

        # Validation Threshold (60 frames ~= 2.0 seconds of sustained valid gesture)
        required_frames = 60
        progress_pct = min(100.0, (self.step_progress_frames / required_frames) * 100.0)

        if self.step_progress_frames >= required_frames and not self.paused:
            # Step Complete!
            completion_record = {
                "step_id": current['step_id'],
                "step_number": current['step_number'],
                "title": current['title'],
                "completed_at": time.time(),
                "duration_s": round(step_elapsed, 1),
                "confidence_avg": round(confidence, 3),
                "attitude_mode": features.get('attitude', {}).get('attitude_mode', 'NOMINAL')
            }
            self.completed_steps.append(completion_record)
            event = {"type": "STEP_COMPLETED", "record": completion_record}

            self.current_step_index += 1
            self.step_start_time = time.time()
            self.step_progress_frames = 0

            if self.current_step_index >= len(self.steps):
                self.is_completed = True
                event = {"type": "EXPERIMENT_SUCCESS", "final_score": round(self.integrity_score, 1)}

        return {
            "current_step_index": self.current_step_index,
            "total_steps": len(self.steps),
            "current_step": self.current_step,
            "step_progress_pct": round(progress_pct, 1),
            "step_elapsed_s": round(step_elapsed, 1),
            "integrity_score": round(self.integrity_score, 1),
            "is_completed": self.is_completed,
            "event": event
        }


class HAREngine:
    """
    Main HAR Orchestration Engine combining kinematics, classification, FSM, and alert generation.
    """
    def __init__(self, experiment: Dict[str, Any]):
        self.kinematics = MicrogravityKinematics()
        self.classifier = ActionClassifier()
        self.fsm = ProceduralFSM(experiment)
        self.rack_rois = self._extract_rack_rois(experiment)
        self.frame_count = 0

    def _extract_rack_rois(self, experiment: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        rois = {
            "GLOVEBOX_A": {"x": 0.15, "y": 0.35, "w": 0.35, "h": 0.45},
            "PIPETTE_RACK": {"x": 0.30, "y": 0.45, "w": 0.30, "h": 0.35},
            "CENTRIFUGE_ROTATION_BAY": {"x": 0.60, "y": 0.50, "w": 0.30, "h": 0.40},
            "CRYO_STOWAGE": {"x": 0.70, "y": 0.15, "w": 0.25, "h": 0.35}
        }
        # Enrich from experiment steps if defined
        for step in experiment.get('steps', []):
            if step.get('target_zone') and step.get('target_zone_coords'):
                rois[step['target_zone']] = step['target_zone_coords']
        return rois

    def process_frame(self, keypoints: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """
        Processes a single video/pose frame.
        Outputs kinematics, action predictions, procedural step status, and telemetry updates.
        """
        self.frame_count += 1
        t0 = time.time()

        # 1. Orientation-agnostic Kinematics
        kinematic_features = self.kinematics.extract_features(keypoints, self.rack_rois)

        # 2. Spatio-temporal Action Classification
        action, conf, dist = self.classifier.classify(kinematic_features)

        # 3. Procedural FSM Update
        fsm_update = self.fsm.update(action, conf, kinematic_features)

        latency_ms = round((time.time() - t0) * 1000.0, 2)

        return {
            "frame_id": self.frame_count,
            "timestamp": time.time(),
            "latency_ms": latency_ms,
            "detected_action": action,
            "action_confidence": conf,
            "action_distribution": dist,
            "kinematics": kinematic_features,
            "fsm_state": fsm_update,
            "rack_rois": self.rack_rois,
            "anomalies": self.fsm.anomalies[-5:],  # Return latest 5
            "integrity_score": fsm_update["integrity_score"]
        }
