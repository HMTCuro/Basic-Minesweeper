# minesweeper game
import numpy as np
import random

class Minesweeper:
    def __init__(self) -> None:
        # default values
        self.board = None
        self.status = None
        self.solved = False
        self.dead = False

    def create_board(self, rows: int, cols: int, mines: int) -> None:
        # reset values
        self.solved = False
        self.dead = False
        # create board
        self.board = np.zeros((rows, cols), dtype=int)
        self.status = np.zeros((rows, cols), dtype=int)
        # place mines
        while mines > 0:
            row = random.randint(0, rows-1)
            col = random.randint(0, cols-1)
            if self.board[row][col] == -1:
                continue
            self.board[row][col] = -1
            mines -= 1
        
        # calculate numbers
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == -1:
                    continue
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if row+i < 0 or row+i >= rows or col+j < 0 or col+j >= cols:
                            continue
                        if self.board[row+i][col+j] == -1:
                            self.board[row][col] += 1
        
        # cover all cells
        self.status = np.zeros((rows, cols), dtype=int)

        # reveal a cell
        while True:
            row = random.randint(0, rows-1)
            col = random.randint(0, cols-1)
            if self.board[row][col] == 0:
                self.reveal(row, col)
                break

    def reveal(self, row: int, col: int) -> None:
        if self.dead or self.solved:
            return
        if self.board[row][col] == -1:
            self.dead = True
            self.status[row][col] = 1
            return
        if self.board[row][col] > 0:
            self.status[row][col] = 1
            return
        rows, cols = self.board.shape
        self.status[row][col] = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if row+i < 0 or row+i >= rows or col+j < 0 or col+j >= cols:
                    continue
                if self.status[row+i][col+j] == 1:
                    continue
                self.reveal(row+i, col+j)

    def flag(self, row: int, col: int) -> None:
        if self.dead or self.solved:
            return
        # wrongly flagging is not allowed
        if self.status[row][col] == 1:
            return
        # flagging a correct mine
        if self.board[row][col] == -1:
            self.status[row][col] = 2
            return
        # flagging a correct non-mine will terminate the game
        self.dead = True
        self.status[row][col] = 1
        
    def check(self) -> None:
        if self.dead:
            return
        self.solved = (np.min(self.status + self.board)!=-1)

    def print_board(self) -> None:
        rows, cols = self.board.shape
        # print column numbers
        print(" ", end=" ")
        for col in range(cols):
            print(col, end=" ")
        print()

        for row in range(rows):
            # print row number
            print(row, end=" ")
            for col in range(cols):
                if self.status[row][col] == 0:
                    print("X", end=" ")
                elif self.status[row][col] == 1:
                    if self.board[row][col] == -1:
                        print("*", end=" ")
                    else:
                        print(self.board[row][col], end=" ")
                else:
                    print("F", end=" ")
            print()

    def print_solution(self) -> None:
        rows, cols = self.board.shape
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == -1:
                    print("*", end=" ")
                else:
                    print(self.board[row][col], end=" ")
            print()

def command_line(game: Minesweeper) -> None:
    while not game.dead and not game.solved:
        game.print_board()
        print("Enter command (R/F row col):")
        command = input()
        command = command.split()
        if len(command) != 3:
            print("Invalid command!")
            continue
        if command[0] == "R":
            game.reveal(int(command[1]), int(command[2]))
        elif command[0] == "F":
            game.flag(int(command[1]), int(command[2]))
        else:
            print("Invalid command!")
        game.check()
    game.print_solution()
    if game.dead:
        print("You lost!")
    else:
        print("You won!")

if __name__ == "__main__":
    game = Minesweeper()
    game.create_board(10, 10, 10)
    command_line(game)

