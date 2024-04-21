with open("quiz-data.txt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.split("\n")
content = [line for line in content if "," in line]

OPTION_LETTERS = ["a", "b", "c", "d"]

score = 0
for i in content[1:]:
    question, *options, answer = i.split(",")
    print(question)
    print("\n".join([f"\t{OPTION_LETTERS[l]}) {x}" for l, x in enumerate(options)]))
    while True:
        inp = input(">>> ")
        if inp.lower() in OPTION_LETTERS:
            break
        print(f"Nhập {", ".join(OPTION_LETTERS[:-1])} hoặc {OPTION_LETTERS[-1]}")
    if inp == answer:
        score += 1

print(f"\nĐiểm: {score}/{len(content[1:])}\n")