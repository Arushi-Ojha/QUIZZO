from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy.exc
import urllib.parse

username = "root"
host = "gondola.proxy.rlwy.net"
port = 39207
database = "railway"
password = "VxGjDwLfTbiGhkTGfqPthepCxckgVjWI"
encoded_password = urllib.parse.quote_plus(password)



DATABASE_URL = f"mysql+mysqlconnector://root:VxGjDwLfTbiGhkTGfqPthepCxckgVjWI@gondola.proxy.rlwy.net:39207/railway"
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def verify_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connection successful.")
    except sqlalchemy.exc.SQLAlchemyError as e:
        print("❌ Database connection failed.")
        print(e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

