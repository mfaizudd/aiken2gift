import sys
import re
import codecs
from pathlib import Path

path = Path(__file__).parent / sys.argv[1]
f = codecs.open(str(path), "r", "utf-8")
mode = "question"
qline = 0
qno = 1
choices = {}
invalid = []
for i, line in enumerate(f):
    if re.match(r"^[A-Z]+\. ", line):
        mode = "choices"
        qline = 0
    elif re.match(r"^ANSWER:", line):
        mode = "answer"
        qline = 0
    else:
        if (mode == "question" or mode == "choices") and qline == 0 and qno > 1:
            invalid.append(qno-1)
        mode = "question"
        choices = {}

    if mode == "question":
        if qline == 0:
            print(f"::Q{qno}\n:: ", end="")
            qno += 1
        print(f"{line.strip()} ")
        qline += 1
    elif mode == "choices":
        letter = line[0]
        choices[letter] = line[3:]
    elif mode == "answer":
        answer = line[7:].strip()
        print("{")
        for letter, choice in choices.items():
            if letter == answer:
                print(f"={choice}", end="")
            else:
                print(f"~{choice}", end="")
        print("}")
    pass
for i in invalid:
    print(f"Invalid question: {i}")
