(MAIN_LOOP)
    @KBD
    D=M

    @SET_WHITE
    D;JEQ

(SET_BLACK)
    @color
    M=-1
    @DRAW
    0;JMP

(SET_WHITE)
    @color
    M=0

(DRAW)
    @17760
    D=A
    @row_addr
    M=D

    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    @row_count
    D=M
    @MAIN_LOOP
    D;JEQ

    @row_addr
    D=M
    @col_addr
    M=D

    @4
    D=A
    @col_count
    M=D

(COL_LOOP)
    @col_count
    D=M
    @NEXT_ROW
    D;JEQ

    @color
    D=M
    @col_addr
    A=M
    M=D

    @col_addr
    M=M+1

    @col_count
    M=M-1

    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @row_addr
    M=D+M

    @row_count
    M=M-1

    @ROW_LOOP
    0;JMP
