
import sys
import os

symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    symbols["R" + str(i)] = i

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def clean_lines(filename):
    lines = []

    with open(filename, "r") as file:
        for line in file:
            line = line.split("//")[0].strip()

            if line:
                lines.append(line)

    return lines


def first_pass(lines):
    rom_address = 0
    labels = {}

    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if label in labels or label in symbols:
                print("Duplicate label:", label)
                continue

            labels[label] = rom_address
            symbols[label] = rom_address

        else:
            rom_address += 1

    return labels


def second_pass(lines):
    machine_code = []
    variables = {}
    next_address = 16

    for line in lines:

        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            value = line[1:]

            if value.isdigit():
                address = int(value)

            else:
                if value not in symbols:
                    symbols[value] = next_address
                    variables[value] = next_address
                    next_address += 1

                address = symbols[value]

            if address < 0 or address > 32767:
                raise ValueError("Invalid A-instruction: " + line)

            binary = format(address, "016b")
            machine_code.append(binary)

        else:
            if "=" in line:
                d, line = line.split("=")
            else:
                d = ""

            if ";" in line:
                c, j = line.split(";")
            else:
                c = line
                j = ""

            if c not in comp:
                raise ValueError("Invalid comp: " + c)

            if d not in dest:
                raise ValueError("Invalid dest: " + d)

            if j not in jump:
                raise ValueError("Invalid jump: " + j)

            binary = "111" + comp[c] + dest[d] + jump[j]
            machine_code.append(binary)

    return machine_code, variables


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py filename.asm")
        return

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("File not found:", input_file)
        return

    lines = clean_lines(input_file)

    first_pass(lines)

    machine_code, variables = second_pass(lines)

    output_file = os.path.splitext(input_file)[0] + ".hack"

    with open(output_file, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")

    with open("symbols.txt", "w") as file:
        for label, address in symbols.items():
            if label not in ["SP", "LCL", "ARG", "THIS", "THAT",
                             "SCREEN", "KBD"] and not (
                label.startswith("R") and label[1:].isdigit()
                and 0 <= int(label[1:]) <= 15
            ):
                file.write(label + " " + str(address) + "\n")

    print("Assembly completed successfully!")
    print("Output file:", output_file)
    print("Symbols saved in symbols.txt")


if __name__ == "__main__":
    main()
