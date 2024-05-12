import os, time, random, datetime

def clear():
    os.system("cls")

def cursor_up(n):
    return f'\033[{n}A'

cursor_end = '\033[K'

def throw(msg):
    print(f"[!] {msg}")

def format_money(value):
    return format(value, ",").replace(",", ".")

with open("quiz-data.txt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.split("\n")
content = [line for line in content if "," in line]

OPTION_SPACING = 4*" "
OPTION_LETTERS = ("a", "b", "c", "d")
help_options = ["50", "call", "vote"]

clear()
name = input("Tên của bạn: ")
clear()
print(f"Xin chào, {name}!")
time.sleep(1)
print("Chào mừng bạn với chương trình: ", end="")
time.sleep(1)
print("AI LÀ TRIỆU PHÚ")
time.sleep(1)

print("Chúng ta hãy bắt đầu nào", end="")
for _ in range(3):
    print(".", end="")
    time.sleep(1)

clear()
money = 100_000
for i in content[1:]:
    clear()

    print(f"Số tiền hiện tại: {format_money(money)}")

    # show helpers
    print(f"Các quyền trợ giúp: ", end="")
    for o in help_options:
        string = ""
        match o:
            case "50": string = "50/50 (nhập '50')"
            case "call": string = "Gọi người thân (nhập 'call')"
            case "vote": string = "Ý kiến khán giả (nhập 'vote')"
        print(string, end=", ")

    print("\n")
    
    # show question
    question, *options, answer = i.split(",")
    options_shown = OPTION_LETTERS
    while True:
        print(question)

        # show options
        for l, x in enumerate(options):
            letter = OPTION_LETTERS[l]
            if letter not in options_shown:
                continue
            print(f"{OPTION_SPACING}{letter}) {x}")

        # answering
        inp = input("Trả lời: ").lower()
        if inp in help_options:
            help_options.remove(inp)
            
            # help options
            match inp:
                case "50": # 50/50
                    clear()
                    options_shown = [answer, random.choice([x for x in OPTION_LETTERS if x != answer])]
                    throw("Đã bỏ đi 2 đáp án sai")
                case "call": # calling (likely to be correct)
                    choice = random.choice(OPTION_LETTERS + (answer,)*10)

                    # suspense
                    print("Đang gọi", end="")
                    for _ in range(10):
                        print(".", end="")
                        time.sleep(.5)
                    time.sleep(2)

                    clear()
                    throw(f'"Tôi nghĩ đáp án đúng là {choice.upper()}!"')
                case "vote": # voting (most reliable)
                    clear()
                    throw("Khán giả đang quyết định...")
                    votes = {l: 0 for l in OPTION_LETTERS}
                    
                    # printing votes and refreshing screen
                    for _ in range(100):
                        choice = random.choice(OPTION_LETTERS + (answer,))
                        votes[choice] += 1
                        for i in OPTION_LETTERS:
                            print(f"{OPTION_SPACING}{i}: {votes[i]*'|'}")
                        print(cursor_up(5))
                        time.sleep(.05)
                    
                    # final votes
                    most_voted, most_votes = "", 0
                    for i in OPTION_LETTERS:
                        if votes[i] > most_votes:
                            most_voted = i
                            most_votes = votes[i]
                        elif votes[i] == most_votes:
                            most_voted = f"{most_voted} hoặc {i}"
                    print("\n"*4)
                    throw(f"Ý kiến của khán giả cho ta thấy rằng đáp án đúng nhất là {most_voted.upper()}!")
            continue
        elif inp not in OPTION_LETTERS:
            clear()
            if len(help_options) > 0:
                throw(f"Nhập {", ".join(OPTION_LETTERS)} hoặc các quyền lựa chọn bạn hiện có ({", ".join(help_options)})")
            else:
                throw(f"Nhập {", ".join(OPTION_LETTERS[:-1])} hoặc {OPTION_LETTERS[-1]}")
            continue
        
        # confirming
        final = input("Bạn có chắc không? (Y/N): ").lower()
        if final in ("y", "yes"):
            break
        elif final in ("n", "no"):
            clear()
            throw("Mời bạn chọn lại đáp án")
        else:
            clear()
            throw("Hãy nhập Y hoặc N để xác nhận.")
    print()

    # suspense
    print("Câu trả lời của bạn", end="")
    for _ in range(3):
        print(".", end="")
        time.sleep(1)
    time.sleep(2)

    # right/wrong
    if inp == answer:
        print(" đúng! (+100.000)")
        money += 100_000
    else:
        print(" sai!")
        time.sleep(1)
        money = 0
        break
    
    # segue
    if i != content[-1]:
        print("Chuẩn bị qua câu kế tiếp", end="")
        for _ in range(3):
            print(".", end="")
            time.sleep(1)
        print()
        clear()

# final results
if money > 0:
    print(f"\nTiền thưởng: {format_money(money)}\n")
else:
    print(f"Rất tiếc, bạn đã mất hết tiền!")

input("\n(Nhấn ENTER để thoát khỏi chương trình)\n")
with open(f"save-{int(time.time())}.txt", "a", encoding="utf-8") as f:
    f.writelines((
        "AI LÀ TRIỆU PHÚ\n",
        f"\nNgày: {datetime.datetime.now()}\n"
        f"Tên: {name}\n",
        f"Tiền: {money}đ ({'thắng' if money > 0 else 'thua'})"
    ))
    f.close()