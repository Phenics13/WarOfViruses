from tkinter import *
from tkinter import messagebox

class Player:
    def __init__(self, n):
        self.__n = n
    def Move(self, value):
        if value == 0: return self.__n
        return -self.__n;
    def GetVal(self):
        return self.__n;

class PaperTable:
    def __GetArr(self):
        arr = [[0 for x in range(self.__row)] for y in range(self.__col)]
        return arr
    
    def Add(self, i, j, n):
        self.__arr[i][j] = n

    def __init__(self, size, Xvalue, Ovalue, canvas, img_size, item_size): 
        if size == 0: exit("size of the self.__arr == 0")
        self.__row = self.__col = size
        self.__arr = self.__GetArr()

        self.Add(size - 1, 0, Xvalue)
        self.Add(size - 2, 0, Xvalue)
        self.Add(size - 1, 1, Xvalue)

        self.Add(0, size - 1, Ovalue)
        self.Add(0, size - 2, Ovalue)
        self.Add(1, size - 1, Ovalue)

        self.__canvas = canvas
        self.__img_size = img_size
        self.__item_size = item_size
    
    def GetVal(self, i, j):
        return self.__arr[i][j]

    def isMoveLegal(self, i, j, n):
        legal = False
        if self.__arr[i][j] == n or self.__arr[i][j] < 0: return legal

        i -= 1
        j -= 1
        for k in range(3):
            for g in range(3):
                if i + k < self.__row and j + g < self.__col and i + k > -1 and j + g > -1:
                    if self.__arr[i + k][j + g] == -n:
                        self.__arr[i + k][j + g] = 0
                        if not legal: legal = self.isMoveLegal(i + k, j + g, n)
                        self.__arr[i + k][j + g] = -n
                    if self.__arr[i + k][j + g] == n: legal = True
        
        return legal
    
    def isDefeated(self, enemvalue):
        for i in range(self.__row):
            for j in range(self.__col):
                if self.__arr[i][j] == enemvalue: return False
        return True

    def isFull(self):
        for i in range(self.__row):
            for j in range(self.__col):
                if self.__arr[i][j] == 0: return False
        return True

    def __X(self, j):
        return 5 + j * self.__img_size/10 + self.__item_size/2

    def __Y(self, i):
        return 5 + i * self.__img_size/10 + self.__item_size/2

    def Draw(self, Xvalue, Ovalue, photos):
        self.__canvas.delete('all')
        self.__canvas.create_image(self.__img_size/2, self.__img_size/2, image=photos[0])

        for i in range(self.__row):
            for j in range(self.__col):
                if self.__arr[i][j] == Xvalue: self.__canvas.create_image(self.__X(j), self.__Y(i), image=photos[1])
                if self.__arr[i][j] == Ovalue: self.__canvas.create_image(self.__X(j), self.__Y(i), image=photos[2])
                if self.__arr[i][j] == -Xvalue: self.__canvas.create_image(self.__X(j), self.__Y(i), image=photos[3])
                if self.__arr[i][j] == -Ovalue: self.__canvas.create_image(self.__X(j), self.__Y(i), image=photos[4])

    def DrawFullEnd(self):
        messagebox.showinfo("Ничья", "Никто не победил.")

    def DrawTheEnd(self, player):
        messagebox.showinfo("Победа", f"Игрок {player} победил!")

    def printTable(self):
        for i in range(self.__row):
            for j in range(self.__col):
                print(self.__arr[i][j], end = " ")
            print("")


