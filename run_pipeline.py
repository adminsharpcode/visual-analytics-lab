"""
Visual Analytics Lab (MACSE603) - Final Project Pipeline Runner
Smart Energy Consumption Visualization Dashboard Using Power BI
Team: Vedant Nimkar (26MML0045), Jitesh Bobde (26MML0025), Ayush Sharma (26MML0043)
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.join(BASE_DIR, "Project_SmartEnergy_PowerBI", "pipeline")
if PIPELINE_DIR not in sys.path:
    sys.path.insert(0, PIPELINE_DIR)

from pipeline_orchestrator import PipelineOrchestrator

if __name__ == "__main__":
    print(f"Executing End-to-End Visual Analytics Pipeline from {BASE_DIR}...")
    orchestrator = PipelineOrchestrator()
    summary = orchestrator.run_all()
