# external modules
from tkinter import *
from PIL import ImageTk, Image
import PIL as pil
from screeninfo import get_monitors
from pygame import mixer
import os

# module of the game
from game import *

# functions
def new():
    global pt, first, n, img_size, item_size
    pt = PaperTable(10, playerX.GetVal(), playerO.GetVal(), canvas, img_size, item_size)
    first = True 
    n = 0
    draw()

def draw():
    global pt, first, n, player, moves, img_size
    pt.Draw(playerX.GetVal(), playerO.GetVal(), photos)
    if first: player.config(text = "Игрок : PlayerX")
    else: player.config(text = "Игрок : PlayerO")
    moves.config(text = f"Кол-во ходов : {3-n}")

    if pt.isDefeated(playerO.GetVal()): 
        pt.DrawTheEnd("playerX")
        new()
    if pt.isDefeated(playerX.GetVal()): 
        pt.DrawTheEnd("playerO")
        new()
    if pt.isFull(): 
        pt.DrawFullEnd()
        new()

def key(event):
    print ("pressed"), repr(event.char)

def callback(event):
    global first, n

    i = int(event.y / (img_size/10))
    j = int(event.x / (img_size/10))
    print (f"clicked at cell: [{i},{j}]")

    if first:
        if pt.isMoveLegal(i, j, playerX.GetVal()):
            pt.Add(i, j, playerX.Move(pt.GetVal(i, j)))
            # draw(playerX.GetVal(), playerO.GetVal())
            n += 1

            if (n == 3):
                first = False
                n = 0
            draw()
    else:
        if pt.isMoveLegal(i, j, playerO.GetVal()):
            pt.Add(i, j, playerO.Move(pt.GetVal(i, j)))
            # draw(playerX.GetVal(), playerO.GetVal())
            n += 1

            if (n == 3):
                first = True
                n = 0
            draw()
def getInfo():
    rules = """
Играют два игрока. Ходят поочередно.\n\nКаждый ход состоит из трех ходиков, во время которых игрок может поставить свой вирус или съесть вирус противника.\n\nХодить можно на клетки, которые соприкасаются (горизонталь, вертикаль, диагональ) с живим вирусом или через цепочку съеденных вирусов противника, которая соприкасается с живим.\n\nВыиграет тот, кто первый съест все вирусы противника.\n\nПриятной игры!
"""
    messagebox.showinfo("Правила игры", f"{rules}")

def skip():
    global first, n
    n += 1
    if n == 3: 
        n = 0
        first = not(first)
    draw()

def lose():
    if first: messagebox.showinfo("Игрок сдался", "Игрок playerX сдался.\nИгрок playerO победил.")
    else: messagebox.showinfo("Игрок сдался", "Игрок playerO сдался.\nИгрок playerX победил.")
    new()
def music(event):
    if mixer.music.get_busy() == True:
        mixer.music.pause()
        lb.config(image=music_off)
    else:
        mixer.music.unpause()
        lb.config(image=music_on)

# initializing the window of the game
win_width = get_monitors()[0].width
win_height = get_monitors()[0].height
scale = 0.8

img_size = round(int(win_height * scale),-2)
item_size = int((img_size/10 - 10))

root = Tk()
root.title('War of Viruses')
root.geometry(f'{img_size + 200}x{img_size}')

full_path = os.path.realpath('__file__')
path, filename = os.path.split(full_path)



resized_img = pil.Image.open(f"{path}/assets/myTable.jpg")

img = ImageTk.PhotoImage(resized_img.resize((img_size , img_size)))


playerXimg_resized = pil.Image.open(f"{path}/assets/playerX.png").resize((item_size, item_size))
playerOimg_resized = pil.Image.open(f"{path}/assets/playerO.png").resize((item_size, item_size))
playerNoX_resized = pil.Image.open(f"{path}/assets/playerNoX+.png").resize((item_size, item_size))
playerNoO_resized = pil.Image.open(f"{path}/assets/playerNoO.png").resize((item_size, item_size))

playerXimg = ImageTk.PhotoImage(playerXimg_resized)
playerOimg = ImageTk.PhotoImage(playerOimg_resized)
playerNoX = ImageTk.PhotoImage(playerNoX_resized)
playerNoO = ImageTk.PhotoImage(playerNoO_resized)
photos = [img, playerXimg, playerOimg, playerNoO, playerNoX]

frame = Frame(root)
frame.pack(fill='both', expand=True)
canvas = Canvas(frame, width=img.width(), height=img.height())
canvas.pack(anchor=NW)

canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)

line_x = img_size + 25
# add labels
player = Label(root, font=('Verdana Bold',15))
player.place(x=line_x, y=10)
moves = Label(root, font=('Verdana', 12))
moves.place(x=line_x,y=40)

# add buttons
info = Button(frame, text="Правила игры", command=getInfo, padx=5, pady=10)
info.place(x=line_x,y=85)

lost = Button(frame, text="Сдаться", command=lose, padx=23, pady=10)
lost.place(x=line_x,y=150)

skip = Button(frame, text="Пропустить ход", command=skip, pady=10)
skip.place(x=line_x,y=215)

exit = Button(frame, text="Выйти", command=root.destroy, padx=5, pady=10)
exit.place(x=line_x,y=img.height() - img.height()/10)

music_on = ImageTk.PhotoImage(pil.Image.open(f"{path}/assets/music_on.png"))
music_off = ImageTk.PhotoImage(pil.Image.open(f"{path}/assets/music_off.png"))
lb = Label(frame, image=music_on)
lb.place(x=line_x, y=290)
lb.bind("<Button-1>", music)

# initializing music
mixer.init()
mixer.music.load(f"{path}/assets/music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(loops = -1)

# initializing game
playerX = Player(1)
playerO = Player(2)
pt = PaperTable(10, playerX.GetVal(), playerO.GetVal(), canvas, img_size, item_size)
first = True 
n = 0
draw()

root.mainloop()