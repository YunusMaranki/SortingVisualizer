import dearpygui.dearpygui as dpg
import threading
import random
import time

from numpy import insert
from algorithms import *

dpg.create_context()

algorithmList = [bubbleSort,insertionSort]
algorithmNames = ["Bubble Sort","Insertion Sort"]

GREEN = (10,256,150)


sorting = False


class windowInformation:
    def __init__(self,height,width,headerheight,columns):
        self.height = height
        self.width = width
        self.headerheight = headerheight
        self.columns = columns
        self.bodyheight = height-headerheight
        self.columnwidth = (width-15)/columns
        self.columnheight = self.bodyheight/columns

w = windowInformation(650,1000,150,50)

class Board:
    def __init__(self,parent):
        self.parent = parent
        self.columns = [Column(x,GREEN) for x in range(w.columns)]
        self.length = w.columns
        self.ids = []
        random.shuffle(self.columns)

    def shuffle(self):
        random.shuffle(self.columns)

    def swap(self,indexA,indexB):
        self.columns[indexA],self.columns[indexB] = self.columns[indexB],self.columns[indexA]
        dpg.configure_item(self.ids[indexA],pmin=[indexA*w.columnwidth,w.bodyheight-(self.columns[indexA].height+1)*w.columnheight-5])
        dpg.configure_item(self.ids[indexB],pmin=[indexB*w.columnwidth,w.bodyheight-(self.columns[indexB].height+1)*w.columnheight-5])

    def initalDraw(self):
        dpg.delete_item(self.parent,children_only=True)
        self.ids = [] 
        for i, num in  enumerate([x.height for x in self.columns]):
            id = dpg.draw_rectangle([i*w.columnwidth,w.bodyheight-(num+1)*w.columnheight-5],[(i+1)*w.columnwidth,w.bodyheight-5],fill=GREEN,parent=self.parent)
            self.ids.append(id)

class Column:
    def __init__(self,height,color):
        self.height = height
        self.color = color
    
    def __lt__(self,otherColumn):
        return self.height<otherColumn.height

def value(sender):
    print(sender)

def startButton(sender):
    global sorting, shuffle, algorithm
    if sorting:
        sorting = False
        dpg.configure_item(shuffle,enabled=True)
        dpg.configure_item(algorithm,enabled=True)
        dpg.configure_item(sender,label="start")
    else:
        sorting = True
        dpg.configure_item(shuffle,enabled=False)
        dpg.configure_item(algorithm,enabled=False)
        dpg.configure_item(sender,label="stop")

def shuffleButton():
    global board,gen,w,columnSlider,algorithm
    w = windowInformation(w.height,w.width,w.headerheight,dpg.get_value(columnSlider))
    board.columns = [Column(x,GREEN) for x in range(w.columns)]
    board.length = w.columns
    board.shuffle()
    board.initalDraw()
    #gen = bubbleSort(board)
    gen = algorithmList[algorithmNames.index(dpg.get_value(algorithm))](board)
    print(gen)

def algoList():
    global gen,algorithm,algorithmList,algorithmNames,board
    gen = algorithmList[algorithmNames.index(dpg.get_value(algorithm))](board)
    print(gen)

def gameLoop():
    global sorting, start
    while 1:
        if sorting:
            time.sleep(0.1)
            try:
                next(gen)
                pass
            except StopIteration:
                sorting = False
                dpg.configure_item(shuffle,enabled=True)
                dpg.configure_item(algorithm,enabled=True)
                dpg.configure_item(start,label="start")

header = dpg.add_window(label="Controlls",width=w.width,height=w.headerheight,no_close=True,no_title_bar=True,no_resize=True,no_move=True)

start = dpg.add_button(label="Start",callback=startButton,parent=header)
shuffle = dpg.add_button(label="Shuffle",callback=shuffleButton,parent=header)
algorithm = dpg.add_combo(label="algorithms",items=algorithmNames,default_value="Insertion Sort",parent=header,callback=algoList)
columnSlider = dpg.add_slider_int(label="columns",default_value=50, max_value=300,min_value=10,parent=header)

body = dpg.add_window(label="main",width=w.width,height=w.bodyheight,pos=(0,w.headerheight),no_close=True,no_title_bar=True,no_resize=True,no_move=True)
board = Board(body)
board.initalDraw()

gen = algorithmList[algorithmNames.index(dpg.get_value(algorithm))](board)
gen = insertionSort(board)
thread = threading.Thread(target=gameLoop)
thread.start()

dpg.create_viewport(title="Sorting Visualizer",width=w.width,height=w.height,resizable=False,)

dpg.setup_dearpygui()
dpg.show_viewport()

#while dpg.is_dearpygui_running():
    #dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()
