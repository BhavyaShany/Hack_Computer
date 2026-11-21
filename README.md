# Hack Computer (Nand2Tetris)

A Hack computer project: assembly programs, an assembler written in Python, and the HDL chips for the computer that runs them.

## Project structure

```
.
├── README.md
├── assembler.py        # Hack assembler (.asm -> .hack)
├── symbols.txt         # Symbol table from the last assembler run
│
├── Box.asm / Box.hack      # Keyboard-controlled box on screen (K = 24)
├── rect.asm / Rect.hack    # Draws a column of R0 rows
├── max.asm / Max.hack      # R2 = max(R0, R1)
├── add.asm / Add.hack      # R0 = 2 + 3
├── sum.asm                 # Array sum snippet
├── pong.asm / Pong.hack    # Full Pong game
│
├── CPU.hdl             # Processor
├── Memory.hdl          # RAM + Screen + Keyboard address map
└── Computer.hdl        # Top-level chip: ROM + CPU + Memory
```

## Value of K

This project uses **K = 24**. In `Box.asm`, K is the screen row where the box starts.

Screen address of a row = `16384 + K * 32`

| K  | Start address |
|----|---------------|
| 24 | 17152         |

With K = 24 the box covers rows 24 to 43 (20 rows tall, 48 pixels wide).

## Using the assembler

Requires Python 3.

```
python3 assembler.py Box.asm
```

This produces:
- `Box.hack`: the 16-bit binary machine code, one instruction per line
- `symbols.txt`: labels and variables with their addresses (overwritten on every run)

If you change K, update the `@17152` lines in `Box.asm` (two places: the FILL and CLEAR sections) and reassemble.

## Programs

| Program | What it does |
|---------|--------------|
| `Box.asm` | While a key is pressed, fills a box starting at row K. When no key is pressed, clears it. |
| `rect.asm` | Reads R0 and draws that many filled 16-pixel-wide rows from the top-left of the screen. Does nothing if R0 <= 0. |
| `max.asm` | Stores the larger of R0 and R1 in R2. |
| `add.asm` | Computes 2 + 3 and stores the result in R0. |
| `sum.asm` | Adds `arr[j]` into `sum` and increments `arr[j]`. A practice fragment with no `.hack` file. |
| `pong.asm` | The Pong game from the Nand2Tetris course, compiled from Jack to VM code to assembly. |

## Running the programs

1. Open the CPU Emulator from the Nand2Tetris software suite.
2. Load a `.hack` file (for example `Box.hack`).
3. Set animation to "No animation" for speed, and enable the screen and keyboard.
4. Run. For `Box.hack`, press any key to draw the box and release it to clear.

For `rect` and `max`, set the input values in RAM (R0, R1) before running.

## Hardware

| Chip | Description |
|------|-------------|
| `CPU.hdl` | Decodes A and C instructions. Contains the A and D registers, the ALU and the program counter. Jumps are decided from the ALU's zero and negative flags. |
| `Memory.hdl` | Address map: 0-16383 RAM, 16384-24575 Screen, 24576 Keyboard. |
| `Computer.hdl` | Connects ROM32K, the CPU and Memory. The only input is `reset`. |

To test the chips, load them in the Hardware Simulator from the Nand2Tetris software suite.
