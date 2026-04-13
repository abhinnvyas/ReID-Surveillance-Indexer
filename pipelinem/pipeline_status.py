from datetime import datetime
from database.mongo_client import pipeline_status_col


PIPELINE_ID = "main_pipeline"


def get_doc():
    return pipeline_status_col.find_one({"_id": PIPELINE_ID})


def ensure_doc():

    doc = get_doc()

    if not doc:
        pipeline_status_col.insert_one({
            "_id": PIPELINE_ID,
            "status": "IDLE",
            "startedAt": None,
            "finishedAt": None,
            "stopRequested": False,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })


def set_running():

    ensure_doc()

    pipeline_status_col.update_one(
        {"_id": PIPELINE_ID},
        {
            "$set": {
                "status": "RUNNING",
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

    doc = get_doc()

    if not doc:
        return False

    return doc.get("stopRequested", False)


def get_status():

    doc = get_doc()

    if not doc:
        return {
            "status": "IDLE",
            "startedAt": None,
            "finishedAt": None
        }

    return {
        "status": doc["status"],
        "startedAt": doc.get("startedAt"),
        "finishedAt": doc.get("finishedAt")
    }