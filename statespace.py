import sys
import copy
import json

sys.setrecursionlimit(5000)

class StateSpace:
    open_close_set = set()

    def __init__(self, filename=None, weights=None, boxes=None, matrix=None):
        if filename:
            self.load_from_file(filename)
        else:
            self.weights = weights if weights is not None else []
            self.box = boxes if boxes is not None else []
            self.matrix = matrix if matrix is not None else []

            # Nếu không có trọng số hoặc hộp nào được cung cấp, hãy đặt chúng thành mặc định
            if not self.weights:
                self.weights = [1] * len(self.box)  # Mặc định trọng số bằng 1 cho mỗi hộp
            for i, weight in enumerate(self.weights):
                if i < len(self.box):  # Kiểm tra nếu index i không vượt quá số lượng hộp
                    self.box[i].append(weight)

    def load_from_file(self,filename):
        self.matrix = []
        self.box = [] 
        with open(filename,'r') as f :
            first_line = f.readline().strip()
    
            # Tách các số từ dòng đầu tiên và chuyển thành int
            self.weights = [int(num) for num in first_line.split()]
            for i, line in enumerate(f):
                row = []
                if line.strip() != "":
                        row = []
                        for j, c in enumerate(line):
                            if c != '\n' :
                                row.append(c)
                                if c=='*' or c =='$':
                                    self.box.append([j,i])
                            elif c == '\n': #jump to next row when newline
                                continue
                            
                        self.matrix.append(row)
                else:
                    break
            for i, weight in enumerate(self.weights):
                self.box[i].append(weight)

    def get_matrix(self):
        return self.matrix
    def to_string(self):
        s = []
        for row in self.get_matrix():
            s.append("".join(row))
        for box in self.box:
            s.append(str(box[2]))

        return "".join(s)
        

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self,x,y):
        return self.matrix[y][x]

    def set_content(self,x,y,content):
        self.matrix[y][x] = content

    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self,x,y):
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
    def set_box(self,x,y,z,t): #box (x,y) thành box(z,t)
        for box in self.box:
            if box[0]==x and box[1]==y:
                box[0]= z
                box[1] = t
    def move_box(self,x,y,a,b):
#        (x,y) -> move to do
#        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,' ')
            self.set_box(x,y,x+a,y+b)
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
            self.set_box(x,y,x+a,y+b)
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,'.')
            self.set_box(x,y,x+a,y+b)
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,'.')
            self.set_box(x,y,x+a,y+b)


    def get_child(self,x,y): 
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
            return self.matrix 
                
        elif self.can_push(x,y):      
            current = self.worker()
            future = self.next(x,y)
            future_box = self.next(x+x,y+y)

            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')

            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
    
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')

            if current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@')

            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')

            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
            return self.matrix    
        return None

class Search :
    path = []

    def __init__(self,search_alg, state, moves):
        self.search_alg = search_alg
        self.start = state
        self.moves = moves
    
    def search(self,state):
        if self.search_alg == 'DFS':
            StateSpace.open_close_set.add(state.to_string())
            if state.is_completed():
                return True
            for move in self.moves[::-1] :
                Search.path.append(move)
                
                child = copy.deepcopy(state)
                res = child.get_child(move[0], move[1])
                if res is not None:
                    child_string = child.to_string()
                    #print(child_string)
                    if child_string not in StateSpace.open_close_set:
                        if self.search(child):
                            return True
                Search.path.pop()

            return False
                
    

# start_state = StateSpace('levels_weight')
# start_state.print_matrix()
# print(start_state.box)
# print(start_state.to_string())
# moves = [(0,-1),(0,1),(-1,0),(1,0)]
# SE = Search('DFS',state=start_state,moves=moves)
# SE.search(state=start_state)
# print(SE.path)
    

# while True:
#     command = input()
#     a = 0
#     b = 0 
#     if command == 'u':
#         a = 0
#         b = -1
#     elif command =='d':
#         a = 0 
#         b = 1
#     elif command == 'l':
#         a = -1
#         b = 0
#     elif command == 'r':
#         a = 1
#         b = 0
#     elif command == 'q':
#         break
#     start_state.get_child(a,b)
#     start_state.print_matrix()
#     print(start_state.box)
#     print(start_state.to_string())





    