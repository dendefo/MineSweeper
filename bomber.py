from tkinter import *
from random import choice
from time import time
from threading import Timer
import itertools

class Pole(object): #создаем Класс поля, наследуемся от Object
    def __init__(self,master,row, column): #Инициализация поля. master - окно Tk().
        self.button = Button(master, text = '   ') #Создаем для нашего поля атрибут 'button'
        self.mine = False #Переменная наличия мины в поле
        self.value = 0 #Кол-во мин вокруг
        self.viewed = False #Открыто/закрыто поле
        self.flag = 0 #0 - флага нет, 1 - флаг стоит, 2 - стоит "?"
        self.clr = 'black' #Цвет текста
        self.bg = None #Цвет фона
        self.row = row #Строка
        self.column = column #Столбец
        
    def around(self):
        in_range = lambda index, max_index: 0 <= index < max_index  # проверка на вхождение в допустимый диапазон
        diffs = (-1, 0, 1)  # где находятся соседи относительно текущего
        adjacents = list()  # список соседей
        for i, j in itertools.product(diffs, diffs):  # https://docs.python.org/3/library/itertools.html#itertools.product
                if i == j == 0:
                    continue # исключаем текущий элемент
                next_row, next_col = self.row + i, self.column + j
                if in_range(next_row, len(buttons)) and in_range(next_col, len(buttons[0])):
                    adjacents.append([next_row, next_col])
        return adjacents
    
    def view(self,event):
        if mines == []: #При первом нажатии
            self.seter(0) #Устанавливаем мины
        if self.value == 0: #Устанавливаем цвета. Можно написать и для 6,7 и 8, но у меня закончилась фантазия
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
        elif self.value == 5:
            self.clr = 'pink'
        elif self.value == 6:
            self.clr = 'orange'
        
        if self.mine and not self.viewed and not self.flag: #Если в клетке есть мина, она еще не открыта и на ней нет флага
            self.button.configure(text = 'B', bg = 'red') #Показываем пользователю, что тут есть мина
            self.viewed = True #Говорим, что клетка раскрыта
            for q in mines:
                buttons[q[0]][q[1]].view('<Button-1>') #Я сейчас буду вскрывать ВСЕ мины
            end('Вы проиграли:-(','В следующий раз повезет больше') #Вызываем окно проигрыша
            exit()
        
        elif not self.viewed and not self.flag: #Если мины нет, клетка не открыта и флаг не стоит
            self.button.configure(text = self.value, fg = self.clr, bg = self.bg) #выводим в текст поля значение
            self.viewed = True
            if self.value == None: #Если вокруг нет мин
                for k in self.around():
                    buttons[k[0]][k[1]].view('<Button-1>') #Открываем все поля вокруг

            return

        if self.viewed: #Если необходимык флаги поблизости поставлены (вне зависимости от правильности ответа), при нажатии на ячейку открывает соседниии ячейки
            ar = self.around()
            flags_nearby = 0
            for i in ar:
                x_coo = i[0]
                y_coo = i[1]
                if buttons[x_coo][y_coo].flag == 1:
                    flags_nearby+=1
            if self.value == flags_nearby:
                for i in ar:
                    x_coo = i[0]
                    y_coo = i[1]
                    
                    if not buttons[x_coo][y_coo].viewed and not buttons[x_coo][y_coo].flag:
                        buttons[x_coo][y_coo].view('<Button-1>')
        
    def setFlag(self,event):
        if self.flag == 0 and not self.viewed: #Если поле не открыто и флага нет
            self.flag = 1 #Ставим флаг
            self.button.configure(text = 'F', bg = 'yellow') #Выводим флаг
            flags.append([self.row,self.column]) #Добавляем в массив флагов
        elif self.flag == 1: #Если флаг стоим
            self.flag = 2 #Ставим значение '?'
            self.button.configure(text = '?', bg = 'blue') #Выводим его
            flags.pop(flags.index([self.row,self.column])) #Удаляем флаг из массива флагов
        elif self.flag == 2: #Если вопрос
            self.flag = 0 #Устанавливаем на отсутствие флага
            self.button.configure(text = '   ', bg = 'white') #Выводим пустоту
        if sorted(mines) == sorted(flags) and mines != []: #если массив флагов идентичен массиву мин
            end('Вы выиграли:-)','Поздравляем!') #Сообщаем о победе

    def seter(self,q):
        if q == bombs: #Если кол-во установленных бомб = кол-ву заявленных
            for i in buttons: #Шагаем по строкам
                for j in i: #Шагаем по полям в строке i
                    for k in j.around(): #Шагаем по полям вокруг выбранного поля j
                        if buttons[k[0]][k[1]].mine: #Если в одном из полей k мина
                            buttons[buttons.index(i)][i.index(j)].value+=1 #То увеличиваем значение поля j
            return
        a = choice(buttons) #Выбираем рандомную строку
        b = choice(a) #Рандомное поле
        if [buttons.index(a),a.index(b)] not in mines and [buttons.index(a),a.index(b)] not in self.around() and [buttons.index(a),a.index(b)] != [self.row,self.column]: #Проверяем, что выбранное поле не выбиралось до этого и, что не является полем на которую мы нажали (или окружающим ее полем)
            b.mine = True #Ставим мину
            mines.append([buttons.index(a),a.index(b)]) #Добавляем ее в массив 
            self.seter(q+1) #Вызываем установщик, сказав, что еще одна мина уже есть
        else:
            self.seter(q) #Вызываем установщик еще раз


