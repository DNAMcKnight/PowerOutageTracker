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
    

class Data:
    def __init__(self):
        self.startup()
        
    def save(self, file, data, preSave):
        if file in os.listdir():
            with open(file, "r") as f:
                preData = json.load(f)
                if preSave and len(preData) > 1:
                    if preData[-1]["start"] == "continue":
                        preData.pop()
                preData.append(data)
                
            with open(file, "w") as f:
                json.dump(preData, f)
        else:
            with open(file, "w") as f:
                json.dump(data, f)
                
            
    def startup(self):
        if "temp.json" not in os.listdir():
            data = []
            self.save("temp.json", data, False)
            print("new temp file created")
            blinker(2)
            
            
def timeSaver():
    database = Data()
    preSave = ""
    while True:
        datetime = Datetime()
        currentTime = str(datetime.time())
        if not preSave:
            data = {"start": "return", "time": str(currentTime), "date": str(datetime.date())}
            database.save("temp.json", data, False)
            print(f"data saved at {currentTime}")
        else:
            data = {"start": "continue", "time": str(currentTime), "date": str(datetime.date())}
            database.save("temp.json", data, True)
            print(f"data overwritten at {currentTime}")
        preSave = currentTime
        blinker(1)
        time.sleep(60)
        