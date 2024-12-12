from app.backend.db import sessionLocal

async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()