import os, time, random

def clear():
    os.system("cls")

def cursor_up(n):
    return f'\033[{n}A'

cursor_end = '\033[K'

def throw(msg):
    print(f"[!] {msg}")

with open("quiz-data.txt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.split("\n")
content = [line for line in content if "," in line]

OPTION_SPACING = 4*" "
OPTION_LETTERS = ("a", "b", "c", "d")
help_options = ["50", "call", "vote"]

clear()
money = 100_000
for i in content[1:]:
    print(f"Số tiền hiện tại: {format(money, ",").replace(",", ".")}")
    print(f"Các quyền trợ giúp: 50/50 (nhập '50'), Gọi người thân (nhập 'call'), Ý kiến khán giả (nhập 'vote')", end="\n\n")
    
    question, *options, answer = i.split(",")
    options_shown = OPTION_LETTERS
    while True:
        print(question)
        for l, x in enumerate(options):
            letter = OPTION_LETTERS[l]
            if letter not in options_shown:
                continue
            print(f"{OPTION_SPACING}{letter}) {x}")

        inp = input("Trả lời: ").lower()
        if inp in help_options:
            help_options.remove(inp)
            match inp:
                case "50":
                    clear()
                    options_shown = [answer, random.choice([x for x in OPTION_LETTERS if x != answer])]
                    throw("Đã bỏ đi 2 đáp án sai")
                case "call":
                    pass
                case "vote":
                    clear()
                    throw("Khán giả đang quyết định...")
                    votes = {l: 0 for l in OPTION_LETTERS}
                    for _ in range(100):
                        choice = random.choice(OPTION_LETTERS + (answer,))
                        votes[choice] += 1
                        for i in OPTION_LETTERS:
                            print(f"{OPTION_SPACING}{i}: {votes[i]*'|'}")
                        print(cursor_up(5))
                        time.sleep(.05)
                    
                    most_voted, most_votes = "", 0
                    for i in OPTION_LETTERS:
                        if votes[i] > most_votes:
                            most_voted = i
                            most_votes = votes[i]
                        elif votes[i] == most_votes:
                            most_voted = f"{most_voted} hoặc {i}"
                    print("\n"*4)
                    throw(f"Ý kiến của khán giả cho ta thấy rằng đáp án đúng nhất là {most_voted}!")
                    # input("Nhấn ENTER để quay lại ")
            continue
        elif inp not in OPTION_LETTERS:
            clear()
            if len(help_options) > 0:
                throw(f"Nhập {", ".join(OPTION_LETTERS)} hoặc các quyền lựa chọn bạn hiện có ({", ".join(help_options)})")
            else:
                throw(f"Nhập {", ".join(OPTION_LETTERS[:-1])} hoặc {OPTION_LETTERS[-1]}")
            continue
        
        final = input("Bạn có chắc không (Y/N): ").lower()
        if final not in ("ko", "no", "n"):
            break
        else:
            clear()
            throw("Mời bạn chọn lại đáp án")
            continue
    print("\n")
    if inp == answer:
        print("Đúng! (+100.000)")
        money += 100_000
    else:
        print("Sai!")
        money = 0
    
    print("Chuẩn bị qua câu kế tiếp", end="")
    for _ in range(3):
        print(".", end="")
        time.sleep(1)

    print()
    clear()

print(f"\nTiền thưởng: {money}\n")