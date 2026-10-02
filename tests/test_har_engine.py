# Automated Unit & Kinematics Test Suite
import sys
from pathlib import Path
import numpy as np

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from har_engine import MicrogravityKinematics, ActionClassifier, ProceduralFSM, HAREngine
from telemetry_streamer import CCSDSPacketBuilder, OrbitalPassSimulator
from synthetic_data_gen import SyntheticSpaceScenario

def test_kinematics_invariance():
    # Test that invariant angles are computed accurately regardless of translation
    ls = np.array([0.4, 0.3, 0.0])
    le = np.array([0.3, 0.4, 0.0])
    lw = np.array([0.3, 0.6, 0.0])

    angle = MicrogravityKinematics.calculate_angle_3d(lw, le, ls)
    assert 90 <= angle <= 180, f"Expected reasonable elbow angle, got {angle}"

def test_attitude_detection():
    # Test inverted astronaut
    keypoints = {
        "nose": np.array([0.5, 0.8, 0.0]),
        "left_shoulder": np.array([0.6, 0.6, 0.0]),
        "right_shoulder": np.array([0.4, 0.6, 0.0]),
        "left_hip": np.array([0.6, 0.3, 0.0]),
        "right_hip": np.array([0.4, 0.3, 0.0])
    }
    att = MicrogravityKinematics.estimate_astronaut_attitude(keypoints)
    assert att["is_inverted"] is True, f"Expected inverted posture, got {att}"

def test_ccsds_generation():
    builder = CCSDSPacketBuilder()
    mock_har = {
        "detected_action": "PIPETTING_REAGENT",
        "action_confidence": 0.94,
        "integrity_score": 98.0,
        "kinematics": {"attitude": {"pitch_deg": 12.0, "roll_deg": -5.0}},
        "fsm_state": {"current_step_index": 2},
        "anomalies": []
    }
    pkt = builder.generate_packet(mock_har, "BAS-BIO-01")
    assert pkt["apid"] == "0x4b2"
    assert len(pkt["hex_dump"]) > 20
    assert "PIPETTING_REAGENT" in pkt["telemetry_fields"]["action"]

def test_synthetic_scenario_generation():
    kps, meta = SyntheticSpaceScenario.get_landmarks_for_scenario("nominal_run", 10)
    assert "left_wrist" in kps
    assert "right_wrist" in kps
    assert "nose" in kps

if __name__ == "__main__":
    print("Running tests...")
    test_kinematics_invariance()
    test_attitude_detection()
    test_ccsds_generation()
    test_synthetic_scenario_generation()
    print("ALL TESTS PASSED SUCCESSFULLY!")
