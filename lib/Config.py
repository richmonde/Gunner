import json

def loadConfig():
    with open('config.json','r') as f:
        wjson = json.loads(f.read())
    return wjson

def setConfig(key,value):
    with open('config.json','w') as f:
        wjson = json.loads(f.read())
        wjson[key] = value
        f.write(wjson)
