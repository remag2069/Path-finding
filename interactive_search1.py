import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

class node():
    def __init__(self,parent,action,pos,heuristic=-1):
        self.parent=parent
        self.action=action
        self.pos=pos
        self.heuristic=heuristic
        self.steps=0
        if self.parent!=None:
            parent=self.parent
            while parent!=None:
                self.steps+=1
                parent=parent.parent


class stack():
    def __init__(self):
        self.storage=[]
    def add(self,node):
        self.storage.append(node)
    def remove(self):
        node=self.storage[-1]
        self.storage=self.storage[:-1]
        return node
    def show_storage(self):
        for i in self.storage:
            print(i.parent,i.action,i.pos)
    def size(self):
        return len(self.storage)

class queue(stack):
    def remove(self):
        node=self.storage[0]
        self.storage=self.storage[1:]
        return node

class A_star(stack):
    def remove(self):
        min=0
        for i in range(len(self.storage)):
            if self.storage[i].heuristic+self.storage[i].steps<self.storage[min].heuristic+self.storage[min].steps:
                min=i
        node=self.storage.pop(min)
        return node
        


window=tk.Tk()

class buttons():
    def __init__(self,pos):
        self.pos=pos
        self.state=0
        self.button=Button(window,text='*',command=self.switch,bg="black")
        self.button.grid(row = pos[0], column = pos[1])

    def switch(self):
        if self.button['bg']=='white':
            self.button.configure(bg = "black")
            self.button.configure(text = "*")
            self.state=0
        else:
            self.button.configure(bg = "white")
            self.button.configure(text = " ")
            self.state=1

    def starting(self):
        self.button.configure(bg = "yellow")
        self.button.configure(text = "*")
        self.state=10

    def ending(self):
        self.button.configure(bg = "green")
        self.button.configure(text = "*")
        self.state=5


def show(data):
    plt.imshow(data)
    plt.show()
        

def parse(b):
    result=[]
    for i in range(len(b)):
        temp=[]
        for j in range(len(b[0])):
            temp.append(b[i][j].state)
        result.append(temp)
    
    result=np.array(result)
    show(result)
    return result

b=[]
height=input("enter the height")
breadth=input("enter the breadth")
if height == "":
    height=5
    breadth=5
else:
    height=int(height)
    breadth=int(breadth)
for i in range(height):
    t=[]
    for j in range(breadth):
        t.append(buttons([i,j]))
    b.append(t)
b[height-1][0].starting()
b[0][breadth-1].ending()





def check_neighbours(parent,maze,finish):
    x,y=parent.pos
    x=x[0]
    y=y[0]
    neighbours=[]
    try:
        if maze[x+1][y]:
            neighbours.append(node(parent,"down",np.array([[x+1],[y]]),abs(x+1-finish.pos[0][0])+abs(y-finish.pos[1][0])))
    except:
        pass
    try:
        if maze[x][y+1]:
            neighbours.append(node(parent,"right",np.array([[x],[y+1]]),abs(x-finish.pos[0][0])+abs(y+1-finish.pos[1][0])))
    except:
        pass
    try:
        if x-1<0 or y<0:
            pass
        elif maze[x-1][y]:
            neighbours.append(node(parent,"up",np.array([[x-1],[y]]),abs(x-1-finish.pos[0][0])+abs(y-finish.pos[1][0])))
    except:
        pass
    try:
        if x<0 or y-1<0:
            pass
        elif maze[x][y-1]:
            neighbours.append(node(parent,"left",np.array([[x],[y-1]]),abs(x-finish.pos[0][0])+abs(y-1-finish.pos[1][0])))
    except:
        pass

    return neighbours


def not_explored(node,explored):
    for i in explored:
        if i.pos[0][0]==node.pos[0][0] and i.pos[1][0]==node.pos[1][0]:
            return 0
    return 1

def show_path(end_node,maze):
    node=end_node
    length=0
    while node.parent.parent != None:
        length+=1
        node=node.parent
        x,y=node.pos
        x=x[0]
        y=y[0]
        maze[x][y]=7
    print('actual length',length)
    show(maze)





def solve_maze(maze,type='stack'):
    explored=[]
    if type== "stack":
        check=stack()
    elif type=="queue":
        check=queue()
    elif type=="A*":
        check=A_star()
    
    finish=node(None,None,np.where(maze==5),0)
    start=node(None,None,np.where(maze==10),abs(np.where(maze==10)[0][0]-np.where(maze==5)[0][0])+abs(np.where(maze==10)[1][0]-np.where(maze==5)[1][0]))

    check.add(start)
    cost=0
    maze_show_all=np.array(maze)

    while(True):
        cost+=1
        if check.size()==0:
            print("no solution")
            break
        curr_node=check.remove()
        explored.append(curr_node)
        curr_x,curr_y=curr_node.pos
        curr_x=curr_x[0]
        curr_y=curr_y[0]
        maze_show_all[curr_x][curr_y]=7
        if maze[curr_x][curr_y]==5:
            print("solution found")
            end_node=curr_node
            break
        neighbours=check_neighbours(curr_node,maze,finish)
        
        for i in neighbours:
            # print('****************\n',i)
            if not_explored(i,explored):
                # print('##################\n',i)
                check.add(i)
        # print('#############')
        # check.show_storage()

    print("cost",cost)
    show_path(end_node,maze)
    show(maze_show_all)


def bfs():
    maze=parse(b)
    solve_maze(maze,"queue")

def dfs():
    maze=parse(b)
    solve_maze(maze,"stack")

def a_star():
    maze=parse(b)
    solve_maze(maze,"A*")

menubar = tk.Menu(window)
menu=tk.Menu(menubar,tearoff=0)
menu.add_command(label='Breadth-first-search',command=bfs)
menu.add_command(label='Depth-first-search',command=dfs)
menu.add_command(label='A*',command=a_star)
menubar.add_cascade(label="Menu", menu=menu)

window.config(menu=menubar)

# print("hi")

window.mainloop()