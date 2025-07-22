import argparse
import psutil
import time
import threading
import csv
import os
from datetime import datetime
import papermill as pm
from pathlib import Path

# === CLI argument parsing ===
parser = argparse.ArgumentParser(description="Profile a Jupyter notebook's resource usage.")
parser.add_argument("notebook_path", type=str, help="Path to the notebook to be executed and profiled.")
parser.add_argument("--output", type=str, default="output.ipynb", help="Path to save the executed notebook.")
parser.add_argument("--log", type=str, default="resource_log.csv", help="CSV file to save resource usage log.")
parser.add_argument("--interval", type=float, default=2.0, help="Monitoring interval in seconds.")

args = parser.parse_args()

NOTEBOOK_PATH = Path(args.notebook_path).resolve()
OUTPUT_NOTEBOOK = Path(args.output).resolve()
RESOURCE_LOG_CSV = Path(args.log).resolve()
MONITOR_INTERVAL = args.interval

if not NOTEBOOK_PATH.exists():
    raise FileNotFoundError(f"Notebook not found: {NOTEBOOK_PATH}")

# === Resource monitoring ===
resource_data = []

def monitor_resources():
    print("📈 Starting resource monitor...")
    while not getattr(monitor_thread, "stop", False):
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage(".")
        now = datetime.now()
        resource_data.append([
            now.isoformat(),
            cpu,
            mem.used / 1e9,
            mem.available / 1e9,
            mem.percent,
            disk.used / 1e9,
            disk.percent
        ])
        time.sleep(MONITOR_INTERVAL)

# === Run notebook ===
monitor_thread = threading.Thread(target=monitor_resources)
monitor_thread.start()

try:
    print(f"▶️ Running notebook: {NOTEBOOK_PATH}")
    pm.execute_notebook(
        input_path=str(NOTEBOOK_PATH),
        output_path=str(OUTPUT_NOTEBOOK),
        log_output=True
    )
finally:
    monitor_thread.stop = True
    monitor_thread.join()
    print("✅ Notebook finished. Writing resource log...")

    with open(RESOURCE_LOG_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "cpu_percent", "mem_used_GB", "mem_available_GB",
            "mem_percent", "disk_used_GB", "disk_percent"
        ])
        writer.writerows(resource_data)

    print(f"📁 Resource log saved to: {RESOURCE_LOG_CSV}")

