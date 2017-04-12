from tkinter import *
from random import choice
class pole(object):
    def __init__(self,master,row, column):
        self.button = Button(master, text = '   ')
        self.mine = False
        self.value = 0
        self.viewed = False
        self.flag = 0
        self.around = []
        self.clr = 'black'
        self.bg = None
        self.row = row
        self.column = column
    def viewAround(self):
        return self.around
    def setAround(self):
        if self.row == 0:
            self.around.append([self.row+1,self.column])
            if self.column == 0:
                self.around.append([self.row,self.column+1])
                self.around.append([self.row+1,self.column+1])
            elif self.column == len(buttons[self.row])-1:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row+1,self.column-1])
            else:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row,self.column+1])
                self.around.append([self.row+1,self.column+1])
                self.around.append([self.row+1,self.column-1])
        elif self.row == len(buttons)-1:
            self.around.append([self.row-1,self.column])
            if self.column == 0:
                self.around.append([self.row,self.column+1])
                self.around.append([self.row-1,self.column+1])
            elif self.column == len(buttons[self.row])-1:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row-1,self.column-1])
            else:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row,self.column+1])
                self.around.append([self.row-1,self.column+1])
                self.around.append([self.row-1,self.column-1])
        else:
            self.around.append([self.row-1,self.column])
            self.around.append([self.row+1,self.column])
            if self.column == 0:
                self.around.append([self.row,self.column+1])
                self.around.append([self.row+1,self.column+1])
                self.around.append([self.row-1,self.column+1])
            elif self.column == len(buttons[self.row])-1:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row+1,self.column-1])
                self.around.append([self.row-1,self.column-1])
            else:
                self.around.append([self.row,self.column-1])
                self.around.append([self.row,self.column+1])
                self.around.append([self.row+1,self.column+1])
                self.around.append([self.row+1,self.column-1])
                self.around.append([self.row-1,self.column+1])
                self.around.append([self.row-1,self.column-1])
            
    def setValue(self,value):
        self.value = value
    def viewValue(self):
        return self.value
    def setMine(self):
        self.mine = True
    def viewMine(self):
        return self.mine
    def view(self,event):
        if mines == []:
            seter(0,self.around,self.row,self.column)
        if self.value == 0:
            self.clr = 'yellow'
            self.value = None
            self.bg = 'lightgrey'
        elif self.value == 1:
            self.clr = 'green'
        elif self.value == 2:
            self.clr = 'blue'
        elif self.value == 3:
            self.clr = 'red'
        elif self.value == 4:
            self.clr = 'purple'
        
        if self.mine == True and not self.viewed and not self.flag:
            self.button.configure(text = 'B', bg = 'red')
            self.viewed = True
            for q in mines:
                buttons[q[0]][q[1]].view('<Button-1>')
            lose()
        
        elif not self.viewed and not self.flag:
            self.button.configure(text = self.value, fg = self.clr, bg = self.bg)
            self.viewed = True
            if self.value == None:
                for k in self.around:
                    buttons[k[0]][k[1]].view('<Button-1>')
    def setFlag(self,event):
        if self.flag == 0 and not self.viewed:
            self.flag = 1
            self.button.configure(text = 'F', bg = 'yellow')
            flags.append([self.row,self.column])
        elif self.flag == 1 and not self.viewed:
            self.flag = 2
            self.button.configure(text = '?', bg = 'blue')
            flags.pop(flags.index([self.row,self.column]))
        elif self.flag == 2 and not self.viewed:
            self.flag = 0
            self.button.configure(text = '   ', bg = 'white')
        if sorted(mines) == sorted(flags) and mines != []:
            winer()
def lose():
    loseWindow = Tk()
    loseWindow.title('Вы проиграли:-(')
    loseWindow.geometry('300x100')
    loseLabe = Label(loseWindow, text = 'В следующий раз повезет больше!')
    loseLabe.pack()
    mines = []
    loseWindow.mainloop()

def seter(q, around,row,column): #Получаем 
    if q == bombs:
        for i in range(len(buttons)):
            for j in range(len(buttons[i])):
                for k in buttons[i][j].viewAround():
                    if buttons[k[0]][k[1]].viewMine():
                        buttons[i][j].setValue(buttons[i][j].viewValue()+1)
        return
    a = choice(buttons)
    b = choice(a)
    if [buttons.index(a),a.index(b)] not in mines and [buttons.index(a),a.index(b)] not in around and [buttons.index(a),a.index(b)] != [row,column]:
        b.setMine()
        mines.append([buttons.index(a),a.index(b)])
        seter(q+1,around,row,column)
    else:
        seter(q,around,row,column)
def winer():
    winWindow = Tk()
    winWindow.geometry('300x100')
    winWindow.title('Вы победили!')
    winLabe = Label(winWindow, text = 'Поздравляем!')
    winLabe.pack()
    winWindow.mainloop()

def cheat(event):
        for t in mines:
            buttons[t[0]][t[1]].setFlag('<Button-1>')

def game(high,lenght):
    root = Tk()
    root.bg = ('grey')
    root.title('Сапер')
    global buttons
    global mines
    global flags
    flags = []
    mines = []
    buttons = [[pole(root,j,i) for i in range(high)] for j in range(lenght)]
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            buttons[i][j].button.grid(column = j, row = i, ipadx = 7, ipady = 1)
            buttons[i][j].button.bind('<Button-1>', buttons[i][j].view)
            buttons[i][j].button.bind('<Button-3>', buttons[i][j].setFlag)
            buttons[i][j].setAround()
    buttons[0][0].button.bind('<Control-Button-1>', cheat)
    root.resizable(False,False)
    root.mainloop()

def bombcounter():
    global bombs
    if mineText.get('1.0', END) == '\n':
        bombs = 10
    else:
        bombs = int(mineText.get('1.0', END))
    if highText.get('1.0', END) == '\n':
        high = 9
    else:
        high = int(highText.get('1.0', END))
    if lenghtText.get('1.0', END) == '\n':
        lenght = 9
    else:
        lenght = int(lenghtText.get('1.0', END))
    game(high,lenght)
settings = Tk()
settings.title('Настройки')
settings.geometry('200x150')
mineText = Text(settings, width = 5, height = 1)
mineLabe = Label(settings, height = 1, text = 'Бомбы:')
highText = Text(settings, width = 5, height = 1)
highLabe = Label(settings, height = 1, text = 'Ширина:')
lenghtText = Text(settings, width = 5, height = 1)
lenghtLabe = Label(settings, height = 1, text = 'Высота:')
mineBut = Button(settings, text = 'Начать:', command = bombcounter)
mineBut.place(x = 70, y = 90)
mineText.place(x = 75, y = 5)
mineLabe.place(x = 5, y = 5)
highText.place(x = 75, y = 30)
highLabe.place(x = 5, y = 30)
lenghtText.place(x = 75, y = 55)
lenghtLabe.place(x = 5, y = 55)
settings.mainloop()

