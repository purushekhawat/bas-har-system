"""
Synthetic Microgravity Pose & Experiment Scenario Generator
Bharatiya Antariksh Station (BAS) - Simulation & Test Harness
Generates realistic multi-joint astronaut kinematics and synthetic camera frames.
"""

import math
import time
import numpy as np
import cv2
from typing import Dict, List, Tuple, Any

class SyntheticSpaceScenario:
    """
    Generates synthetic 33-point pose landmark sequences simulating microgravity activities.
    """

    @classmethod
    def get_landmarks_for_scenario(
        cls,
        scenario_id: str,
        frame_idx: int,
        fps: int = 30
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        """
        Returns normalized 3D keypoints for a given frame index and scenario mode.
        """
        t = frame_idx / float(fps)

        # Microgravity gentle floating oscillation (translation drift)
        drift_x = 0.02 * math.sin(t * 0.8)
        drift_y = 0.03 * math.cos(t * 0.6)

        # Default Nominal Torso Base
        center_x = 0.50 + drift_x
        center_y = 0.45 + drift_y

        roll_deg = 0.0
        pitch_deg = 0.0
        inverted = False

        if scenario_id == "inverted_floating_test":
            # Astronaut floating upside down (180 deg inverted)
            inverted = True
            roll_deg = 180.0 + 15.0 * math.sin(t * 0.5)
            pitch_deg = 150.0 + 10.0 * math.cos(t * 0.4)

        elif scenario_id == "lateral_tilt_test":
            roll_deg = 45.0 + 10.0 * math.sin(t * 0.7)

        # Base body coordinates
        torso_len = 0.28
        shoulder_width = 0.22

        # Invert or rotate if inverted scenario
        if inverted:
            # Head at bottom, hips at top
            head_y = center_y + torso_len * 0.6
            hip_y = center_y - torso_len * 0.4
            shoulder_y = center_y + torso_len * 0.2
        else:
            head_y = center_y - torso_len * 0.6
            hip_y = center_y + torso_len * 0.4
            shoulder_y = center_y - torso_len * 0.2

        nose = np.array([center_x, head_y, 0.0])
        ls = np.array([center_x - shoulder_width / 2.0, shoulder_y, 0.0])
        rs = np.array([center_x + shoulder_width / 2.0, shoulder_y, 0.0])
        lh = np.array([center_x - shoulder_width * 0.35, hip_y, 0.0])
        rh = np.array([center_x + shoulder_width * 0.35, hip_y, 0.0])

        # Hand kinematics based on scenario and time progress
        step_phase = int(t / 4.0) % 5  # Each step cycle ~4 seconds in test mode

        if scenario_id == "out_of_sequence_anomaly" and t > 3.0:
            # Force premature interaction with Centrifuge bay (Step 4/5 zone)
            lw = np.array([0.72 + 0.03 * math.sin(t * 3), 0.62 + 0.02 * math.cos(t * 3), 0.0])
            rw = np.array([0.75 + 0.02 * math.cos(t * 3), 0.60 + 0.03 * math.sin(t * 3), 0.0])
            le = (ls + lw) / 2.0 + np.array([-0.05, 0.05, 0.0])
            re = (rs + rw) / 2.0 + np.array([0.05, 0.05, 0.0])

        elif step_phase == 0 or (scenario_id == "nominal_run" and t < 5.0):
            # Phase 1: Glovebox Seal Check (Hands both in Glovebox ROI 0.15 - 0.50)
            lw = np.array([0.28 + 0.02 * math.sin(t * 2.5), 0.55 + 0.01 * math.cos(t * 2.5), 0.0])
            rw = np.array([0.38 + 0.02 * math.cos(t * 2.5), 0.52 + 0.01 * math.sin(t * 2.5), 0.0])
            le = np.array([0.22, 0.45, 0.0])
            re = np.array([0.48, 0.42, 0.0])

        elif step_phase == 1:
            # Phase 2: Retrieve Cryo-Vial (Reaching into Cryo-Stowage at top-right 0.70 - 0.95)
            rw = np.array([0.82 + 0.03 * math.sin(t * 3), 0.25 + 0.02 * math.cos(t * 3), 0.0])
            lw = np.array([0.50, 0.65, 0.0])
            re = np.array([0.72, 0.30, 0.0])
            le = np.array([0.42, 0.55, 0.0])

        elif step_phase == 2 or scenario_id == "inverted_floating_test":
            # Phase 3: Pipetting Reagent (Pipette zone 0.30 - 0.60)
            lw = np.array([0.42 + 0.01 * math.sin(t * 4), 0.58 + 0.01 * math.cos(t * 4), 0.0])
            rw = np.array([0.46 + 0.01 * math.cos(t * 4), 0.55 + 0.01 * math.sin(t * 4), 0.0])
            le = np.array([0.34, 0.50, 0.0])
            re = np.array([0.56, 0.48, 0.0])

        elif step_phase == 3:
            # Phase 4: Centrifuge Bay (0.60 - 0.90)
            lw = np.array([0.68 + 0.02 * math.sin(t * 2), 0.65, 0.0])
            rw = np.array([0.75 + 0.02 * math.cos(t * 2), 0.62, 0.0])
            le = np.array([0.58, 0.58, 0.0])
            re = np.array([0.70, 0.52, 0.0])

        else:
            # Phase 5: Cryo Archival / Seal
            lw = np.array([0.78, 0.28, 0.0])
            rw = np.array([0.82, 0.24, 0.0])
            le = np.array([0.65, 0.38, 0.0])
            re = np.array([0.72, 0.32, 0.0])

        # Legs in relaxed microgravity tuck
        lk = np.array([lh[0] - 0.08, hip_y + (0.15 if not inverted else -0.15), 0.0])
        rk = np.array([rh[0] + 0.08, hip_y + (0.15 if not inverted else -0.15), 0.0])
        la = np.array([lk[0] + 0.04, lk[1] + (0.12 if not inverted else -0.12), 0.0])
        ra = np.array([rk[0] - 0.04, rk[1] + (0.12 if not inverted else -0.12), 0.0])

        keypoints = {
            "nose": nose,
            "left_shoulder": ls,
            "right_shoulder": rs,
            "left_elbow": le,
            "right_elbow": re,
            "left_wrist": lw,
            "right_wrist": rw,
            "left_hip": lh,
            "right_hip": rh,
            "left_knee": lk,
            "right_knee": rk,
            "left_ankle": la,
            "right_ankle": ra
        }

        metadata = {
            "time_s": round(t, 2),
            "step_phase": step_phase,
            "simulated_roll": round(roll_deg, 1),
            "simulated_pitch": round(pitch_deg, 1)
        }

        return keypoints, metadata

    @classmethod
    def render_synthetic_frame(
        cls,
        keypoints: Dict[str, np.ndarray],
        rack_rois: Dict[str, Dict[str, float]],
        har_output: Dict[str, Any],
        width: int = 960,
        height: int = 540
    ) -> np.ndarray:
        """
        Renders a high-tech tactical space station camera frame with:
        - Deep space station module interior styling
        - Rack Equipment interaction zones
        - Orientation-Agnostic Skeleton HUD
        - Attitude vector and artificial horizon
        """
        # Create dark station module canvas (#0b101d)
        frame = np.full((height, width, 3), (29, 16, 11), dtype=np.uint8)

        # Subtle modular station rack grid lines
        grid_color = (45, 30, 20)
        for gx in range(0, width, 80):
            cv2.line(frame, (gx, 0), (gx, height), grid_color, 1)
        for gy in range(0, height, 80):
            cv2.line(frame, (0, gy), (width, gy), grid_color, 1)

        # Draw Science Rack Zones with tactical HUD boxes
        zone_colors = {
            "GLOVEBOX_A": (255, 180, 0),              # Cyan / Amber
            "PIPETTE_RACK": (0, 240, 255),             # Yellow
            "CENTRIFUGE_ROTATION_BAY": (255, 100, 50), # Orange / Purple
            "CRYO_STOWAGE": (240, 200, 0)              # Cyan
        }

        active_zone_names = [z['zone'] for z in har_output.get('kinematics', {}).get('active_zones', [])]

        for zname, roi in rack_rois.items():
            rx1, ry1 = int(roi['x'] * width), int(roi['y'] * height)
            rx2, ry2 = int((roi['x'] + roi['w']) * width), int((roi['y'] + roi['h']) * height)

            is_active = zname in active_zone_names
            color = (0, 255, 136) if is_active else zone_colors.get(zname, (180, 150, 100))
            thickness = 2 if is_active else 1

            # Dashed corner markers
            cl = 15
            cv2.line(frame, (rx1, ry1), (rx1 + cl, ry1), color, 2)
            cv2.line(frame, (rx1, ry1), (rx1, ry1 + cl), color, 2)
            cv2.line(frame, (rx2, ry1), (rx2 - cl, ry1), color, 2)
            cv2.line(frame, (rx2, ry1), (rx2, ry1 + cl), color, 2)
            cv2.line(frame, (rx1, ry2), (rx1 + cl, ry2), color, 2)
            cv2.line(frame, (rx1, ry2), (rx1, ry2 - cl), color, 2)
            cv2.line(frame, (rx2, ry2), (rx2 - cl, ry2), color, 2)
            cv2.line(frame, (rx2, ry2), (rx2, ry2 - cl), color, 2)

            # Zone label
            cv2.putText(
                frame,
                f"[{zname.replace('_', ' ')}]",
                (rx1 + 8, ry1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.40,
                color,
                1,
                cv2.LINE_AA
            )

        # Draw Skeleton Bones
        skeleton_links = [
            ("nose", "left_shoulder"), ("nose", "right_shoulder"),
            ("left_shoulder", "right_shoulder"),
            ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"),
            ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"),
            ("left_shoulder", "left_hip"), ("right_shoulder", "right_hip"),
            ("left_hip", "right_hip"),
            ("left_hip", "left_knee"), ("left_knee", "left_ankle"),
            ("right_hip", "right_knee"), ("right_knee", "right_ankle")
        ]

        bone_color = (255, 220, 0)  # Cyan
        for p1_name, p2_name in skeleton_links:
            if p1_name in keypoints and p2_name in keypoints:
                pt1 = (int(keypoints[p1_name][0] * width), int(keypoints[p1_name][1] * height))
                pt2 = (int(keypoints[p2_name][0] * width), int(keypoints[p2_name][1] * height))
                cv2.line(frame, pt1, pt2, bone_color, 2, cv2.LINE_AA)

        # Draw Keypoint Joints
        for kname, kpos in keypoints.items():
            px, py = int(kpos[0] * width), int(kpos[1] * height)
            jcolor = (0, 255, 120) if "wrist" in kname else (0, 200, 255)
            radius = 6 if "wrist" in kname else 4
            cv2.circle(frame, (px, py), radius, jcolor, -1, cv2.LINE_AA)
            cv2.circle(frame, (px, py), radius + 2, (255, 255, 255), 1, cv2.LINE_AA)

        # Draw HUD overlays: Attitude & Pitch/Roll
        att = har_output.get('kinematics', {}).get('attitude', {})
        roll = att.get('roll_deg', 0.0)
        pitch = att.get('pitch_deg', 0.0)
        att_mode = att.get('attitude_mode', 'NOMINAL')

        hud_text = f"ATTITUDE: {att_mode} | ROLL: {roll:+.1f} deg | PITCH: {pitch:+.1f} deg"
        cv2.putText(frame, hud_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)

        action_txt = f"ACTION: {har_output.get('detected_action')} ({int(har_output.get('action_confidence', 0)*100)}%)"
        cv2.putText(frame, action_txt, (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 136), 2, cv2.LINE_AA)

        # Check for active anomalies
        anomalies = har_output.get('anomalies', [])
        if anomalies:
            latest = anomalies[-1]
            warn_txt = f"! ALERT: {latest.get('message')}"
            cv2.putText(frame, warn_txt, (20, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 50, 255), 2, cv2.LINE_AA)

        return frame
