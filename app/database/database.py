from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


# ===================================================================================


load_dotenv()


password = quote_plus(os.getenv("MYSQL_PASSWORD"))

DATABASE_URL = (
    f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:"
    f"{password}@"
    f"{os.getenv('MYSQL_HOST')}:"
    f"{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DB')}"
)

#  Async Setup Using aiomysql
# DATABASE_URL = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"

print("DATABASE_URL =", DATABASE_URL)
print("USER =", os.getenv("MYSQL_USER"))
print("PASSWORD =", os.getenv("MYSQL_PASSWORD"))
print("HOST =", os.getenv("MYSQL_HOST"))
print("PORT =", os.getenv("MYSQL_PORT"))
print("DB =", os.getenv("MYSQL_DB"))
print("DATABASE_URL =", DATABASE_URL)


# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db