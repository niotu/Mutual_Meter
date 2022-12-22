import json

default = {"highest_score": 0, "money": 0, "bought_cars": [], "current_car_index": 0}

with open('storage/scores.json', 'w') as file:
    json.dump(default, file)