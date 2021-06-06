from tkinter import *
import random as rd
from tkinter import messagebox
from PIL import ImageTk, Image
import sys
from tkinter.font import Font


class GameGrid(Frame):     #the game

    def __init__(self, master, panel, height, width, mines_count, player, lv):
        Frame.__init__(self, master)
        self.grid(row=0)
        self.master = master
        self.panel = panel
        if sys.platform == 'win32':     #checking os
            self.platform = 'windows'
        else:
            self.platform = 'macos'
        self.height = height     #storing height, width, mines_count, and player's name
        self.width = width
        self.mines_count = mines_count
        self.player_name = player
        self.lv = lv
        self.play_time = 0     #initiating play_time and other values
        self.lost = False
        self.won = False
        self.notmine = height * width - mines_count     #calculate the number of tiles that are not mines
        flag = Image.open('flag.png')    #creating and storing flag and bomb images
        flag = flag.resize((12, 12), Image.ANTIALIAS)
        bomb = Image.open('bomb.png')
        bomb = bomb.resize((12, 12), Image.ANTIALIAS)
        self.flag = ImageTk.PhotoImage(flag)
        self.bomb = ImageTk.PhotoImage(bomb)
        
        grid_model = [[0]*width for item in [0]*height]     #creating a list to hold 1's and 0's
        while mines_count > 0:                              #1 is mine, 0 is normal
            randi = rd.randint(0, height-1)     #putting mines into the list by generating random coordinates
            randj = rd.randint(0, width-1)      #and storing mine in the corresponding place
            if grid_model[randi][randj] == 0:
                grid_model[randi][randj] = 1
                mines_count -= 1
        self.tiles = {}     #creating Tiles and storing them using dictionary
        for i in range(height):
            for j in range(width):   
                if grid_model[i][j] == 1:
                    self.tiles[i, j] = Tile(self, i, j, True)
                else:       
                    mine_neighbors = 0     #counting nearby mines if Tile in creation is not a mine
                    if i - 1 >= 0:
                        if grid_model[i-1][j] == 1:
                            mine_neighbors += 1
                    if i - 1 >= 0 and j - 1 >= 0:
                        if grid_model[i-1][j-1] == 1:
                            mine_neighbors += 1
                    if i - 1 >= 0 and j + 1 < width:
                        if grid_model[i-1][j+1] == 1:
                            mine_neighbors += 1
                    if j - 1 >= 0:
                        if grid_model[i][j-1] == 1:
                            mine_neighbors += 1
                    if j + 1 < width:
                        if grid_model[i][j+1] == 1:
                            mine_neighbors += 1
                    if i + 1 < height:
                        if grid_model[i+1][j] == 1:
                            mine_neighbors += 1
                    if i + 1 < height and j - 1 >= 0:
                        if grid_model[i+1][j-1] == 1:
                            mine_neighbors += 1
                    if i + 1 < height and j + 1 < width:
                        if grid_model[i+1][j+1] == 1:
                            mine_neighbors += 1
                    
                    self.tiles[i, j] = Tile(self, i, j, False, mine_neighbors)
     
    def reveal_surroundings(self, i, j):     #reveal nearby tiles
        revealing = []
        width = self.width
        height = self.height

        
        if i - 1 >= 0:
            revealing.append(self.tiles[i-1, j])
        if i - 1 >= 0 and j - 1 >= 0:
            revealing.append(self.tiles[i-1, j-1])
        if i - 1 >= 0 and j + 1 < width:
            revealing.append(self.tiles[i-1, j+1])
        if j - 1 >= 0:
            revealing.append(self.tiles[i, j-1])
        if j + 1 < width:
            revealing.append(self.tiles[i, j+1])
        if i + 1 < height:
            revealing.append(self.tiles[i+1, j])
        if i + 1 < height and j - 1 >= 0:
            revealing.append(self.tiles[i+1, j-1])
        if i + 1 < height and j + 1 < width:
            revealing.append(self.tiles[i+1, j+1])


        for tile in revealing:
            tile.reveal()


    def lose(self):     #show if lost, stop the clock
        self.panel.stp = True
        self.lost = True
        if self.platform == 'windows':
            for tile in self.tiles:
                if self.tiles[tile].mine:
                    self.tiles[tile].config(bg='red')
        
        else:    
            for tile in self.tiles:
                if self.tiles[tile].mine:
                    self.tiles[tile].config(image=self.bomb, padx=9, pady=4, bg='red')
                self.tiles[tile].unbind('<Button-1>')
                self.tiles[tile].unbind('<Button-2>')   
        messagebox.showerror(message='Boom, Game Over!!')
        self.score = ScoreBoard(self.master)
        
        
    def win(self):      #show if won, stop the clock, creating a window recording scores
        
        self.panel.stp = True
        self.won = True
        for tile in self.tiles:
            if self.tiles[tile].mine:
                self.tiles[tile].config(image=self.bomb, padx=9, pady=4, bg='red')
            self.tiles[tile].unbind('<Button-1>')
            self.tiles[tile].unbind('<Button-2>')
        messagebox.showinfo(message='Congrats, You Survived ;)')
       
        play_time = str(self.panel.m) + ' mins, ' + str(self.panel.s) + ' secs'
        self.score = ScoreBoard(self.master, self.player_name, play_time, self.lv)
                

