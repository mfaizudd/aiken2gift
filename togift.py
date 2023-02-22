import sys
import re
import codecs
from pathlib import Path

path = Path(__file__).parent / sys.argv[1]
if len(sys.argv) > 2:
    output_path = Path(__file__).parent / sys.argv[2]
    output_file = open(str(output_path), "a", encoding="utf-8")
    output_file.seek(0)
    output_file.truncate()

def write(s, end="\n", strip=True):
    if strip:
        s = s.strip()
    if len(sys.argv) > 2:
        output_file.write(s + end)
    else:
        print(s, end=end)
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
        elif mode == "question" and qno > 1:
            write("\\n")
        mode = "question"
        choices = {}

    if mode == "question":
        if qline == 0:
            write(f"::Q{qno}:: ", end="", strip=False)
            qno += 1
        write(f"{line}", end="")
        qline += 1
    elif mode == "choices":
        letter = line[0]
        choices[letter] = line[3:]
    elif mode == "answer":
        answer = line[7:].strip()
        write(" {", strip=False)
        for letter, choice in choices.items():
            if letter == answer:
                write(f"={choice}")
            else:
                write(f"~{choice}")
        write("}\n", strip=False)
    pass
for i in invalid:
    print(f"Invalid question: {i}")
