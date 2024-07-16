#!/usr/bin/env python3
""" Module """


def update_topics(mongo_collection, name, topics):
    """Changes all topic document based on the name."""
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
