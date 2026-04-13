from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/?replicaSet=rs0"

client = MongoClient(MONGO_URL)

db = client["iccsdb"]

identities_col = db["identities"]
observations_col = db["identity_observations"]
patterns_col = db["patterns"]
anomalies_col = db["anomalies"]

pipeline_status_col = db["pipeline_status"]