class ScoreBoard(Toplevel):

    def __init__(self, master, name=None, time=None, lv=None):
        Toplevel.__init__(self, master)
        self.title('Hall of Fame')                   
        fin_text = ''
        self.lv = lv
        
        if name != None:    #writing in the record if there is one
            self.board = open('ScoreBoard.txt', 'r')    #assigning the text inside ScoreBoard.txt to board_text
            board_text = ''                             #and writing it into ScoreBoard.txt
            for line in self.board:
                board_text = board_text + line
            self.board = open('ScoreBoard.txt', 'w')
            self.record = self.lv + ' ' + name + ' ' + time
            self.board.write(board_text + '\n' + self.record)
            
        self.board = open('ScoreBoard.txt', 'r') #reading text in ScoreBoard and put it on the window

        for line in self.board:
            fin_text = fin_text + line
        self.lbl = Label(self, text=fin_text)
        self.lbl.pack()
        self.geometry('300x300')
        self.board.close()
            
            
            
        
    
class Tile(Label):

    def __init__(self, master, i, j, mine, mine_neighbors=None):
        Label.__init__(self, master, width=2, relief=RAISED)
        self.grid(row=i, column=j)
        self.game = master     #storing row, column, is mine or not, count of nearby mines
        self.mine = mine
        self.row = i
        self.col = j
        self.mine_neighbors = mine_neighbors
        self.revealed = False
        self.marked = False

    def game_start(self):

        self.bind('<Button-1>', self.reveal)    #bind Tile: reveal(left click), mark(right click)
        self.bind('<Button-2>', self.mark)

    def reveal(self, event=None):       #revealing tile
        if self.mine:
            self.game.lose()
            return
        else:
            if not self.revealed:
                self.revealed = True
                self.mark()
                self.unbind('<Button-1>')
                self.unbind('<Button-2>')
                if self.mine_neighbors == 0:    #if no nearby mines, reveal nearby tiles
                    self.config(text='', relief=SUNKEN, bg='lightgrey', image='', padx=1, pady=1)
                    self.game.reveal_surroundings(self.row, self.col)
                else:
                    self.config(text=self.mine_neighbors, relief=SUNKEN, bg='lightgrey', image='', padx=1, pady=1)
                self.game.notmine -= 1

            
            if self.game.notmine == 0:
                self.game.win() 

    def mark(self,event=None):      #marking tile
        if self.game.platform == 'windows':
            if not self.marked:
                self.config(text='*')
                self.marked = True
            else:
                self.config(text='')
                self.marked = False
    
        else:
            if not self.marked:
                self.config(image=self.game.flag, padx=9, pady=4)
                self.marked = True
            else:
                self.config(image='', padx=1, pady=1)
                self.marked = False


