import json, traceback, time
from tracemalloc import start
from typing import final

    
def parser(readData,outputData):
    """This function requires a file to be parsed and an output file to save it in"""
    try:
        #reaDing the data
        with open(readData, "r") as f:
            data = json.load(f)
            # we need to make pairs so if it's not a even number it fails
            if not len(data) % 2 == 0:
                print(f"ERROR: required equal pairs got {len(data)}")
                return False
            count = 2
            prev = 0
            parsedList = []
            # takes 2 messages and pairs them up and puts it all back in a list
            for x in range(0, round(len(data)/2)):
                messageList = [data[x] for x in range(prev, count)]
                prev = count
                count += 2
                parsedList.append(messageList)
        # now we save it  all to a file for now, in the futuer we could parse the whole thing and then save it.
        with open(outputData, "w") as f:
            json.dump(parsedList, f, indent=2)
        return True
    except Exception:
        print(traceback.format_exc())
        

def minuteConv(rawTime):
    hours, minutes, sec = rawTime.split(":")
    return (int(hours) * 60 + int(minutes)) * 60 + int(sec)

def dateConv(rawDate):
    year, month, days = rawDate.split("-")
    return (int(year) * 12 + int(month)) * 30 + int(days)

def timeDuration(data):
    for item in data:   
        if item['start'] == "continue":
            time = item['time']
            date = item['date']
            startTime = minuteConv(item['time'])
            startDate = dateConv(item['date'])
        elif item['start'] == "return":
            endTime = minuteConv(item['time'])
            endDate = dateConv(item['date'])
    if startDate == endDate:
        duration = int(endTime) - int(startTime)
    else:
        days = (int(endDate) - int(startDate)) * 24 * 60 * 60
        endTime = int(endTime) + days
        duration = int(endTime) - int(startTime)
    
    hours, rem = divmod(duration, 3600)
    minutes, seconds = divmod(rem, 60)
    # if hours:
    #     print(item)
    message = f"\t{hours if hours else 0} hours\t{minutes if minutes else 0} min\t{seconds if seconds else 0} sec\t Time: {time}\t Date: {date}"
    # print(message)
    return {"value": timeStringify(duration), "duration": duration, "time": time, "date":date}

def timeCalc(duration):
    hours, rem = divmod(duration, 3600)
    minutes, seconds = divmod(rem, 60)
    return hours, minutes, seconds

def timeStringify(duration):
    hours, rem = divmod(duration, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours if hours else 0}h {minutes if minutes else 0}m {seconds if seconds else 0}s"

def main():
    db = []
    finalDB = []
    lastDate = ""
    with open("parsedData.json", 'r') as f:
        data = json.load(f)
        for item in data:
            td = timeDuration(item)
            if lastDate == "" :
                db.append(td)
                lastDate = td["date"]
            elif td['date'] == lastDate:
                db.append(td)
            else:
                finalDB.append(db)
                db = []
                db.append(td)
                lastDate = td["date"]
                # print(finalDB)
                
    for day in finalDB:
        dailyDuration = 0
        highest = 0
        for items in day:
            dailyDuration += items['duration']
            highest = items['duration'] if items['duration'] > highest else highest
            print(items)
        print()
        print(f"Total Outages: {len(day)}\tlongest outage: {timeStringify(highest)}\tTotal Duration: {timeStringify(dailyDuration)}")
        print("------------------------------")
        print("\n")


main()
# parser("temp.json", "parsedData.json")