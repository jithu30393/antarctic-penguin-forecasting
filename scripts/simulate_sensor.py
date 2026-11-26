import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json,time,random
for _ in range(5): print(json.dumps({'temperature':round(random.uniform(-15,2),2),'sea_ice':round(random.uniform(.1,.9),3),'ocean_condition':round(random.uniform(-1,1),3)})); time.sleep(.5)
