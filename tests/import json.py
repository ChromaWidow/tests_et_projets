import json
import numpy
with open(r"C:\Users\Elèves\Documents\Info\meteo.json",encoding="utf-8",mode='r') as f:
    data=json.load(f)
#print(data["stations"][2]["mesures"]["t"])

for st in data ["stations"]:
    print(st["id"])
    som=0
    for temp in st["mesures"]["t"]:
        som=som+temp
    print(som/3)
