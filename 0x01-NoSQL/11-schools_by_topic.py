#!/usr/bin/env python3
""" Module """


def schools_by_topic(mongo_collection, topic):
    """List of dictionaries representing schools matching the topic."""
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
