import json


def load_current_car():
    with open('storage/scores.json', 'r') as scores:
        storage = json.load(scores)
    return storage['current_car_index']

def load_bought_cars():
    with open('storage/scores.json', 'r') as scores:
        storage = json.load(scores)
    return storage['bought_cars']


def load_data():
    with open('storage/scores.json', 'r', encoding='utf-8') as scores:
        storage = json.load(scores)
    highest_score = storage.get('highest_score')
    money = storage.get('money')
    return storage, highest_score, money


class Storage:
    def __init__(self):
        self.storage = None
        self.highest_score = None
        self.money = None
        self.bought_cars = load_bought_cars()
        self.current_car_tag = self.bought_cars[int(load_current_car())]
        self.storage, self.highest_score, self.money = load_data()

    def get_current_car_index(self):
        return int(load_current_car())

    def get_bought_cars(self):
        return self.bought_cars

    def get_upgrades_levels(self):
        return self.storage["booster_levels"]

    def get_upgrades_params(self):
        return self.storage["booster_stats"]

    def get_storage(self):
        return self.storage

    def load_storage(self):
        self.storage['highest_score'] = self.highest_score
        self.storage['money'] = self.money
        self.storage['bought_cars'] = self.bought_cars

    def set_highest(self, score):
        self.highest_score = score

    def set_money(self, money):
        self.money = money

    def set_bought_cars(self, bought_cars):
        self.bought_cars = bought_cars

    def save_data(self, highest_score, money, upgrades_levels, uprades_stats):
        self.storage['highest_score'] = highest_score
        self.storage['money'] = money
        self.storage["bought_cars"] = self.bought_cars
        self.storage["booster_levels"] = upgrades_levels
        self.storage["booster_stats"] = uprades_stats

        with open('storage/scores.json', 'w', encoding='utf-8') as scores:
            json.dump(self.storage, scores)
