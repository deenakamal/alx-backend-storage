#!/usr/bin/env python3
""" Module """


def list_all(mongo_collection):
    """ list_all mongo_collection """
    return [document for document in mongo_collection.find()]
