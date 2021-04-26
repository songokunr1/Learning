
from sqlalchemy import create_engine, text

conn = create_engine.connect()

stmt = text("SELECT * FROM CUSTOMER")
results = conn.execute(stmt)

for record in results:
    print(record)