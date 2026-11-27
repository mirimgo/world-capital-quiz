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
    while True:
        show_menu()
        choice = read_number("\n메뉴를 선택하세요: ", 1, 5)

        if choice == 1:
            print("\n[퀴즈 풀기] 준비 중입니다.")
        elif choice == 2:
            print("\n[퀴즈 추가하기] 준비 중입니다.")
        elif choice == 3:
            print("\n[퀴즈 목록] 준비 중입니다.")
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