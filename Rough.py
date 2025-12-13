# type_of_trip = "Round_trip"

# string_one = "//li[@data-cy='oneWayTrip']"

# if type_of_trip == "Round_trip":
#     string_one.replace('oneWayTrip', 'Round_trip')

# print(string_one)    

# from datetime import datetime

# date = "15 Dec 2025"

# def convert_to_aria_label(date_str):
#         date_obj = datetime.strptime(date_str, "%d %b %Y")
#         weekday = date_obj.strftime("%a")
#         return date_obj.strftime(f"{weekday} %b %d %Y")

# print(convert_to_aria_label(date))

data = [{"name":"Sorav", "age": 30},
        {"name":"Raj tilak", "age": 35}]

for item in data:
    print(item["name"])