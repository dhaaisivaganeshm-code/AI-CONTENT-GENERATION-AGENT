from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_db():
    global client, db

    client = AsyncIOMotorClient(settings.mongodb_url)

    # Verify the connection
    await client.admin.command("ping")

    db = client[settings.mongodb_db]

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.chats.create_index(
        [("user_id", 1), ("updated_at", -1)]
    )

    print("✅ MongoDB Connected")


async def close_db():
    global client

    if client:
        client.close()
        print("🔒 MongoDB Connection Closed")