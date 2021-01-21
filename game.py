import random
import msvcrt
import time


class Screen(object):       #This program doesn't use curses, it just prints into the console
    def __init__(self, y = 10, x = 10, chars = ''):
        self.clear()
        self.y, self.x = y, x
        self.chars = chars if chars else [[' ' for i in range(x)] for i in range(y)] #chars stores what's printed
        self.vals = [[0 for i in range(x)] for i in range(y)]       #vals stores the state of each cell
        self.selected = (0, 0)

    def select(self, x, y): #validate that this cell can be selected
        if x >= 0 and y >= 0 and x < self.x and y < self.y:
            self.selected = (y, x)
        
    def clear(self):
        print('\n' * 50)

    def __str__(self):      #print function
        #FIRST LINE
        ret = chr(218) + 3*chr(196) + (chr(194) + 3*chr(196)) * (self.x-1) + chr(191) + '\n'
        #ALL OTHER LINES
        for i in range(self.y):
            line = chr(179)
            for j in range(self.x):
                #HIGHLIGHT SELECTED CELL
                if self.selected == (i, j):
                    line += chr(177) + self.chars[i][j] + chr(177) + chr(179)
                elif self.chars[i][j] == str(self.vals[i][j]) or self.chars[i][j] == chr(178):
                    line += chr(178) + self.chars[i][j] + chr(178) + chr(179)
                else:
                    line += '|' + self.chars[i][j] + '|' + chr(179)
            line = line[:-1] + chr(179)
            ret += line + '\n'
            if i != self.y - 1:
                ret += chr(195) + 3*chr(196) + (chr(197) + 3*chr(196)) * (self.x-1) + chr(180) + '\n'
        return ret + chr(192) + 3*chr(196) + (chr(193) + 3*chr(196)) * (self.x-1) + chr(217) + '\n'

    def getch(self):
        return msvcrt.getch()

    def update(self):
        self.clear()
        print(self)

    def flag(self):
        if self.chars[self.selected[0]][self.selected[1]] != 'P':
            self.chars[self.selected[0]][self.selected[1]] = 'P'
        else:
            self.chars[self.selected[0]][self.selected[1]] = ' '

    def reveal(self):
        y, x = self.selected
        
        if not(self.revealcoord(x, y)): 
            return False    #returns will be used to break the loop
        if self.won():
            print("You Have Won!")
            return False
        return True
    
    def revealcoord(self, x, y):    #recursive function that clears all empty cells
        if self.vals[y][x] == self.chars[y][x]:
            return True
        elif self.chars[y][x] == chr(178):
            return True
        elif self.vals[y][x] == 0:
            self.chars[y][x] = chr(178)
            for coord in self.adjacent_coords(x, y):
                self.revealcoord(*coord)
        else:
            self.chars[y][x] = str(self.vals[y][x])
        if self.vals[y][x] == 'X':
            self.game_over()
            return False
        return True
    
    def game_over(self):
        for i, line in enumerate(self.vals):
            for j, val in enumerate(line):
                if val == 'X':
                    self.chars[i][j] = 'X'
        self.update()
        print("Game Over!")
        
    def adjacent_coords(self, x, y):    #returns a list of coords adjacent to x, y
        ret = []
        if x > 0 and y >0:
            ret.append((x-1, y-1))
        if x > 0 and y < self.y -1:
            ret.append((x-1, y+1))
        if x < self.x -1 and y > 0:
            ret.append((x+1, y-1))
        if x < self.x -1 and y < self.x -1:
            ret.append((x+1, y+1))
        if x > 0:
            ret.append((x-1, y))
        if y > 0:
            ret.append((x, y-1))
        if x < self.x -1:
            ret.append((x+1, y))
        if y < self.y -1:
            ret.append((x, y+1))
        
        return ret

    def won(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.vals[y][x] == 'X':
                    continue
                elif str(self.vals[y][x]) == self.chars[y][x]:
                    pass
                elif self.chars[y][x] == chr(178):
                    pass
                else:
                    return False
        return True

class Game(object): #game logic
    arrows = {75: 0, 72: 1, 80: 2, 77: 3}
    
    def __init__(self):
        while True:
            try:
                x, y = input("How big would you like your grid?(x,y): ")
                break
            except NameError, ValueError:
                continue
                
        while True:
            try:
                self.mines = int(raw_input("How many mines would you like?: "))
                break
            except ValueError:
                continue
        
        print """\
        Controls:
        To select Box   <-, ^, v, ->
        To flag         p
        To select       SPACE
        To exit         ESC
"""
        raw_input('')
        self.screen = Screen(y, x)
        for i in range(self.mines):
            coord = self.rand_coord()
            if self.screen.vals[coord[1]][coord[0]] == 'X':
                continue
            else:
                self.screen.vals[coord[1]][coord[0]] = 'X'
                for coord in self.screen.adjacent_coords(*coord):
                    self.increment_coord(*coord)
                
        self.screen.update()
        

    def update(self):
        self.screen.update()
        char = self.screen.getch()
        if char == '\xe0':
            code = self.arrows[ord(self.screen.getch())]
            self.screen.select(self.screen.selected[1] + (-1 if code == 0 else (1 if code == 3 else 0)),
                               self.screen.selected[0] + (-1 if code == 1 else (1 if code == 2 else 0)))
        elif char == '\x1b':
            sys.exit()
        elif char.lower() == 'p':
            self.screen.flag()
        elif char == ' ':
            return self.screen.reveal()
        return True

    def rand_coord(self):
        return (random.randint(0, self.screen.x - 1), random.randint(0, self.screen.y - 1))

    
    def increment_coord(self, x, y):
        self.screen.vals[y][x] += 1 if self.screen.vals[y][x] != 'X' else ''
        

while True:
    try:
        while raw_input("Would you like to play?: ")[0].lower() == 'y':
            game = Game()
            while game.update():
                pass
        break
    except IndexError:
        pass
    



