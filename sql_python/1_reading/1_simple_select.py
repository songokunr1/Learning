from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///thunderbird_manufacturing.db')
conn = engine.connect()

stmt = text("SELECT * FROM PRODUCT")
results = conn.execute(stmt)

print(results)

for record in results:
    print(record)