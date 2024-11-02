import sys
import copy

sys.setrecursionlimit(5000)

class StateSpace:
    open_close_set = set()

    def __init__(self,matrix):
        self.matrix = matrix

    def get_matrix(self):
        return self.matrix
    def to_string(self):
        return ''.join(''.join(row) for row in self.get_matrix())
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

    def move_box(self,x,y,a,b):
#        (x,y) -> move to do
#        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,'.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,'.')

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
            # print("new state")
            # state.print_matrix()
            # print('\n')
            Search.path.append(state.matrix)
            if state.is_completed():
                return True
            for move in self.moves :
                # print(move)
                # Search.path.append(move)
                matrix = copy.deepcopy(state.get_matrix())
                child = StateSpace(matrix)
                res = child.get_child(move[0], move[1])
                # child.print_matrix()
                if res is not None:
                    child_string = child.to_string()
                    if child_string not in StateSpace.open_close_set:
                        if self.search(child):
                            return True
                        
            Search.path.pop()
            return False
                
    

# matrix = []
# level = 1
# if level < 1:
#     print("ERROR: Level "+str(level)+" is out of range")
#     sys.exit(1)
# else:
#     file = open('levels','r')
#     level_found = False
#     for line in file:
#         row = []
#         if not level_found:
#             if  "Level "+str(level) == line.strip():
#                 level_found = True
#         else:
#             if line.strip() != "":
#                 row = []
#                 for c in line:
#                     if c != '\n' :
#                         row.append(c)
#                     elif c == '\n': #jump to next row when newline
#                         continue
#                     else:
#                         print("ERROR: Level "+str(level)+" has invalid value "+c)
#                         sys.exit(1)
#                 matrix.append(row)
#             else:
#                 break

start_state = StateSpace(matrix=matrix)
moves = [(0,-1),(0,1),(-1,0),(1,0)]

    
SE = Search('DFS',start_state,moves)







    