from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///thunderbird_manufacturing.db')
conn = engine.connect()

stmt = text("SELECT * FROM CUSTOMER LIMIT 1")
single_result = conn.execute(stmt).fetchone()

print(single_result)