# imports
from pymongo import MongoClient

# Creates a class for the FDA API
class FDA_API:

    def __init__(self):
        # Connects to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        # Access the fda_reports database
        db = client["fda_reports"]
        # Access the reports collection
        self.collection = db["reports"]

    def get_drugs_by_outcome(self, limit, most_frequent, outcome):
        """
        Gets the counts of most frequent or least frequent drugs by outcome type
        limit : Number of reports, most_frequent: Most or least frequent events,
        outcome: 1 (Recovered), 2 (Recovering), 3 (Resolving),
        4 (Recovered with permanent damage), 5 (Fatal), 6 (Unknown)
        """

        if most_frequent:
            sort = -1
        else:
            sort = 1

        pipeline = [
            {"$unwind": "$patient.reaction"},
            {"$match": {"patient.reaction.reactionoutcome": outcome}},
            {"$unwind": "$patient.drug"},
            {"$group": {
                "_id": "$patient.drug.medicinalproduct",
                "report_ids": {"$addToSet": "$safetyreportid"}
            }},
            {"$project": {
                "drug": "$_id",
                "fatal_count": {"$size": "$report_ids"},
                "_id": 0
            }},
            {"$sort": {"fatal_count": sort}},
            {"$limit": limit}
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

    def get_outcomes_by_age_bucket(self, bucket_size=10):
        """
        Parameters
        ----------
        bucket_size : int   size of age groups e.g. 10 = (0-10, 10-20, 20-30...)
        """
        pipeline = [
            {"$match": {"patient.patientonsetage": {"$exists": True}}},
            {"$addFields": {
                "age_bucket": {
                    "$multiply": [
                        {"$floor": {"$divide": [{"$toInt": "$patient.patientonsetage"}, bucket_size]}},
                        bucket_size
                    ]
                }
            }},
            {"$group": {
                "_id": {"age_bucket": "$age_bucket", "serious": "$serious"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.age_bucket": 1}}
        ]

        return list(self.collection.aggregate(pipeline))
