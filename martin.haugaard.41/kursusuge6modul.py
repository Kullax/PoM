from Tkinter import *
import time

class visLife(object):
    def __init__(self,foerste,naeste,levende):
        '''tk class init.
        Computes dimensions and initalize the screen canvas.'''
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 600, height = 600)
        self.canvas.pack()
        self.cell_width = 0
        self.foerste = foerste
        self.naeste = naeste
        self.levende = levende
        self.cells = []
        self.canvas.pack()

        self.expand = 15
        self.i_min = 0
        self.i_max = 0
        self.j_min = 0
        self.j_max = 0
        self.canvas_i_min = 0
        self.canvas_i_max = 0
        self.canvas_j_min = 0
        self.canvas_j_max = 0
        
        self.root.after(0, self.animation) # Setup mainloop piracy to keep control
        self.root.mainloop()

    def calc_scale(self,bounds):
        '''Internal method for calculating the scale of the cells.'''
        self.i_min, self.i_max, self.j_min, self.j_max = bounds

        change_flag = False

        while self.canvas_i_min > self.i_min:
            self.canvas_i_min -= self.expand
            change_flag = True
        while self.canvas_i_min + 1.5*self.expand < self.i_min:
            self.canvas_i_min += self.expand
            change_flag = True

        while self.canvas_i_max < self.i_max:
            self.canvas_i_max += self.expand
            change_flag = True
        while self.canvas_i_max - 1.5*self.expand > self.i_max:
            self.canvas_i_max -= self.expand
            change_flag = True

        while self.canvas_j_min > self.j_min:
            self.canvas_j_min -= self.expand
            change_flag = True
        while self.canvas_j_min + 1.5*self.expand < self.j_min:
            self.canvas_j_min += self.expand
            change_flag = True

        while self.canvas_j_max < self.j_max:
            self.canvas_j_max += self.expand
            change_flag = True
        while self.canvas_j_max - 1.5*self.expand > self.j_max:
            self.canvas_j_max -= self.expand
            change_flag = True

        if change_flag:
            self.cell_width = min(600.0/(self.canvas_i_max-self.canvas_i_min),600.0/(self.canvas_j_max-self.canvas_j_min))

    def draw_cell(self,i_in,j_in):
        '''Internal method for drawing cells.'''
        i = i_in - self.canvas_i_min
        j = j_in - self.canvas_j_min
        self.canvas.create_rectangle(i*self.cell_width, j*self.cell_width, (i+1)*self.cell_width, (j+1)*self.cell_width, outline='black', fill='red')

    def animation(self):
        '''Main animation loop using the given functions foerste, naeste and levende to update cell generation, define the grid to draw and draw living cells.'''
        self.calc_scale(self.foerste())

        while True:
            try:                
                for i in range(self.i_min,self.i_max):
                    for j in range(self.j_min,self.j_max):
                        if self.levende(i,j):
                            self.draw_cell(i,j)

                self.canvas.update()
                self.canvas.delete("all")
                self.calc_scale(self.naeste())
                time.sleep(0.2)
            except TclError:
                break
