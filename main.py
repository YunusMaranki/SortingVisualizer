import dearpygui.dearpygui as dpg
import threading
import random
import time
from algorithms import *
GREEN = (10,256,150)
RED = (255, 107, 107)

class windowInformation:
    def __init__(self,height,width,headerheight,columns):
        self.height = height
        self.width = width
        self.headerheight = headerheight
        self.columns = columns
        self.bodyheight = height-headerheight
        self.columnwidth = (width-15)/columns
        self.columnheight = self.bodyheight/columns



class Board:
    def __init__(self,parent,windowInfo):
        self.w = windowInfo
        self.parent = parent
        self.columns = [Column(x,GREEN) for x in range(self.w.columns)]
        self.length = self.w.columns
        self.ids = []
        random.shuffle(self.columns)

    def shuffle(self):
        random.shuffle(self.columns)

    def swap(self,indexA,indexB):
        self.columns[indexA],self.columns[indexB] = self.columns[indexB],self.columns[indexA]
        dpg.configure_item(self.ids[indexA],pmin=[indexA*self.w.columnwidth,self.w.bodyheight-(self.columns[indexA].height+1)*self.w.columnheight-5]
                           ,fill=self.columns[indexA].color)
        dpg.configure_item(self.ids[indexB],pmin=[indexB*self.w.columnwidth,self.w.bodyheight-(self.columns[indexB].height+1)*self.w.columnheight-5]
                           ,fill=self.columns[indexB].color)

    def initalDraw(self):
        dpg.delete_item(self.parent,children_only=True)
        self.ids = [] 
        for i, num in  enumerate([x.height for x in self.columns]):
            id = dpg.draw_rectangle([i*self.w.columnwidth,self.w.bodyheight-(num+1)*self.w.columnheight-5],[(i+1)*self.w.columnwidth,self.w.bodyheight-5]
                                    ,fill=GREEN,parent=self.parent,rounding=1)
            self.ids.append(id)

class Column:
    def __init__(self,height,color):
        self.height = height
        self.color = color
    
    def __lt__(self,otherColumn):
        return self.height<otherColumn.height

class Gui:
    def __init__(self):
        dpg.create_context()
        
        self.w = windowInformation(650,1000,150,150)
        self.algorithmList = [bubbleSort,insertionSort]
        self.algorithmNames = ["Bubble Sort","Insertion Sort"]
        self.sorting = False
        
        self.header = dpg.add_window(label="Controlls",width=self.w.width,height=self.w.headerheight,no_close=True,no_title_bar=True,no_resize=True,no_move=True)

        self.start = dpg.add_button(label="Start",callback=self.startButton,parent=self.header)
        self.shuffle = dpg.add_button(label="Shuffle",callback=self.shuffleButton,parent=self.header)
        self.algorithm = dpg.add_combo(label="algorithm",items=self.algorithmNames,default_value="Bubble Sort",parent=self.header,callback=self.algoList)
        self.columnSlider = dpg.add_slider_int(label="columns",default_value=150, max_value=500,min_value=10,parent=self.header)
        self.speedSlider = dpg.add_slider_float(label="speed",default_value=0.7, max_value=0.999,min_value=0.001,parent=self.header)
        self.body = dpg.add_window(label="main",width=self.w.width,height=self.w.bodyheight,pos=(0,self.w.headerheight),no_close=True,no_title_bar=True,no_resize=True,no_move=True)
        
        self.board = Board(self.body,self.w)
        self.board.initalDraw()

        self.gen = self.algorithmList[self.algorithmNames.index(dpg.get_value(self.algorithm))](self.board)

        thread = threading.Thread(target=self.gameLoop)
        thread.start()

        dpg.create_viewport(title="Sorting Visualizer",width=self.w.width,height=self.w.height,resizable=False,)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def startButton(self):
        if self.sorting:
            self.sorting = False
            dpg.configure_item(self.shuffle,enabled=True)
            dpg.configure_item(self.algorithm,enabled=True)
            dpg.configure_item(self.start,label="start")
        else:
            self.sorting = True
            dpg.configure_item(self.shuffle,enabled=False)
            dpg.configure_item(self.algorithm,enabled=False)
            dpg.configure_item(self.start,label="stop")

    def shuffleButton(self):
        self.w = windowInformation(self.w.height,self.w.width,self.w.headerheight,dpg.get_value(self.columnSlider))
        self.board.w = self.w
        self.board.columns = [Column(x,GREEN) for x in range(self.w.columns)]
        self.board.length = self.w.columns
        self.board.shuffle()
        self.board.initalDraw()
        self.gen = self.algorithmList[self.algorithmNames.index(dpg.get_value(self.algorithm))](self.board)


    def algoList(self):
        self.gen = self.algorithmList[self.algorithmNames.index(dpg.get_value(self.algorithm))](self.board)


    def gameLoop(self):
        while 1:
            if self.sorting:
                time.sleep((1-dpg.get_value(self.speedSlider))/10)
                try:
                    next(self.gen)
                    pass
                except StopIteration:
                    self.sorting = False
                    dpg.configure_item(self.shuffle,enabled=True)
                    dpg.configure_item(self.algorithm,enabled=True)
                    dpg.configure_item(self.start,label="start")



if __name__ == "__main__":
    Gui()