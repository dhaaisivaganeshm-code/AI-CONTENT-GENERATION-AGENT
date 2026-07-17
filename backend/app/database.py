import copy
import logging
from types import SimpleNamespace

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from app.config import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


class _MemoryCursor:
    def __init__(self, docs: list[dict]):
        self._docs = docs
        self._index = 0

    def sort(self, field: str, direction: int = -1):
        self._docs = sorted(
            self._docs,
            key=lambda item: item.get(field, ""),
            reverse=direction == -1,
        )
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self._docs):
            raise StopAsyncIteration

        doc = self._docs[self._index]
        self._index += 1
        return copy.deepcopy(doc)


class _MemoryCollection:
    def __init__(self, name: str):
        self.name = name
        self._docs: list[dict] = []

    async def create_index(self, *args, **kwargs):
        return None

    async def find_one(self, query: dict):
        for doc in self._docs:
            if _matches_query(doc, query):
                return copy.deepcopy(doc)
        return None

    async def insert_one(self, doc: dict):
        self._docs.append(copy.deepcopy(doc))
        return SimpleNamespace(inserted_id=doc.get("_id"))

    async def update_one(self, query: dict, update: dict):
        for index, doc in enumerate(self._docs):
            if not _matches_query(doc, query):
                continue

            updated_doc = copy.deepcopy(doc)

            for key, value in update.get("$set", {}).items():
                updated_doc[key] = copy.deepcopy(value)

            for key, change in update.get("$push", {}).items():
                if isinstance(change, dict) and "$each" in change:
                    current = updated_doc.setdefault(key, [])
                    current.extend(copy.deepcopy(change["$each"]))
                else:
                    current = updated_doc.setdefault(key, [])
                    current.append(copy.deepcopy(change))

            self._docs[index] = updated_doc
            return SimpleNamespace(matched_count=1, modified_count=1)

        return SimpleNamespace(matched_count=0, modified_count=0)

    async def delete_one(self, query: dict):
        for index, doc in enumerate(self._docs):
            if _matches_query(doc, query):
                del self._docs[index]
                return SimpleNamespace(deleted_count=1)
        return SimpleNamespace(deleted_count=0)

    def find(self, query: dict):
        return _MemoryCursor([
            copy.deepcopy(doc)
            for doc in self._docs
            if _matches_query(doc, query)
        ])


class _MemoryDatabase:
    def __init__(self):
        self.users = _MemoryCollection("users")
        self.chats = _MemoryCollection("chats")


def _matches_query(doc: dict, query: dict) -> bool:
    for key, expected in query.items():
        if isinstance(expected, dict):
            if not _matches_query(doc.get(key, {}), expected):
                return False
            continue

        if doc.get(key) != expected:
            return False

    return True


async def connect_db() -> None:
    """
    Connect to MongoDB when available, otherwise fall back to an in-memory store.
    """

    global client, db

    try:
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,
        )

        await client.admin.command("ping")

        db = client[settings.mongodb_db]

        await db.users.create_index(
            "email",
            unique=True,
        )

        await db.chats.create_index(
            [
                ("user_id", 1),
                ("updated_at", -1),
            ]
        )

        logger.info("MongoDB connected successfully.")

    except Exception:
        logger.exception("MongoDB unavailable; using in-memory fallback database.")
        db = _MemoryDatabase()
        client = None


async def close_db() -> None:
    """
    Close the MongoDB connection when present.
    """

    global client

    if client is not None:
        client.close()
        client = None

        logger.info("MongoDB connection closed.")