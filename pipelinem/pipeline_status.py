from datetime import datetime
from database.mongo_client import pipeline_status_col

PIPELINE_ID = "main_pipeline"


def ensure_doc():

    doc = pipeline_status_col.find_one({"_id": PIPELINE_ID})

    if not doc:
        pipeline_status_col.insert_one({
            "_id": PIPELINE_ID,
            "status": "IDLE",
            "stage": None,
            "progress": 0,
            "etaMinutes": None,
            "startedAt": None,
            "finishedAt": None,
            "stopRequested": False,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })


def update_pipeline(stage=None, progress=None, eta=None, status=None):

    ensure_doc()

    update = {}

    if stage is not None:
        update["stage"] = stage

    if progress is not None:
        update["progress"] = progress

    if eta is not None:
        update["etaMinutes"] = eta

    if status is not None:
        update["status"] = status

    update["updatedAt"] = datetime.utcnow()

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {"$set": update}
    )


def set_running():

    ensure_doc()

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {
            "$set": {
                "status": "RUNNING",
                "progress": 0,
                "stage": "Starting Pipeline",
                "startedAt": datetime.utcnow(),
                "finishedAt": None,
                "stopRequested": False,
                "updatedAt": datetime.utcnow()
            }
        }
    )


def set_completed():

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {
            "$set": {
                "status": "COMPLETED",
                "stage": "Completed",
                "progress": 100,
                "etaMinutes": 0,
                "finishedAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        }
    )


def set_failed():

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {
            "$set": {
                "status": "FAILED",
                "stage": "Failed",
                "finishedAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        }
    )


def request_stop():

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {
            "$set": {
                "stopRequested": True,
                "updatedAt": datetime.utcnow()
            }
        }
    )


def stop_requested():

    doc = pipeline_status_col.find_one({"_id": PIPELINE_ID})

    if not doc:
        return False

    return doc.get("stopRequested", False)


def get_status():

    doc = pipeline_status_col.find_one({"_id": PIPELINE_ID})

    if not doc:
        return {
            "status": "IDLE"
        }

    return doc