class Panel():


    def __init__(self):

        self.level_select = Tk()
        self.level_select.resizable(False,False)
        self.level_select.title('MineSweeper')
        self.font = Font(family='Courier', weight='bold')

        self.easy = Button(self.level_select, text='Novice', fg='green',
                                        padx=10, pady=10, relief=RAISED,
                                        command= lambda: self.lv_select('N'),
                                        font=self.font)
        self.hard = Button(self.level_select, text='Master', fg='red',
                                        padx=10, pady=10, relief=RAISED,
                                        command= lambda: self.lv_select('M'),
                                        font=self.font)
        self.intermediate = Button(self.level_select, text='Expert', fg='purple',
                                        padx=10, pady=10, relief=RAISED,
                                        command= lambda: self.lv_select('E'),
                                        font=self.font)
        self.var = StringVar()
        self.e = Entry(self.level_select, text='Name', font=self.font, relief=SUNKEN, textvariable=self.var)
        font = Font(family='Courier', weight='bold', size=15)
        self.e_label = Label(self.level_select, text="Name:", font=font)

        self.e.grid(row=0, column=1, columnspan=2)
        self.e_label.grid(row=0, column=0, pady=5)
        self.easy.grid(row=1, column=0, pady=10, padx=8, sticky=W)
        self.hard.grid(row=1, column=2, pady=10, padx=10, sticky=E)
        self.intermediate.grid(row=1, column=1, pady=8, padx=5)

        self.stp = True
        self.level = ''



    def update_time(self):     #a stopwatch

        if self.stp == False:
            self.s += 1

            if self.s == 60:
                self.m = self.m + 1
                self.s = 0

            mn = str(self.m)     #making the clock look better by adding a 0 when the number
            sc = str(self.s)     #of second or minute is just one digit, e.g. 01, 06, 09..
            if len(sc) == 1 and len(mn) == 1:
                sc = '0' + sc
                mn = '0' + mn
                self.timer.config(text=mn+':'+sc)
            elif len(mn) == 1 and len(sc) != 1:
                mn = '0' + mn
                self.timer.config(text=mn+':'+sc)
            else:
                sc = '0' + sc
                self.timer.config(text=mn+':'+sc)
     
        self.timer.after(1000, self.update_time)
            
    def start(self, event=None):

        for tile in self.game.tiles:
            self.game.tiles[tile].game_start()

        self.stp = False
        self.update_time()

        self.start_button.config(relief=GROOVE)
        self.start_button.destroy()
        self.exit_button.grid(sticky=E+W, padx=30)

    def lv_select(self, lv):
        if self.var.get():
            player = self.var.get()

            self.level_select.destroy()

            self.root = Tk()
            self.root.title('MineSweeper')
            self.root.resizable(False, False)


            self.start_button = Label(self.root, text='Start', relief=GROOVE, bd=3,
                                      width=8, pady=10)
            self.exit_button = Label(self.root, text='Exit', relief=GROOVE, bd=3,
                                     width=8, pady=10)
            self.start_button.grid(row=2, column=0, sticky=E+W, padx=30)
            self.start_button.bind('<ButtonPress-1>', lambda x: self.start_button.config(relief=SUNKEN))
            self.start_button.bind('<ButtonRelease-1>', self.start)
            self.exit_button.bind('<ButtonPress-1>', lambda x: self.exit_button.config(relief=SUNKEN))
            self.exit_button.bind('<ButtonRelease-1>', lambda x: self.root.destroy())

            self.font = Font(family='Courier', weight='bold')

            self.start_button.config(font=self.font)
            self.exit_button.config(font=self.font)

            self.stp = True
            self.m = 0
            self.s = 0
            self.timer = Label(self.root, text='%s:%s'%('00','00'))
            self.timer.grid(row=1)



            if lv == 'N':
                self.game = GameGrid(self.root, self, 10, 10, 10, player, lv)

            elif lv == 'M':
                self.game = GameGrid(self.root, self, 16, 30, 99, player, lv)

            else:
                self.game = GameGrid(self.root, self, 16, 16, 40, player, lv)







if __name__ == '__main__':   
    play = Panel()
    mainloop()

