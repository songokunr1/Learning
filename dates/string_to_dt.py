from datetime import datetime
today = datetime.today()
today_string = "4/10/2021"
dt_object1 = datetime.strptime(today_string, "%d/%m/%Y")

#dt into string:
dt_object1.strftime("%m/%d/%Y %H:%M:%S")
