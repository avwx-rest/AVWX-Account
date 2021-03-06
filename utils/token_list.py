"""
Convert account token into list of tokens
"""

# stdlib
from contextlib import suppress
from os import environ
from secrets import token_urlsafe

# library
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mdb = MongoClient(environ["MONGO_URI"])


def format_token(token: dict) -> dict:
    """Updates token with new field defaults"""
    return {"_id": ObjectId(), "name": "App", "type": "app", **token}


def dev_token() -> dict:
    """Returns a new unique dev token"""
    value = "dev-" + token_urlsafe(32)[4:]
    while mdb.account.user.find_one({"token.value": value}, {"_id": 1}):
        value = "dev-" + token_urlsafe(32)[4:]
    return {
        "_id": ObjectId(),
        "name": "Development",
        "type": "dev",
        "active": True,
        "value": value,
    }


def main() -> int:
    """Convert account token into list of tokens"""
    for user in mdb.account.user.find(
        {"tokens": {"$exists": 1}}, {"token": 1, "plan": 1}
    ):
        print(user)
        tokens = []
        with suppress(KeyError):
            tokens.append(format_token(user["token"]))
        with suppress(KeyError):
            if user["plan"]["type"] != "free":
                tokens.append(dev_token())
        resp = mdb.account.user.update_one(
            {"_id": user["_id"]}, {"$set": {"tokens": tokens}}
        )
        print(resp.modified_count)
    return 0


if __name__ == "__main__":
    main()
