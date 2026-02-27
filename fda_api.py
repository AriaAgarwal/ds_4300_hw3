from pymongo import MongoClient

class FDA_API:

    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["fda_reports"]
        self.collection = db["reports"]

    def get_fatal_drugs(self, limit, fatal):
        col = self.collection

        if fatal:
            sort = 1
        else:
            sort = -1

        pipeline = [
            {"$unwind": "$patient.reaction"},
            {"$match": {"patient.reaction.reactionoutcome": "5"}},
            {"$unwind": "$patient.drug"},
            {"$group": {
                "_id": "$patient.drug.medicinalproduct",
                "fatal_count": {"$sum": 1}
            }},
            {"$sort": {"fatal_count": sort}},
            {"$limit": limit},
            {"$project": {"drug": "$_id", "fatal_count": 1, "_id": 0}}
        ]

        return list(self.collection.aggregate(pipeline))
