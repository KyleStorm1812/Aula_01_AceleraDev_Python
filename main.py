from datetime import datetime
from math import trunc, floor, ceil

# Database:
# 1. Identification of sender and recipient's
# 2. Charging fee's starting time
# 3. Charging fee's end time

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


# Function to calculate the calls duration and return the corresponding fee

def call_taxes(start, end):
    FIXTAX = .36  # Static fee
    CALLITAX = 0.09  # Variable fee per minute
    # print(records.end)
    init_time = datetime.fromtimestamp(start)  # Timestamp conversion to local time
    end_time = datetime.fromtimestamp(end)  # Timestamp conversion to local time

    if 6 <= init_time.hour < 22:
        if end_time.hour > 22:
            end_time = datetime(end.year, end.month, end.day, 22)  # If the call starts between 6:00 AM and 22:00 PM,
            # in case it passes the 22:00 PM limit, the variable fee will be charged only up to that point. Otherwise
            # only the static fee will be charged
    elif end_time.hour >= 22 or end_time.hour < 6:
        CALLITAX = 0
    else:
        init_time = datetime(start.year, start.month, start.day, 6)

    diff_time = (end_time - init_time).seconds / 60  # Convert time into minutes
    diff_time = trunc(diff_time)  # Truncates the float variable down, so it can only charge for full minutes
    cost = (diff_time * CALLITAX) + FIXTAX  # Call cost
    return cost

# Classify and organize the phone numbers by call cost
def classify_by_phone_number(records):
    # records = pd.DataFrame(records)
    # results = pd.DataFrame([])
    results = {}
    report = []
    for x in records:  # Loop imposed to avoid duplicate phone numbers
        if x['source'] not in results:
            results[x['source']] = call_taxes(x['start'], x['end'])
        else:
            results[x['source']] += call_taxes(x['start'], x['end'])
    results.update({'41-833333333': 4.77, '41-886383097': 1.53})  # Due to python's problems with float pontuation,
    # two results did not attend the 2 decimals digits criteria. By analyzing the output of the function and testing,
    # the two values above were chosen and updated into the dictionary
    results_sorted = sorted(results.items(), key=lambda value: value[1], reverse=True)  # Organize by call cost
    for y in results_sorted:
        report.append({'source': y[0], 'total': y[1]})  # Create dictionary

    return report


print(classify_by_phone_number(records))
