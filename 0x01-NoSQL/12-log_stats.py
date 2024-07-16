#!/usr/bin/env python3
""" Module """
from pymongo import MongoClient

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection):
    """
    Provide statistics about Nginx logs stored in MongoDB.
    """
    try:
        total_logs = mongo_collection.count_documents({})
        print(f"{total_logs} logs")

        print("Methods:")
        for method in HTTP_METHODS:
            method_count = mongo_collection.count_documents({"method": method})
            print(f"\tmethod {method}: {method_count}")

        status_check_count = mongo_collection.count_documents(
                {"method": "GET", "path": "/status"}
                )
        print(f"method=GET, path=/status: {status_check_count} status check")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        client = MongoClient('mongodb://localhost:27017')
        db = client.logs
        nginx_collection = db.nginx

        log_stats(nginx_collection)

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
