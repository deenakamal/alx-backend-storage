#!/usr/bin/env python3
"""
Moduel
"""
from pymongo import MongoClient


HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def display_nginx_log_stats(mongo_collection):
    """ display"""
    total_log_count = mongo_collection.count_documents({})
    print(f"{total_log_count} logs")

    print("Methods:")
    for method in HTTP_METHODS:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
    print("IPs:")
    top_ips = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


def main():
    """ main """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    display_nginx_log_stats(nginx_collection)


if __name__ == "__main__":
    main()
