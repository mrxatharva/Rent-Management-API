# create_tables.py

from sqlalchemy import *

DATABASE_URL = "postgresql://neondb_owner:npg_ubcCS7d0YUnz@ep-fancy-meadow-apocfv7f.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(100)),
    Column("password", String(255))
)

tenants = Table(
    "tenants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("phone", String(20)),
    Column("property_type", String(50)),
    Column("property_number", String(50)),
    Column("deposit", Float),
    Column("deposit_mode", String(50))
)

rent = Table(
    "rent",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tenant_id", Integer),
    Column("month", String(20)),
    Column("amount", Float),
    Column("transaction_id", String(100)),
    Column("payment_mode", String(50))
)

metadata.create_all(engine)

print("Database Created")