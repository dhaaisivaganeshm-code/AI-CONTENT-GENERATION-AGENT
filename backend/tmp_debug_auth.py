import asyncio
import app.database as db
import app.routers.auth as auth
import app.schemas.auth as schema

async def main():
    await db.connect_db()
    print('db', db.db)
    req = schema.RegisterRequest(name='Test User', email='test@example.com', password='password123')
    print(req)
    print(await auth.register(req))

asyncio.run(main())
