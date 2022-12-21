import json


class Storage:
    def __init__(self):
        self.storage = None
        self.highest_score = None
        self.bought_cars = None
        self.current_car_index = None
        self.money = None
        self.storage, self.highest_score, self.money = self.load_data()

    def load_data(self):
        with open('storage/scores.json', 'r', encoding='utf-8') as scores:
            storage = json.load(scores)
        highest_score = storage.get('highest_score')
        money = storage.get('money')
        bought_cars = storage.get('bought_cars')
        return storage, highest_score, money

    def get_storage(self):
        return self.storage

    def load_storage(self):
        self.storage['highest_score'] = self.highest_score
        self.storage['money'] = self.money
        self.storage['bought_cars'] = self.bought_cars

    def set_highest(self, score):
        self.highest_score = score

    def set_score(self, score):
        self.score = score

    def set_money(self, money):
        self.money = money

    def set_bought_cars(self, bought_cars):
        self.bought_cars = bought_cars

    def save_data(self, highest_score, money, bought_cars):
        self.storage['highest_score'] = highest_score
        self.storage['money'] = money
        self.storage['bought_cars'] = bought_cars

        with open('storage/scores.json', 'w', encoding='utf-8') as scores:
            json.dump(self.storage, scores)
