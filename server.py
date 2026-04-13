from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from threading import Thread

from pipeline import run_pipeline

from pipelinem.pipeline_status import (
    set_running,
    set_completed,
    set_failed,
    get_status,
    request_stop,
    stop_requested
)

app = FastAPI()


# ---------------------------
# PIPELINE THREAD
# ---------------------------

def pipeline_worker():

    try:

        set_running()

        run_pipeline()

        if stop_requested():
            print("Pipeline stopped by user")
            set_failed()
            return

        set_completed()

    except Exception as e:

        print("Pipeline error:", e)

        set_failed()

# ---------------------------
# START PIPELINE
# ---------------------------

@app.post("/run-pipeline")
def run():

    status = get_status()

    if status["status"] == "RUNNING":

        return {
            "success": False,
            "message": "Pipeline already running"
        }

    thread = Thread(target=pipeline_worker)
    thread.start()

    return {
        "success": True,
        "message": "Pipeline started"
    }


# ---------------------------
# STOP PIPELINE
# ---------------------------

@app.post("/stop-pipeline")
def stop():

    request_stop()

    return {
        "success": True,
        "message": "Stop requested"
    }


# ---------------------------
# STATUS
# ---------------------------

@app.get("/pipeline-status")
def status():

    return {
        "success": True,
        "data": get_status()
    }


# ---------------------------
# IMAGE HOSTING
# ---------------------------

app.mount(
    "/detections",
    StaticFiles(directory="detections"),
    name="detections"
)