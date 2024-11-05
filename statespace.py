import sys
<<<<<<< HEAD
import copy
from collections import deque
import heapq
import utils


=======
>>>>>>> 9876863e0b981fa2360546ab4dc2410c6f8e5aac
class StateSpace:
    open_close_set = set()

    def __init__(self, filename=None, weights=None, boxes=None, matrix=None):
        if filename: #init by file
            self.load_from_file(filename)
        else: #init by parameter
            self.weights = weights if weights is not None else []
            self.box = boxes if boxes is not None else []
            self.matrix = matrix if matrix is not None else []

            if not self.weights:
                self.weights = [1] * len(self.box)  # default 1
            for i, weight in enumerate(self.weights):
                if i < len(self.box):  
                    self.box[i].append(weight)

    def load_from_file(self,filename):
        self.matrix = []
        self.box = [] 
        with open(filename,'r') as f :
            first_line = f.readline().strip()
    
            self.weights = [int(num) for num in first_line.split()]
            for i, line in enumerate(f):
                row = []
                if line.strip() != "":
                        row = []
                        for j, c in enumerate(line):
                            if c != '\n' :
                                row.append(c)
                                if c=='*' or c =='$':
                                    self.box.append([i,j])
                            elif c == '\n': #jump to next row when newline
                                continue
                            
                        self.matrix.append(row)
                else:
                    break
            for i, weight in enumerate(self.weights):
                self.box[i].append(weight)

    def get_matrix(self):
        return self.matrix
    def to_string(self):#encoding a State to string 
        s = []
        for row in self.get_matrix():
            s.append("".join(row)) #matrix -> string
        for box in self.box:
            s.append(str(box[2])) #add weight to s

        return "".join(s)
        

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self,x,y):
        return self.matrix[x][y]

    def set_content(self,x,y,content):
        self.matrix[x][y] = content

    def worker(self):
        for i,row in enumerate(self.matrix):
            # print(row)
            for j,pos in enumerate(row):
                if pos == '@' or pos == '+':
                    return (i, j, pos)

    def can_move(self,x,y): #(0,1)(0,-1)
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y) not in ['#','*','$']

    def next(self,x,y):
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y)

    def can_push(self,x,y):
        return (self.next(x,y) in ['*','$'] and self.next(x+x,y+y) in [' ','.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True
    def set_box(self,x,y,z,t): #box(x,y) -> box(z,t)
        for box in self.box:
            if box[0]==x and box[1]==y:
                box[0]= z
                box[1] = t
                return box[2] # get the weight
    def move_box(self,x,y,a,b):
#        (x,y) -> move to do
#        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,' ')#update on matrix only
            weight = self.set_box(x,y,x+a,y+b)#update on self.box
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
            weight =  self.set_box(x,y,x+a,y+b)
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,'.')
            weight =  self.set_box(x,y,x+a,y+b)
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,'.')
            weight = self.set_box(x,y,x+a,y+b)
        return weight

    def can_move_or_push(self,x,y):
        return (self.can_move(x,y) or self.can_push(x,y))
    

    def get_child(self,x,y): #return (weight, push or not)
        if self.can_move(x,y):
            current = self.worker()
            future = self.next(x,y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '@' and future == '.':   
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],'.')
            elif current[2] == '+' and future == '.': 
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'.')
            return (0,False) 
                
        elif self.can_push(x,y):      
            current = self.worker()
            future = self.next(x,y)
            future_box = self.next(x+x,y+y)

            if current[2] == '@' and future == '$' and future_box == ' ':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')

            elif current[2] == '@' and future == '$' and future_box == '.':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
    
            elif current[2] == '@' and future == '*' and future_box == ' ':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '@' and future == '*' and future_box == '.':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')

            if current[2] == '+' and future == '$' and future_box == ' ':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@')

            elif current[2] == '+' and future == '$' and future_box == '.':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '+' and future == '*' and future_box == ' ':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '+' and future == '*' and future_box == '.':
                weight = self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
            return (weight,True)     
        return None


import os              
import time

def write_to_file(inputfile, outputfile, algorithms, moves=[(0, -1), (0, 1), (-1, 0), (1, 0)]):
    start_state = StateSpace(filename=inputfile)
    
    # Clear previous content if needed
    with open(outputfile, 'w') as f:
        pass  # Just open in write mode to clear content
    
    for algorithm in algorithms:
        StateSpace.open_close_set.clear()
        search_engine = Search(search_alg=algorithm, state=start_state, moves=moves)
        start_time = time.time()
        total_weight, size, path, flag, node = search_engine.search()
        end_time = time.time()
        total_time = 1000 * (end_time - start_time)
        
        path_str = []
        for (i, move) in enumerate(path):
            if move == (0, -1):
                path_str.append('L' if flag[i] else 'l')
            elif move == (0, 1):
                path_str.append('R' if flag[i] else 'r')
            elif move == (-1, 0):
                path_str.append('U' if flag[i] else 'u')
            elif move == (1, 0):
                path_str.append('D' if flag[i] else 'd')
                
        path_str = "".join(path_str)
        print(len(path), total_weight)
        
        # Append results to output file
        with open(outputfile, 'a') as f:
            f.write(algorithm + '\n')
            f.write(f"Steps: {len(flag)}, Weight: {total_weight}, Node: {node}, Time (ms): {total_time}, Memory(MB): {size}\n")
            f.write(path_str + '\n')

# write_to_file('input-02.txt', 'output-02.txt', ['BFS', 'DFS'])  #un comment to write path to file, should add A* and UCS in the array



#Uncomment to play game in command line
# start_state = StateSpace('levels_weight')
# start_state.print_matrix()
# print(start_state.box)
# print(start_state.worker())
# while True :
#     command = input()
#     if command == 'l' :
#         start_state.get_child(0,-1)
#     if command == 'r':
#         start_state.get_child(0,1)
#     if command == 'u':
#         start_state.get_child(-1,0)
#     if command == 'd':
#         start_state.get_child(1,0)
#     if command == 'q':
#         break
#     start_state.print_matrix()  
#     print(start_state.box)          





    







    