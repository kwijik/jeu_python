from random import *



class Position(object):

    def __init__(self, height, width, x_perso, y_perso):
        self.stones = []
        self.height = height  
        self.width = width
        self.empty_cells = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (self.is_exist((x,y))):
                    self.empty_cells.append((x,y))
        self.x_perso = x_perso
        self.y_perso = y_perso
        self.empty_cells.remove((self.x_perso,self.y_perso))

        self.last_move = False # need for debugging 

    def get_neibours(self, n):
        x = n[0]
        y = n[1]
        if y % 2 == 0:
            return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1)]
        else:
            return [(x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


    def border_cells(self):
        arr = []
        for i in range(0,self.width):
            arr.append((i,0))
            arr.append((i,self.height-1))
        for j in range(1, self.height-1):
            arr.append((0,j))
            arr.append((self.width-1-(j%2), j))
        return arr


    def weight(self):
        known_cells = []
        known_cells_weight = []
        for b in self.border_cells():
            if ( self.x_perso == b[0] and self.y_perso == b[1]):
                return -9999
            if(b not in self.stones):
                known_cells.append(b)
                known_cells_weight.append(0)
        current_cell = 0
        while current_cell < len(known_cells):
            nbs = self.get_neibours(known_cells[current_cell])
            for n in nbs:
                if n == (self.x_perso, self.y_perso): # if person is on this cell
                    return known_cells_weight[current_cell]
                if self.is_exist(n) and (n not in known_cells) and (n not in self.stones):
                    known_cells.append(n)
                    known_cells_weight.append(known_cells_weight[current_cell]+1)
            current_cell += 1

        return 9999 # means stones won


    def get_children(self, maximizingPlayer):
        possible_movement = []
        if (maximizingPlayer): # if stones 
            for n in self.empty_cells: 
                child = self.clone()
                child.add_stone(n)
                possible_movement.append(child) # possible_movement should be sorted to optimize minimax
        else:
            neibours = self.get_neibours((self.x_perso, self.y_perso))
            for n in neibours:
                if (self.is_exist(n) and n not in self.stones):
                    child = self.clone()
                    child.setPerson(n[0], n[1])
                    possible_movement.append(child)
        return possible_movement

    def is_exist(self,n):
        x = n[0]
        y = n[1]
        return x >= 0 and y >= 0 and y <= self.height-1 and x <= self.width - 1 - y % 2


    def add_stone(self,n):
        x = n[0]
        y = n[1]
        if self.is_exist(n) and (x != self.x_perso or y != self.y_perso) and (n not in self.stones):
            self.stones.append(n)
            self.last_move = n
            self.empty_cells.remove(n)
            return True # if it's possible to add stone
        return False


    def placeRandom (self,num) :
        if num > len(self.empty_cells):
            return  
        for i in range(0,num):
            while True:
                x = randrange(0, self.width)
                y = randrange(0, self.height)
                if self.add_stone((x,y)):
                    break

    def clone(self):
        c = Position(self.height, self.width, self.x_perso, self.y_perso)
        for s in self.stones:
            c.stones.append(s)
        c.empty_cells = []
        for e in self.empty_cells:
            c.empty_cells.append(e)
        return c

    def setPerson(self,x,y):
        self.empty_cells.append((self.x_perso,self.y_perso))
        self.x_perso = x
        self.y_perso = y
        self.empty_cells.remove((self.x_perso,self.y_perso))
      