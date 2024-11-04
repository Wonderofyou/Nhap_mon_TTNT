#!../bin/python

import sys
import pygame
import time
import copy
import queue

from statespace import StateSpace, Search

class game:

    def is_valid_value(self,char):
        if ( char == ' ' or #floor
            char == '#' or #wall
            char == '@' or #worker on floor
            char == '.' or #dock
            char == '*' or #box on dock
            char == '$' or #box
            char == '+' ): #worker on dock
            return True
        else:
            return False

    def __init__(self,level):
        self.queue = queue.LifoQueue()
        #if level < 1 or level > 50:
        if level < 1 or level > 50:
            print("ERROR: Level "+str(level)+" is out of range")
            sys.exit(1)
        else:
            formatted_level = f"{level:02}"
            self.start_state = StateSpace(f"input-{formatted_level}.txt")
            
            

    def load_size(self):
        x = 0
        y = len(self.start_state.get_matrix())
        for row in self.start_state.get_matrix():
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)
    
    def load_move_from_file(self, output_file):
        # Initialize the dictionary to store results
        result = {'algorithm': [], 'path': [], 'instruction':[]}

        # Open and read the file
        with open(output_file, 'r') as file:
            # Initialize variables to keep track of current algorithm and path
            current_algorithm = None
            current_path = None

            # Read through each line in the file
            for line in file:
                # Check if the line indicates a new algorithm
                if line.startswith('BFS') or line.startswith('DFS') or line.startswith('A*') or line.startswith('UCS'):
                    # Extract algorithm name and store it
                    current_algorithm = line.split()[0]
                    result['algorithm'].append(current_algorithm)

                # Check if the line represents a path (assumes paths do not start with 'Steps')
                elif not line.startswith('Steps') and current_algorithm:
                    # Extract and store the path for the current algorithm

                    current_path = line.strip()
                    instruction = []
                    for command in current_path:
                        if command.lower() == 'l':
                            instruction.append((0, -1))
                        elif command.lower() == 'r':
                            instruction.append((0, 1))
                        elif command.lower() == 'u':
                            instruction.append((-1, 0))
                        elif command.lower() == 'd':
                            instruction.append((1, 0))
                    
                    result['path'].append(current_path)
                    result['instruction'].append(instruction)

        # Print the dictionary
        return result
#     def unmove(self): 
#         if not self.queue.empty():
#             movement = self.queue.get()
#             if movement[2]:
#                 current = self.worker()
#                 self.move(movement[0] * -1,movement[1] * -1, False)
#                 self.move_box(current[0]+movement[0],current[1]+movement[1],movement[0] * -1,movement[1] * -1)
#             else:
#                 self.move(movement[0] * -1,movement[1] * -1, False)



def print_game(matrix,screen):
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == ' ': #floor
                screen.blit(floor,(x,y))
            elif char == '#': #wall
                screen.blit(wall,(x,y))
            elif char == '@': #worker on floor
                screen.blit(worker,(x,y))
            elif char == '.': #dock
                screen.blit(docker,(x,y))
            elif char == '*': #box on dock
                screen.blit(box_docked,(x,y))
            elif char == '$': #box
                screen.blit(box,(x,y))
            elif char == '+': #worker on dock
                screen.blit(worker_docked,(x,y))
            x = x + 32
        x = 0
        y = y + 32


def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def display_end(screen):
    message = "Level Completed"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string))
  while 1:
    inkey = get_key()
    if inkey == pygame.K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == pygame.K_RETURN:
      break
    elif inkey == pygame.K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + "".join(current_string))
  return "".join(current_string)

def start_game():
    start = pygame.display.set_mode((320,240))
    level = int(ask(start,"Select Level"))
    if level > 0:
        return level
    else:
        print("ERROR: Invalid Level: "+str(level))
        sys.exit(2)

wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/box.png')
box_docked = pygame.image.load('images/box_docked.png')
worker = pygame.image.load('images/worker.png')
worker_docked = pygame.image.load('images/worker_dock.png')
docker = pygame.image.load('images/dock.png')
background = 255, 226, 191
pygame.init()


while True:
    # Chọn lại level khi trò chơi hoàn tất
    
    level = start_game()
    game = game(level)

    size = game.load_size()
    screen = pygame.display.set_mode(size)


    

    print_game(game.start_state.get_matrix(), screen)
    display_box(screen,"Computing...")
    pygame.display.update()


    move_list = game.load_move_from_file('output-02.txt')['instruction'][0]
    print(move_list)
    index = 0 
    is_drawn = True  # Khởi tạo với True để bắt đầu di chuyển đầu tiên
        
    while True:

        # Chỉ thực hiện di chuyển nếu lần cập nhật màn hình trước đó đã hoàn tất
        if is_drawn and index < len(move_list):
            dx, dy = move_list[index]
            game.start_state.get_child(dx, dy)  # Thực hiện di chuyển
            index += 1
            is_drawn = False  # Đặt lại flag, chờ việc vẽ hoàn tất

        # Cập nhật màn hình
        print_game(game.start_state.get_matrix(), screen)
        pygame.display.update()
        is_drawn = True  # Đặt lại flag sau khi cập nhật xong màn hình

        # Kiểm tra xem game đã hoàn tất hay chưa
        if game.start_state.is_completed():
            pygame.display.update()
            display_end(screen=screen)
            pygame.time.delay(1000)  # Đợi một lúc trước khi quay lại màn hình chọn
            break  # Quay lại vòng lặp bên ngoài để chọn level mới

        pygame.time.delay(50)