def end(title, string):
    global root
    global start_time
    start_time = -1
    loseWindow = Tk()
    loseWindow.title(title)
    loseWindow.geometry('300x100')
    loseLabe = Label(loseWindow, text = string)
    loseLabe.pack()
    mines = []
    loseWindow.resizable(False,False)
    root.destroy()
    loseWindow.mainloop()


def cheat(event):
        for t in mines:
            buttons[t[0]][t[1]].setFlag('<Button-1>')

def game(high,lenght): #получаем значения
    global root
    root = Tk() 
    root.title('Сапер') 
    global buttons
    global mines
    global flags
    flags = [] #Массив, содержащий в себе места, где стоят флажки
    mines = [] #Массив, содержащий в себе места, где лежат мины
    buttons = [[Pole(root,row,column) for column in range(high)] for row in range(lenght)] #Двумерный массив, в котором лежат поля
    for i in buttons: #Цикл по строкам
        for j in i: #Цикл по элементам строки
            j.button.grid(column = i.index(j), row = buttons.index(i), ipadx = 7, ipady = 1) #Размещаем все в одной сетке при помощи grid
            j.button.bind('<Button-1>', j.view) #Биндим открывание клетки
            j.button.bind('<Button-3>', j.setFlag) #Установка флажка
            j.button.configure(bg = 'white')
    buttons[0][0].button.bind('<Control-Button-1>', cheat) #создаем комбинацию клавиш для быстрого решения
    root.resizable(False,False) #запрещаем изменения размера
    root.mainloop()

global start_time

def bombcounter(): 
    global bombs 
    if mineText.get('1.0', END) == '\n': #Проверяем наличие текста
        bombs = 99 #Если текста нет, то по стандарту кол-во бомб - 10
    else:
        bombs = int(mineText.get('1.0', END)) #Если текст есть, то это и будет кол-во бомб
    if highText.get('1.0', END) == '\n':
        high = 30
    else:
        high = int(highText.get('1.0', END))
    if lenghtText.get('1.0', END) == '\n':
        lenght = 16
    else:
        lenght = int(lenghtText.get('1.0', END))
    global start_time
    start_time = int(time())
    timeCounter()
    game(high,lenght) #Начинаем игру, передавая кол-во полей
    
def timeCounter(): #кривой таймер. Работает и норм
    if start_time == -1:
        return
    counter = Timer(1,timeCounter)
    counter.start()
    timeLabe.configure(text = 'Время: ' + str(int(time())- start_time))
    
    
    
settings = Tk() #Создаем окно
settings.title('Настройки') #Пишем название окна
settings.geometry('200x150') #Задаем размер
mineText = Text(settings, width = 5, height = 1) #Создаем поля для ввода текста и пояснения
mineLabe = Label(settings, height = 1, text = 'Бомбы:')
highText = Text(settings, width = 5, height = 1)
highLabe = Label(settings, height = 1, text = 'Ширина:')
lenghtText = Text(settings, width = 5, height = 1)
lenghtLabe = Label(settings, height = 1, text = 'Высота:')
mineBut = Button(settings, text = 'Начать:', command = bombcounter) #Создаем кнопку
global timeLabe
timeLabe = Label(settings, height = 1, width = 10, text = '00:00')
mineBut.place(x = 70, y = 90)  #Размещаем это все
mineText.place(x = 75, y = 5)
mineLabe.place(x = 5, y = 5)
highText.place(x = 75, y = 30)
highLabe.place(x = 5, y = 30)
lenghtText.place(x = 75, y = 55)
lenghtLabe.place(x = 5, y = 55)
timeLabe.place(x = 5, y = 117)
settings.resizable(False,False)
settings.mainloop() 
