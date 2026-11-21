
// Box program for K : 24
// Starting row : 24  (address = 16384 + 24*32 = 17152)
// Height : 20 rows
// Width : 48 pixels

(CHECK_KEY)
@KBD
D=M
@FILL
D;JGT
@CLEAR
0;JMP

(FILL)
@17152
D=A
@addr
M=D

@20
D=A
@rows
M=D

(FILL_ROW)
@3
D=A
@cols
M=D

(FILL_WORD)
@addr
A=M
M=-1

@addr
M=M+1

@cols
MD=M-1
@FILL_WORD
D;JGT

@29
D=A
@addr
M=D+M

@rows
MD=M-1
@FILL_ROW
D;JGT

@CHECK_KEY
0;JMP

(CLEAR)
@17152
D=A
@addr
M=D

@20
D=A
@rows
M=D

(CLEAR_ROW)
@3
D=A
@cols
M=D

(CLEAR_WORD)
@addr
A=M
M=0

@addr
M=M+1

@cols
MD=M-1
@CLEAR_WORD
D;JGT

@29
D=A
@addr
M=D+M

@rows
MD=M-1
@CLEAR_ROW
D;JGT

@CHECK_KEY
0;JMP

//Bhavya Shany

