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
    if re.match(r"^[A-Za-z]+\..*?", line):
        mode = "choices"
        qline = 0
    elif re.match(r"ANS.*?:", line):
        mode = "answer"
        qline = 0
    else:
        if mode == "choices":
            invalid.append(qno-1)
        elif mode == "question" and qline == 0 and line.strip() == "":
            continue
        elif mode == "question" and qline >= 1:
            write("\\n")
        mode = "question"
        choices = {}

    if mode == "question":
        text = line.strip()
        if qline == 0 and text == "":
            continue
        if qline == 0:
            number = str(qno).zfill(2)
            write(f"::Q{number}:: ", end="", strip=False)
            qno += 1
        match = re.search(r"^(\d+)\.(.*)", text)
        if match:
            text = match.group(2)
        elif qline == 0 and text != "":
            print(f"Possibly invalid question on line {i+1} question no {qno-1} (no numbering)")
        write(f"{text}", end="")
        qline += 1
    elif mode == "choices":
        letter = line[0]
        choices[letter] = line[3:]
    elif mode == "answer":
        match = re.search(r"\w+.*?:.*([A-Z]+)", line)
        answer = ""
        if match:
            answer = match.group(1)
        else:
            invalid.append(qno-1)
            print(f"Invalid answer on line {i+1}")
        write(" {", strip=False)
        for letter, choice in choices.items():
            if letter == answer:
                write(f"={choice}")
            else:
                write(f"~{choice}")
        write("}\n", strip=False)
        mode = "question"
        qline = 0
    pass
for i in invalid:
    print(f"Invalid question: {i}")
