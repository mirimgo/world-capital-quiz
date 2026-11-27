import json
import random

# 숫자 입력 공통 처리 (공백 제거, 빈 입력, 숫자 아님, 범위 밖 처리)
def read_number(prompt, min_value, max_value):
    while True:
        text = input(prompt).strip()

        if not text:
            print("입력이 비어 있습니다. 숫자를 입력해주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("숫자만 입력해주세요.")
            continue

        if number < min_value or number > max_value:
            print(f"{min_value}부터 {max_value}까지의 번호를 입력해주세요.")
            continue

        return number

# 문자열 입력 공통 처리 (공백 제거, 빈 입력 불가)
def read_text(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("입력이 비어 있습니다. 다시 입력해주세요.")

# 퀴즈 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제
        self.choices = choices    # 선택지 4개 (리스트)
        self.answer = answer      # 정답 번호 (1~4)

    # 문제와 선택지 출력
    def show_question(self):
        print(f"\n{self.question}")

        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    # 정답 확인 (선택한 번호가 정답이면 True)
    def check_answer(self, choice_number):
        return choice_number == self.answer

    # 정답 선택지 글자 반환
    def get_answer_text(self):
        return self.choices[self.answer - 1]

# JSON 파일을 읽지 못할 때 사용하는 기본 퀴즈 (나라, 정답 수도, 오답 3개)
FALLBACK_DATA = [
    ("대한민국", "서울", ["부산", "인천", "대전"]),
    ("캐나다", "오타와", ["토론토", "밴쿠버", "몬트리올"]),
    ("도미니카 공화국", "산토도밍고", ["산티아고", "푸에르토플라타", "라로마나"]),
    ("아일랜드", "더블린", ["코크", "골웨이", "리머릭"]),
    ("적도 기니", "시우다드데라파스", ["바타", "에비나용", "몽고모"]),
]


# 나라 이름과 정답/오답으로 Quiz 객체 만들기 (선택지는 섞고, 정답은 번호로 저장)
def make_capital_quiz(country, answer, wrong_answers):
    if len(wrong_answers) != 3:
        raise ValueError("오답 선택지는 국가별로 3개여야 합니다.")

    choices = list(wrong_answers) + [answer]
    random.shuffle(choices)
    answer_number = choices.index(answer) + 1

    return Quiz(f"{country}의 수도는 어디일까요?", choices, answer_number)


# 기본 퀴즈 불러오기 (JSON 파일 -> 실패하면 FALLBACK_DATA)
def load_default_quizzes():
    try:
        with open("capitals.json", "r", encoding="utf-8") as file:
            capitals = json.load(file)

        with open("cities.json", "r", encoding="utf-8") as file:
            cities = json.load(file)

        quizzes = [
            make_capital_quiz(country, answer, cities[country])
            for country, answer in capitals.items()
        ]

        if quizzes:
            return quizzes

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("기본 퀴즈 파일을 읽지 못해 내장된 기본 퀴즈를 사용합니다.")

    return [
        make_capital_quiz(country, answer, wrong_answers)
        for country, answer, wrong_answers in FALLBACK_DATA
    ]

# 퀴즈 추가
def add_quiz(quizzes):
    print("\n[퀴즈 추가하기]")

    question = read_text("문제를 입력하세요: ")

    choices = []

    for i in range(4):
        while True:
            choice = read_text(f"{i + 1}번 선택지를 입력하세요: ")

            if choice in choices:
                print("이미 입력한 선택지입니다.")
            else:
                choices.append(choice)
                break

    answer_number = read_number("정답 번호를 입력하세요 (1~4): ", 1, 4)

    quizzes.append(Quiz(question, choices, answer_number))

    print("퀴즈가 성공적으로 추가되었습니다!")

# 퀴즈 풀기 (푼 점수를 반환)
def play_quiz(quizzes):
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return None

    score = 0
    total = len(quizzes)

    print("\n모를 '수도' 있지! 🌎 세계 수도 퀴즈!")
    print(f"총 {total}개의 문제가 준비되어 있습니다.")

    for quiz in quizzes:
        quiz.show_question()
        number = read_number("정답 번호를 입력하세요 (1~4): ", 1, 4)

        if quiz.check_answer(number):
            print("정답입니다! 🎉")
            score += 1
        else:
            print(f"아쉽네요! 정답은 {quiz.get_answer_text()}입니다.")

    accuracy = score / total * 100

    print("\n퀴즈가 종료되었습니다!")
    print(f"최종 점수: {score} / {total}")
    print(f"정답률: {accuracy:.1f}%")

    return score

# 퀴즈 목록 보기
def show_quizzes(quizzes):
    print("\n[등록된 퀴즈 목록]")

    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    for i, quiz in enumerate(quizzes, start=1):
        print(f"{i}. {quiz.question}")

# 메뉴 출력
def show_menu():
    print("\n================================")
    print("       모를 '수도' 있지! 🌎")
    print("================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가하기")
    print("3. 퀴즈 목록 보기")
    print("4. 점수 확인하기")
    print("5. 종료하기")


# 메인 루프
def main():
    quizzes = load_default_quizzes()

    while True:
        show_menu()
        choice = read_number("\n메뉴를 선택하세요: ", 1, 5)

        if choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            show_quizzes(quizzes)
        elif choice == 4:
            print("\n[점수 확인] 준비 중입니다.")
        elif choice == 5:
            print("\n프로그램을 종료합니다. 감사합니다!")
            break


# 프로그램 실행
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램이 중단되었습니다. 안전하게 종료합니다.")