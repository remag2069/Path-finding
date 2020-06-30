import matplotlib.pyplot as plt
import numpy as np

class node():
    def __init__(self,parent,action,pos):
        self.parent=parent
        self.action=action
        self.pos=pos
        # self.


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


def show(data):
    plt.imshow(data)
    plt.show()
        


def parse(maze='maz1.txt'):
    file=open(maze)
    data=file.read()
    t_data=data.split('\n')
    h=len(t_data)
    w=len(t_data[0])
    result=[]
    for i in range(h):
        temp=[]
        for j in range(w):
            if t_data[i][j]=='#':
                temp.append(0)
            elif t_data[i][j]=='A' or t_data[i][j]=='a':
                temp.append(10)
            elif t_data[i][j]=='B' or t_data[i][j]=='b':
                temp.append(5)
            else:
                temp.append(1)
        result.append(temp)
    result=np.array(result)
    show(result)
    return result

def check_neighbours(parent,maze):
    x,y=parent.pos
    x=x[0]
    y=y[0]
    neighbours=[]
    try:
        if maze[x+1][y]:
            neighbours.append(node(parent,"down",np.array([[x+1],[y]])))
    except:
        pass
    try:
        if maze[x][y+1]:
            neighbours.append(node(parent,"right",np.array([[x],[y+1]])))
    except:
        pass
    try:
        if maze[x-1][y]:
            neighbours.append(node(parent,"up",np.array([[x-1],[y]])))
    except:
        pass
    try:
        if maze[x][y-1]:
            neighbours.append(node(parent,"left",np.array([[x],[y-1]])))
    except:
        pass

    return neighbours


def not_explored(node):
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

#################################
maze=parse('maze3.txt')

start=node(None,None,np.where(maze==10))

explored=[]
##################################
check=stack()
check.add(start)

maze_show_all=np.array(maze)

cost=0

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
    neighbours=check_neighbours(curr_node,maze)
    for i in neighbours:
        if not_explored(i):
            check.add(i)
    print('#############')
    check.show_storage()

print("cost",cost)
show_path(end_node,maze)
show(maze_show_all)

