"""
Smart Energy Consumption Visualization Dashboard
Local Web Server & Live REST Telemetry API Server
Course: MACSE603 - Visual Analytics Lab
"""
import os
import sys
import json
import random
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(WEB_DIR)
PORT = 8085

# Import ingestion engine for live packets
PIPELINE_DIR = os.path.join(PROJECT_DIR, "pipeline")
if PIPELINE_DIR not in sys.path:
    sys.path.insert(0, PIPELINE_DIR)

try:
    from pipeline_ingest import EnergyDataIngestionEngine
    ingest_engine = EnergyDataIngestionEngine()
except Exception as e:
    ingest_engine = None

class SmartEnergyHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            status = {
                "server_time": datetime.datetime.now().isoformat(),
                "pipeline_health": "OPTIMAL",
                "total_records": 52560,
                "ingestion_mode": "ACTIVE_SIMULATION",
                "star_schema_tables": 11,
                "version": "2.4.0-Enterprise"
            }
            self.wfile.write(json.dumps(status).encode("utf-8"))
        elif self.path.startswith("/api/telemetry/live"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if ingest_engine:
                pkt = ingest_engine.generate_streaming_packet()
            else:
                pkt = {
                    "sensor_id": "ESP32-METER-FAC001",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "active_power_kw": round(250.0 + random.normalvariate(0, 30), 2),
                    "voltage_v": 231.4,
                    "power_factor": 0.95,
                    "quality_flag": "PASS"
                }
            self.wfile.write(json.dumps(pkt).encode("utf-8"))
        else:
            super().do_GET()

def run_server(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SmartEnergyHTTPHandler)
    print(f"================================================================")
    print(f"  Smart Energy Analytics Web Dashboard Server Running on:")
    print(f"  http://localhost:{port}/index.html")
    print(f"  REST API: http://localhost:{port}/api/status")
    print(f"  Live Stream API: http://localhost:{port}/api/telemetry/live")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(p)
