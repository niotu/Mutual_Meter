import json

default = {"highest_score": 0, "money": 0, "bought_cars": ["red_car"], "current_car_index": 0,
           "booster_levels": [1, 1, 1], "booster_stats": [1, 100, 1]}

with open('storage/scores.json', 'w') as file:
    json.dump(default, file)
