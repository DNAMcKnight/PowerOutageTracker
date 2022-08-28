try:
    import time, json, os # type: ignore
    import ntptime
    from main import blinker
except:
    import time, json, os # type: ignore
    from main import blinker
    print("failed to import some stuff")
    
    
class Datetime:
    def __init__(self):
        pass
        
    def localTime(self, ofset):
        """Creates the desired timezone for your local time"""
        UTC_OFFSET = int(ofset) * 60 * 60
        actual_time = time.localtime(time.time() + UTC_OFFSET)
        return actual_time
    
    def time(self,):
        "This converts the time to look similar to the datetime module in python"
        local = self.localTime(+6)
        results = f"{local[3]}:{local[4]}:{local[5]}"
        return results
    
    def utcTime(self):
        "Shows the UTCTime that looks similar to datetime module in Python"
        utc =  time.gmtime()
        results = f"{utc[3]}:{utc[4]}:{utc[5]}"
        return results
    
    def date(self):
        "Shows the local date similar to how datetime module does in python"
        local = self.localTime()
        date = f"{local[0]}-{local[1]}-{local[2]}"
        return date
    
    def totalSeconds(self, time):
        "takes in a time with hours:minutes:seconds and returns total seconds"
        if time:
            hour, minute, sec = time.split(":")
            return (int(hour) *60 * 60) + (int(minute) *60) + (int(sec))
        else:
            return False    

class Data:
    def __init__(self):
        self.startup()
        self.integrity("temp.json")
        
    def jsonRead(self, file):
        "Opens file for us with one line instead of 3"
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
        return
        
        
    def integrity(self, file):
        "responsible for checking if the file has data that could be caused by user error"
        dt = Datetime()
        if file in os.listdir():
            preData = self.jsonRead(file)
            if len(preData) >= 1:
                for _ in range(len(preData)):
                    lastSaveDiff = dt.totalSeconds(dt.time()) - dt.totalSeconds(preData[-1]["time"])
                    date = True if dt.date() == preData[-1]["date"] else False
                    if lastSaveDiff < 150 and date == True:
                        preData.pop()
        with open(file, "w") as f:
            json.dump(preData, f)
        return
    def startup(self):
        "creates the json file if it doesn't exist, without this running things can break"
        if "temp.json" not in os.listdir():
            data = []
            self.save("temp.json", data, False)
            print("new temp file created")
            blinker(2)
            return    
    
class Mountain:
    """We really didn't need another class however it would be best to 
    contain the data within a class than to introduce global variables
    and which don't seem to wrok properly.
    """
    def __init__(self):
        self.firstStartTime = None
        self.currentTime = None
    
    def timeSaver(self):
        """This function holds the logic to how it is set to log data."""
        db = Data()
        preData = db.jsonRead("temp.json")
        # value really doens't matter we're just trying to trigger it to continue
        preSave = ""
        if len(preData) > 1:
            preSave = "" if preData[-1]["start"] == "continue" else "1"
        elif len(preData) == 1:
            preSave = "" if preData[0]['start'] == "continue" else "1"          
        self.firstStartTime = str(Datetime().time())
        while True:
            self.timeSync()
            datetime = Datetime()
            self.currentTime = str(datetime.time())
            if not preSave:
                data = {"start": "return", "time": str(self.currentTime), "date": str(datetime.date())}
                db.save("temp.json", data, False)
                print(f"data saved at {self.currentTime}")
            else:
                data = {"start": "continue", "time": str(self.currentTime), "date": str(datetime.date())}
                db.save("temp.json", data, True)
                print(f"data overwritten at {self.currentTime}")
            preSave = self.currentTime
            blinker(1)
            time.sleep(60)
        
    
    def timeSync(self):
        """This function updates the time every hour after starting up"""
        if self.firstStartTime and self.firstStartTime != "1":
            dt = Datetime()
            preSec = dt.totalSeconds(str(self.firstStartTime))
            currentSec = dt.totalSeconds(self.currentTime)
            print(currentSec - preSec) if preSec else print("failed to convert again")
            timediff = currentSec - preSec
            if timediff >= 3600:
                ntptime.settime()
                dt = Datetime()
                if dt.date() == "2000-1-1":
                    print("invalid time")
                else:
                    self.firstStartTime = dt.time()
                    print(f"firstStartTime reset to {self.firstStartTime}")
                    print("\n")
                    print(f"LOCAL TIME: {dt.time()}")
                    print(f"UTC TIME: {dt.utcTime()}")
                    print(f"DATE: {dt.date()}")
            
            return
