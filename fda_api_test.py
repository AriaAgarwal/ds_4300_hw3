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

    def get_common_reactions_by_sex(self, limit, sex=None):
        """
        Get most common reactions by patient sex.
        sex: None (both), "1" (male), or "2" (female).
        """
        sex_filter = {"$in": ["1", "2"]} if sex is None else sex
        pipeline = [
            {"$match": {"patient.patientsex": sex_filter}},
            {"$unwind": "$patient.reaction"},
            {
                "$group": {
                    "_id": {
                        "sex": "$patient.patientsex",
                        "reaction": "$patient.reaction.reactionmeddrapt",
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {
                "$group": {
                    "_id": "$_id.sex",
                    "reactions": {
                        "$push": {
                            "reaction": "$_id.reaction",
                            "count": "$count",
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "sex": "$_id",
                    "reactions": {"$slice": ["$reactions", limit]},
                }
            },
            {"$sort": {"sex": 1}},
        ]

        return list(self.collection.aggregate(pipeline))

