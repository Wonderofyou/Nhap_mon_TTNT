import sys
import copy
from collections import deque


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

import sys
from collections import deque
import copy

class Search:
    def __init__(self, search_alg, state, moves):
        self.search_alg = search_alg
        self.start = state
        self.moves = moves  

    from collections import deque
import sys
import copy

from queue import PriorityQueue

class Search:
    def __init__(self, search_alg, state, moves):
        self.search_alg = search_alg
        self.start = state
        self.moves = moves 
        
    def get_manhattan_distance(self,point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    
    def get_targets(self,state):
        targets = []
        for i, row in enumerate(state.matrix):
            for j, cell in enumerate(row):
                if cell in ['.', '*']:
                    targets.append((i, j))
        return targets
    
    
    def calculate_heuristic(self,state):
        targets = self.get_targets(state)
        
        # Tạo ma trận chi phí từ mỗi box đến mỗi target
        cost_matrix = []
        for box in state.box:
            row = []
            for target in targets:
                # Chi phí = trọng số * khoảng cách Manhattan
                cost = box[2] * self.get_manhattan_distance((box[0], box[1]), target)
                row.append(cost)
            cost_matrix.append(row)
        return self.hungarian_algorithm(cost_matrix)
    
    def hungarian_algorithm(self,cost_matrix):
        if not cost_matrix:
            return 0
        n = len(cost_matrix)
        m = len(cost_matrix[0])
            
        # Đảm bảo ma trận vuông
        size = max(n, m)
        padded_matrix = [[float('inf')] * size for _ in range(size)]
        for i in range(n):
            for j in range(m):
                padded_matrix[i][j] = cost_matrix[i][j]
            
        # Trừ hàng
        for i in range(size):
            min_row = min(padded_matrix[i])
            if min_row != float('inf'):
                for j in range(size):
                    if padded_matrix[i][j] != float('inf'):
                        padded_matrix[i][j] -= min_row
            
        # Trừ cột
        for j in range(size):
            min_col = float('inf')
            for i in range(size):
                if padded_matrix[i][j] < min_col:
                    min_col = padded_matrix[i][j]
            if min_col != float('inf'):
                for i in range(size):
                    if padded_matrix[i][j] != float('inf'):
                        padded_matrix[i][j] -= min_col
            
        # Tìm chi phí nhỏ nhất
        total_cost = 0
        assigned = set()
        for i in range(size):
            min_cost = float('inf')
            min_j = -1
            for j in range(size):
                if j not in assigned and padded_matrix[i][j] < min_cost:
                    min_cost = padded_matrix[i][j]
                    min_j = j
            if min_j != -1:
                assigned.add(min_j)
                if min_cost != float('inf'):
                    total_cost += cost_matrix[i][min_j]
            
        return total_cost 
    
    

    def search(self):
        if self.search_alg == 'DFS':
            stack = deque([(self.start, [], 0, [])])  # Stack holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while stack:
                current_state, path, current_weight, flag = stack.pop()

                if current_state.is_completed():
                    return current_weight, size / (1024 * 1024), path, flag, node

                for move in self.moves:
                    child = copy.deepcopy(current_state)
                    res = child.get_child(move[0], move[1])
                    node += 1

                    if res is not None:
                        child_string = child.to_string()

                        # Chỉ tiến hành nếu trạng thái chưa được thăm
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # Nếu trạng thái hoàn thành, không cần thêm vào ngăn xếp
                                return current_weight+res[0], size / (1024 * 1024), path + [move], flag + [res[1]], node

                            # Thêm trạng thái con vào ngăn xếp với trọng số
                            stack.append((child, path + [move], current_weight+res[0], flag + [res[1]]))


            return 0, size / (1024 * 1024), [], flag, node
        
        elif self.search_alg == 'BFS':
            queue = deque([(self.start, [], 0, [])])  # Queue holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while queue:
                current_state, path, current_weight, flag = queue.popleft()  # Pop from the front of the queue

                if current_state.is_completed():
                    return current_weight, size / (1024 * 1024), path, flag, node

                for move in self.moves:
                    child = copy.deepcopy(current_state)
                    res = child.get_child(move[0], move[1])
                    node += 1

                    if res is not None:
                        child_weight = res[0]  # Weight of the child state
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # If the state is complete, return immediately without adding it to the queue
                                return current_weight + res[0], size / (1024 * 1024), path + [move], flag + [res[1]], node

                            # Add the child state to the queue with the accumulated weight
                            queue.append((child, path + [move], current_weight + res[0], flag + [res[1]]))

            return 0, size / (1024 * 1024), [], flag, node
        
        
        elif self.search_alg == 'AStar':
            pq = PriorityQueue()
            counter = 0
            initial_h = self.calculate_heuristic(self.start)
            pq.put((initial_h, 0, counter, self.start, [], []))
            counter += 1
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)
            while not pq.empty():
                f_score, current_weight, _, current_state, path, flag = pq.get()
        
                if current_state.is_completed():
                    return current_weight, size / (1024 * 1024), path, flag, node
            
                for move in self.moves:
                    child = copy.deepcopy(current_state)
                    res = child.get_child(move[0], move[1])
                    node += 1
            
                    if res is not None:
                        child_string = child.to_string()
                
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)
                    
                            if child.is_completed():
                                return current_weight + res[0], size / (1024 * 1024), path + [move], flag + [res[1]], node
                    
                            # Tính f_score mới = g(n) + h(n)
                            g_score = current_weight + res[0]  # Chi phí thực tế từ start đến node hiện tại
                            h_score = self.calculate_heuristic(child)  # Ước lượng chi phí từ node hiện tại đến goal
                            f_score = g_score + h_score
                    
                            pq.put((f_score, g_score, counter, child, path + [move], flag + [res[1]]))
                            counter += 1
                    
            return 0, size / (1024 * 1024), [], flag, node
            
            
            

 


import os              
import time
def write_to_file(inputfile,outputfile, algorithms, moves = [(0,-1),(0,1),(-1,0),(1,0)]):
    if not os.path.exists(outputfile):
        start_state = StateSpace(filename=inputfile)
        for algorithm in algorithms :
            search_engine = Search(search_alg=algorithm,state=start_state,moves=moves )
            start_time = time.time()
            total_weight,size, path, flag, node  =  search_engine.search()
            end_time = time.time()
            total_time = 1000*(end_time-start_time)
            path_str = []
            for (i,move) in enumerate(path) :
                if move == (0,-1):
                    if flag[i]:
                        path_str.append('L')
                    elif flag[i] ==1:
                        path_str.append('l')

                elif move == (0,1):
                    if flag[i] :
                        path_str.append('R')
                    elif flag[i] ==1:
                        path_str.append('r')
                
                elif move == (-1,0):
                    if flag[i]:
                        path_str.append('U')
                    elif flag[i] ==1:
                        path_str.append('u')

                elif move == (1,0):
                    if flag[i] :
                        path_str.append('D')
                    elif flag[i]:
                        path_str.append('d')
            path_str = "".join(path_str)
            print(len(path),total_weight)
            with open(outputfile,'w') as f:
                f.write(algorithm+'\n')
                f.write(f"Steps: {len(flag)}, Weight: {total_weight}, Node: {node}, Time (ms): {total_time}, Memory(MB): {size}\n")
                f.write(path_str+'\n')

# write_to_file('levels_weight','output',['DFS'])

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





    







    