from colorama import Fore, init

init()  # colorama 초기화

class InputHandler:
    def display_text(self, text):
        print(Fore.WHITE + text + Fore.RESET)

    def display_choices(self, choices):
        for i, choice in enumerate(choices, 1):
            print(Fore.CYAN + f"{i}. {choice['text']}" + Fore.RESET)

    def get_choice(self, choices):
        while True:
            try:
                choice = int(input(Fore.YELLOW + "선택하세요 (번호 입력): " + Fore.RESET))
                if 1 <= choice <= len(choices):
                    return choice - 1
                print("잘못된 입력입니다!")
            except ValueError:
                print("숫자를 입력하세요!")