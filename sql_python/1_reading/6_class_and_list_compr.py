from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///thunderbird_manufacturing.db')
conn = engine.connect()


class Customer:
    def __init__(self, record):
        self.id = int(record["CUSTOMER_ID"])
        self.name = record["CUSTOMER_NAME"]
        self.address = record["ADDRESS"]
        self.city = record["CITY"]
        self.state = record["STATE"]
        self.zip = int(record["ZIP"])
        self.category = record["CATEGORY"]

    def __repr__(self):
        return "{0} - {1}".format(self.id, self.name)


all_customers = [Customer(record) for record in conn.execute(text("SELECT * FROM CUSTOMER"))]

print(all_customers)