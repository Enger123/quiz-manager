import random
import os
import json
import time

class StatsManager:
    FILE = "stats.json"
    def __init__(self):
        self.data = self.load()

    def load(self):
        if os.path.isfile(self.FILE):
            try:
                with open("stats.json", "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, ValueError):
               return {'best score': 0, 'history': []}
        else:
            return {'best score': 0, 'history': []}

    def save(self):
        with open("stats.json", "w") as file:
            json.dump(self.data, file, indent=4)

    def update(self, score):
        best_score = self.data.get('best score', 0)
        if score > best_score:
            best_score = score
        self.data['best score'] = best_score
        if "history" not in self.data:
            self.data["history"] = []
        self.data["history"].append(score)
        self.save()

    def show(self):
        history = self.data.get("history", [])

        if not history:
            print("Статистика відсутня")
            return

        avg = sum(history) / len(history)
        print(f"Найкращий результат: {self.data['best score']}")
        print(f"Середній бал: {round(avg, 2)}")
        print(f"Кількість проходжень: {len(history)}")
        print(f"Останні 5: {history[-5:]}")

class QuestionManager:
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
        items = list(self.answers.items())
        random.shuffle(items)
        while True:
            mode = input("Виберіть режим питань (1) - 3 випадкових, (2) - 5 випадкових, (3) - усі питання: ")
            if mode not in ('1', '2', '3'):
                print("Помилка: Таке значення не допустиме.")
            elif mode == '1':
                count = 3
                break
            elif mode == '2':
                count = 5
                break
            elif mode == '3':
                count = len(items)
                break
        if count > len(items):
            print("Помилка: Недостатньо питань в базі")
            return
        sample_questions = random.sample(items, count)
        all_questions = count

        for question, correct_answers in sample_questions:
            print("У вас 10 секунд")
            start = time.time()
            user_ans = input(question).strip().lower()
            elapsed = time.time() - start
            if elapsed > 10:
                print(f"Ви не встигли відповісти по часу! Правильна відповідь: {', '.join(correct_answers).title()}")
                false_counter += 1
                continue
            if user_ans in correct_answers:
                true_counter += 1
            else:
                false_counter += 1
                print(f"Неправильно! Правильна відповідь: {', '.join(correct_answers).title()}")


        grade = true_counter * 100 / all_questions
        rounded_grade = round(grade)
        return rounded_grade



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
        except (IndexError, ValueError):
            print("Ви виходите за межі або ввели не число")

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
        except (IndexError, ValueError):
            print("Ви виходите за межі або ввели не число")

def main():
    question = QuestionManager()
    stats = StatsManager()
    print("Ви у менеджері питань")
    while True:
        button = input("Натисніть 1 - щоб пройти тестування, 2 - додати питання, 3 - видалити питання, 4 - редагувати питання, 5 - показати статистику, 0 - закрити: ")
        if button not in ('0', '1', '2', '3', '4', '5'):
            print("Помилка: Таке значення в програмі не доступне")
        elif button == '1':
            score = question.questions()
            if score is not None: #захист від недостатньої кількості питань після return повертає None
                stats.update(score)
        elif button == '2':
            question.add_questions()
            question.save()
        elif button == '3':
            question.del_question()
            question.save()
        elif button == '4':
            question.edit_question()
            question.save()
        elif button == '5':
            stats.show()
        else:
            break

if __name__ == '__main__':
    main()