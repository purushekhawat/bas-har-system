"""
CCSDS Telemetry Streamer & Orbital Pass Simulator
Bharatiya Antariksh Station (BAS) - Subsystem APID 0x04B2 (AI-HAR-PAYLOAD)
Conforming to CCSDS 133.0-B-1 Space Packet Protocol
"""

import time
import struct
import math
from typing import Dict, Any, List, Optional

class CCSDSPacketBuilder:
    """
    Constructs CCSDS compliant Space Telemetry Packets for on-board BAS experiment tracking.
    """
    APID_HAR = 0x04B2  # 1202 in decimal: Bharatiya Antariksh Station AI HAR Subsystem
    ACTION_CODE_MAP = {
        "IDLE_FLOATING": 0x01,
        "SAFETY_CHECK": 0x02,
        "SAMPLE_STOWAGE": 0x03,
        "PIPETTING_REAGENT": 0x04,
        "CENTRIFUGE_OPERATION": 0x05,
        "INSTRUMENT_CALIBRATION": 0x06,
        "ANOMALOUS_STRUGGLE": 0xEE
    }

    def __init__(self):
        self.packet_seq_count = 0
        self.mission_start_time = time.time() - 14820  # Simulate MET 04:07:00

    @property
    def met_seconds(self) -> int:
        return int(time.time() - self.mission_start_time)

    def generate_packet(self, har_output: Dict[str, Any], experiment_id: str) -> Dict[str, Any]:
        """
        Generates binary CCSDS packet and formatted telemetry object.
        """
        self.packet_seq_count = (self.packet_seq_count + 1) % 16384  # 14-bit roll

        action_str = har_output.get("detected_action", "IDLE_FLOATING")
        action_code = self.ACTION_CODE_MAP.get(action_str, 0x00)
        confidence = int(har_output.get("action_confidence", 0.0) * 100)
        integrity = int(har_output.get("integrity_score", 100))

        attitude = har_output.get("kinematics", {}).get("attitude", {})
        pitch_int16 = int(np_clip(attitude.get("pitch_deg", 0.0) * 10, -32768, 32767))
        roll_int16 = int(np_clip(attitude.get("roll_deg", 0.0) * 10, -32768, 32767))

        fsm = har_output.get("fsm_state", {})
        step_idx = fsm.get("current_step_index", 0) + 1
        anomalies = har_output.get("anomalies", [])
        anomaly_flag = 0 if len(anomalies) == 0 else 1

        # 1. Primary Header (6 bytes)
        # Packet ID: Version(3b=0) + Type(1b=0) + SecHdr(1b=1) + APID(11b=0x04B2)
        packet_id = (0 << 13) | (1 << 11) | (self.APID_HAR & 0x07FF)
        # Packet Sequence Control: SeqFlags(2b=3 unsegmented) + SeqCount(14b)
        packet_seq_ctrl = (3 << 14) | (self.packet_seq_count & 0x3FFF)
        # User data length: 16 bytes payload + 6 bytes secondary header - 1
        data_length = 21

        primary_hdr = struct.pack(">HHH", packet_id, packet_seq_ctrl, data_length)

        # 2. Secondary Header (6 bytes MET)
        met_sec = self.met_seconds
        met_subsec = int((time.time() % 1.0) * 65535)
        sec_hdr = struct.pack(">IH", met_sec, met_subsec)

        # 3. Payload (14 bytes)
        exp_byte = 0x01 if "BIO" in experiment_id else (0x02 if "MAT" in experiment_id else 0x03)
        payload = struct.pack(
            ">BBBhhBBB",
            exp_byte,
            step_idx,
            action_code,
            pitch_int16,
            roll_int16,
            confidence,
            integrity,
            anomaly_flag
        )

        # 4. CRC-16 Checksum (2 bytes)
        raw_body = primary_hdr + sec_hdr + payload
        crc = self._crc16(raw_body)
        full_packet_bytes = raw_body + struct.pack(">H", crc)

        hex_dump = " ".join(f"{b:02X}" for b in full_packet_bytes)

        return {
            "apid": hex(self.APID_HAR),
            "seq_count": self.packet_seq_count,
            "met_timestamp": self.format_met(met_sec),
            "epoch_utc": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "packet_size_bytes": len(full_packet_bytes),
            "hex_dump": hex_dump,
            "telemetry_fields": {
                "action": action_str,
                "confidence_pct": confidence,
                "step_number": step_idx,
                "pitch_deg": round(pitch_int16 / 10.0, 1),
                "roll_deg": round(roll_int16 / 10.0, 1),
                "integrity_score": integrity,
                "anomaly_active": anomaly_flag == 1
            }
        }

    @staticmethod
    def _crc16(data: bytes) -> int:
        crc = 0xFFFF
        for b in data:
            crc ^= (b << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
        return crc

    @staticmethod
    def format_met(total_seconds: int) -> str:
        hours = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        return f"{hours:02d}:{mins:02d}:{secs:02d}"


def np_clip(v: float, min_v: float, max_v: float) -> float:
    return max(min_v, min(max_v, v))


class OrbitalPassSimulator:
    """
    Simulates Bharatiya Antariksh Station (BAS) orbit (408 km LEO, 51.6° inc)
    and communication pass windows with ISRO ground stations (ISTRAC).
    """
    STATIONS = [
        {"name": "ISTRAC BENGALURU", "country": "India", "elevation": "48°", "status": "ACTIVE_LINK", "downlink_rate": "150 Mbps"},
        {"name": "ISTRAC PORT BLAIR", "country": "India", "elevation": "32°", "status": "STANDBY", "downlink_rate": "100 Mbps"},
        {"name": "ISTRAC MAURITIUS", "country": "Mauritius", "elevation": "12°", "status": "UPCOMING", "downlink_rate": "50 Mbps"},
        {"name": "SVALBARD STATION", "country": "Norway", "elevation": "0°", "status": "BELOW_HORIZON", "downlink_rate": "0 Mbps"},
        {"name": "ORBITAL BLACKOUT WINDOW", "country": "Indian Ocean", "elevation": "N/A", "status": "BUFFERING_EDGE", "downlink_rate": "0 Mbps"}
    ]

    def __init__(self):
        self.orbit_number = 1420
        self.orbit_period_s = 92.5 * 60  # 92.5 min orbit

    def get_orbit_telemetry(self) -> Dict[str, Any]:
        t = time.time()
        phase = (t % self.orbit_period_s) / self.orbit_period_s

        # Simulating station pass rotation
        station_idx = int(phase * len(self.STATIONS)) % len(self.STATIONS)
        active_station = self.STATIONS[station_idx]

        # Latitude / Longitude ground track simulation
        lat = round(51.6 * math.sin(phase * 2 * math.pi), 2)
        lon = round(((phase * 360.0 * 16) % 360) - 180.0, 2)

        # Contact remaining
        remaining_contact_s = int((1.0 - (phase * len(self.STATIONS) % 1.0)) * 600)

        return {
            "orbit_id": f"BAS-ORBIT-{self.orbit_number}",
            "altitude_km": 408.2,
            "velocity_kms": 7.66,
            "inclination_deg": 51.64,
            "latitude": lat,
            "longitude": lon,
            "ground_station": active_station["name"],
            "link_status": active_station["status"],
            "downlink_rate": active_station["downlink_rate"],
            "contact_remaining": f"{remaining_contact_s // 60:02d}:{remaining_contact_s % 60:02d}",
            "buffered_packets_edge": 0 if "ACTIVE" in active_station["status"] else 42
        }
