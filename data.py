import requests
from random import choice
# from testing import QuizInterface

trivia_categories = [
            {"id": 9, "name": "General Knowledge"},
            {"id": 11, "name": "Entertainment: Film"},
            {"id": 12, "name": "Entertainment: Music"},
            {"id": 14, "name": "Entertainment: Television"},
            {"id": 15, "name": "Entertainment: Video Games"},
            {"id": 17, "name": "Science & Nature"},
            {"id": 18, "name": "Science: Computers"},
            {"id": 19, "name": "Science: Mathematics"},
            {"id": 20, "name": "Mythology"},
            {"id": 21, "name": "Sports"},
            {"id": 22, "name": "Geography"},
            {"id": 23, "name": "History"},
            {"id": 24, "name": "Politics"},
            {"id": 27, "name": "Animals"},
            {"id": 28, "name": "Vehicles"},
]

category_nums = [9, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, ]

# category_choice = choice(category_nums)
#
# parameters = {
#     "amount": 2,
#     "category": category_choice,
#     "type": "boolean",
# }
#
# response = requests.get("https://opentdb.com/api.php?", params=parameters)
# response.raise_for_status()
# data = response.json()
#
# question_data = data['results']


class TriviaData:

    def __init__(self, possible_category):
        self.data_amount = 10
        if possible_category != None:
            category_choice = possible_category
        elif possible_category == None:
            category_choice = choice(category_nums)
        self.parameters = {"amount": self.data_amount, "category": category_choice, "type": "boolean", }

        self.response = requests.get("https://opentdb.com/api.php?", params=self.parameters)
        self.response.raise_for_status()
        self.question_data = self.response.json()['results']

    def get_question_data(self):
        return self.question_data

    # def get_question_number(self):
    #     return self.data_amount
