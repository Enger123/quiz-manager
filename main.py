import random
import os
import json
from json import JSONDecodeError


class Answers:
    def __init__(self):
        self.answers = self.load_file()

    FILE = "questions.json"

    def load_file(self):
        if os.path.isfile(self.FILE):
            try:
                with open(self.FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, ValueError):
                return self.default_data()
        else:
            return self.default_data()

    def default_data(self):
        return {
            "Яка столиця України? ": ["київ"],
            "Хто написав Заповіт? ": ["тарас шевченко", "шевченко", "тарас григорович шевченко"],
            "Хто президент України? ": ["володимир зеленський", "зеленський"]
        }

    def save(self):
        with open(self.FILE, "w", encoding='utf-8') as file:
            json.dump(self.answers, file, indent=4, ensure_ascii=False)

    def questions(self):
        true_counter = 0
        false_counter = 0
        all_questions = len(self.answers)
        items = list(self.answers.items())
        random.shuffle(items)
        for question, correct_answers in items:
            if input(question).strip().lower() in correct_answers:
                true_counter += 1
            else:
                false_counter += 1
                print(f"Неправильно! Правильна відповідь: {', '.join(correct_answers).title()}")
        self.results(true_counter, false_counter, all_questions)

    def results(self, t, f, all):
        grade = t * 100 / all
        rounded_grade = round(grade)
        if os.path.isfile("stats.json"):
            try:
                with open("stats.json", "r") as file:
                    data = json.load(file)
            except (json.JSONDecodeError, ValueError):
               data = {}
        else:
            data = {}

        best_score = data.get("best score", 0)
        if rounded_grade > best_score:
            best_score = rounded_grade
        data["best score"] = best_score
        if "history" not in data:
            data["history"] = []
        data["history"].append(rounded_grade)
        with open("stats.json", "w") as file:
            json.dump(data, file, indent=4)


        print(f"Ваш результат: {rounded_grade}.")

    def add_questions(self):
        try:
            num = int(input("Скільки питань додати? (максимум 3): "))
            if 0 < num < 4:
                for i in range(1, num + 1):
                    question = input(f"Питання №{i}: ").strip()
                    correct_answer = input(f"Відповідь до питання через кому №{i}: ").lower().split(", ")
                    self.answers[question] = [ans.strip() for ans in correct_answer]
                    print("Питання додано")
            else:
                print("Недоступно ввести")
        except ValueError:
            print("Кількість питань повинна бути числом")

    def del_question(self):
        try:
            for i, question in enumerate(self.answers.keys(), start=1):
                print(f"{i}. {question}")
            n = int(input(f"Введіть номер питання для видалення: "))
            key_to_remove = list(self.answers.keys())[n - 1]
            del self.answers[key_to_remove]
            print("Питання видалено")
        except IndexError:
            print("Ви виходите за межі")

    def edit_question(self):
        try:
            for i, question in enumerate(self.answers.keys(), start=1):
                print(f"{i}. {question}")
            n = int(input(f"Введіть номер питання для редагування: "))
            key_to_remove = list(self.answers.keys())[n - 1]
            new_question = input(f"Введіть нове питання {n}: ")
            new_answer = input(f"Введіть відповідь до цього питання(через кому \", \"): ").lower().split(", ")
            self.answers[new_question] = [ans.strip() for ans in new_answer]
            del self.answers[key_to_remove]
            print("Питання відреаговано")
        except IndexError:
            print("Ви виходите за межі")

def main():
    manager = Answers()
    print("Ви у менеджері питань")
    while True:
        button = input("Натисніть 1 - щоб пройти тестування, 2 - додати питання, 3 - видалити питання, 4 - редагувати питання, 0 - закрити: ")
        if button not in ('0', '1', '2', '3', '4'):
            print("Помилка: Таке значення в програмі не доступне")
        elif button == '1':
            manager.questions()
        elif button == '2':
            manager.add_questions()
            manager.save()
        elif button == '3':
            manager.del_question()
            manager.save()
        elif button == '4':
            manager.edit_question()
            manager.save()
        else:
            break


if __name__ == '__main__':
    main()