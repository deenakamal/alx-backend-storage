#!/usr/bin/env python3
""" Module """


def top_students(mongo_collection):
    """
    List of dictionaries representing students sorted by averageScore.
    """
    pipeline = [
        {
            "$unwind": "$topics"  # Unwind the topics array
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}  # Sort by averageScore descending
        }
    ]

    students = list(mongo_collection.aggregate(pipeline))
    return students
