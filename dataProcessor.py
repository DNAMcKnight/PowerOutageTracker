import json, traceback

    
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
        
parser("temp 2022-8-23.json", "tempOldP.json")

