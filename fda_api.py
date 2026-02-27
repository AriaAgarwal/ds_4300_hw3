from pymongo import MongoClient

class FDA_API:

    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["fda_reports"]
        self.collection = db["reports"]

    def get_fatal_drugs(self, limit, most_frequent, outcome):
        col = self.collection

        if most_frequent:
            sort = -1
        else:
            sort = 1

        pipeline = [
            {"$unwind": "$patient.reaction"},
            {"$match": {"patient.reaction.reactionoutcome": outcome}},  # now parameterized!
            {"$unwind": "$patient.drug"},
            {"$group": {
                "_id": "$patient.drug.medicinalproduct",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": sort}},
            {"$limit": limit},
            {"$project": {"drug": "$_id", "count": 1, "_id": 0}}
        ]

        return list(self.collection.aggregate(pipeline))

    def get_common_reactions_by_sex(self, limit):
        pipeline = [
            {"$match": {"patient.patientsex": {"$in": ["1", "2"]}}},
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