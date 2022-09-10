import time, json, os # type: ignore
#import ntptime
from main import blinker

LASTSYNC = 0
class Datetime:
    def __init__(self):
        if self.date() == "2000-1-1":
            print("invalid time")
        print("\n")
        print(f"LOCAL TIME: {self.time()}")
        print(f"UTC TIME: {self.utcTime()}")
        print(f"DATE: {self.date()}")
        
        
        
    def localTime(self):
        UTC_OFFSET = +6 * 60 * 60
        actual_time = time.localtime(time.time() + UTC_OFFSET)
        return actual_time
    
    def time(self):
        local = self.localTime()
        results = f"{local[3]}:{local[4]}:{local[5]}"
        return results
    
    def utcTime(self):
        utc =  time.gmtime()
        results = f"{utc[3]}:{utc[4]}:{utc[5]}"
        return results
    
    def date(self):
        local = self.localTime()
        date = f"{local[0]}-{local[1]}-{local[2]}"
        return date
    
    def totalSeconds(self, time):
        hour, minute, sec = time.split(":")
        return (int(hour) *60 * 60) + (int(minute) *60) + (int(sec))
    

class Data:
    def __init__(self):
        self.startup()
        self.integrity("temp.json")
        
    def jsonRead(self, file):
        with open(file, "r") as f:
            preData =  json.load(f)
        return preData
        
    def save(self, file, data, preSave):
        "the actual time saver part of the code, this checks if a continue entry is present and replaces it"
        if file in os.listdir():
            preData = self.jsonRead(file)
            if preSave and len(preData) > 1:
                if preData[-1]["start"] == "continue":
                    preData.pop()
            preData.append(data)
                
            with open(file, "w") as f:
                json.dump(preData, f)
        else:
            with open(file, "w") as f:
                json.dump(data, f)
        
    def integrity(self, file):
        "responsible for checking if the file has data that could be caused by user error"
        dt = Datetime()
        if file in os.listdir():
            preData = preData = self.jsonRead(file)
            if len(preData) >= 1:
                for _ in range(len(preData)):
                    lastSaveDiff = dt.totalSeconds(dt.time()) - dt.totalSeconds(preData[-1]["time"])
                    date = True if dt.date() == preData[-1]["date"] else False
                    if lastSaveDiff < 150 and date == True:
                        preData.pop()
        with open(file, "w") as f:
            json.dump(preData, f)
            
    def startup(self):
        "creates the json file if it doesn't exist, without this running things can break"
        if "temp.json" not in os.listdir():
            data = []
            self.save("temp.json", data, False)
            print("new temp file created")
            blinker(2)
    
    
def timeSaver():
    db = Data()
    preData = db.jsonRead("temp.json")
    # value really doens't matter we're just trying to trigger it to continue
    preSave = "" if preData[-1]["start"] == "continue" else "1" 
    while True:
        datetime = Datetime()
        currentTime = str(datetime.time())
        if not preSave:
            data = {"start": "return", "time": str(currentTime), "date": str(datetime.date())}
            db.save("temp.json", data, False)
            print(f"data saved at {currentTime}")
        else:
            data = {"start": "continue", "time": str(currentTime), "date": str(datetime.date())}
            db.save("temp.json", data, True)
            print(f"data overwritten at {currentTime}")
        preSave = currentTime
        blinker(1)
        time.sleep(60)
        
