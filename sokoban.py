#!../bin/python

import sys
import pygame

from statespace import StateSpace
from search import Search
from game import game




def draw_weight_on_box(number, x, y, image):
    screen.blit(image, (x, y))  # Vẽ hình ảnh đá
    width, height = image.get_size()
    # Tạo phông chữ và render số
    font = pygame.font.SysFont(None, 18)  # Cỡ chữ nhỏ hơn cho phù hợp (18)
    text_surface = font.render(str(number), True, (0, 0, 0))  # Màu đen cho số

    # Tính toán vị trí để số nằm giữa hình tròn
    circle_x, circle_y = x + width // 2, y + height // 2
    text_rect = text_surface.get_rect(center=(circle_x, circle_y))

    # Vẽ hình tròn trắng làm nền cho số
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 12)
    pygame.draw.circle(screen, (0, 0, 0), (circle_x, circle_y), 12, 2)  # Viền đen xung quanh


    # Vẽ số lên hình tròn
    screen.blit(text_surface, text_rect)


def print_game(matrix,screen, boxes=None, scale=0):
    positions = [x[:2] for x in boxes]  # Lấy 2 phần tử đầu của mỗi phần tử trong a
    weights = [x[-1] for x in boxes]

    screen.fill(background)
    x = 0
    y = 0
    for i, (row) in enumerate(matrix):
        for j, (char) in enumerate(row):
            if char == ' ': #floor
                screen.blit(floor,(x,y))
            elif char == '#': #wall
                screen.blit(wall,(x,y))
            elif char == '@': #worker on floor
                screen.blit(worker,(x,y))
            elif char == '.': #dock
                screen.blit(docker,(x,y))
            elif char == '*': #box on dock
                for k in range(0, len(positions)):
                    if i==positions[k][0] and j==positions[k][1]:
                        draw_weight_on_box(weights[k], x, y, box_docked)
            elif char == '$': #box
                for k in range(0, len(positions)):
                    if i==positions[k][0] and j==positions[k][1]:
                        draw_weight_on_box(weights[k], x, y, box)
            # elif char == '*': #box on dock
            #     screen.blit(box_docked, (x, y))
            # elif char == '$': #box
            #     screen.blit(box, (x, y))
            elif char == '+': #worker on dock
                screen.blit(worker_docked,(x,y))
            x = x + scale
        x = 0
        y = y + scale


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

def draw_mode_buttons(screen):
    font = pygame.font.Font(None, 24)
    button_texts = ['BFS', 'DFS', 'AStar', 'UCS']
    buttons = []
    
    for i, text in enumerate(button_texts):
        rect = pygame.Rect(50, 50 + i * 60, 100, 40)  # Đặt vị trí các nút
        pygame.draw.rect(screen, (200, 200, 200), rect)  # Màu nền nút
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Viền nút
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + 20, rect.y + 10))
        buttons.append((rect, text))
    
    pygame.display.update()
    return buttons

def get_mode_selection(screen):
    buttons = draw_mode_buttons(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button, mode in buttons:
                    if button.collidepoint(mouse_pos):
                        return mode  # Trả về chế độ đã chọn


def start_game():
    start = pygame.display.set_mode((320,240))
    level = int(ask(start,"Select Level"))
    if level > 0:
        mode = get_mode_selection(start)  # Nhận chế độ tìm kiếm từ nút
        return level, mode
    else:
        print("ERROR: Invalid Level: "+str(level))
        sys.exit(2)

wall = pygame.transform.scale(pygame.image.load('images/wall.png'), (64, 64))
floor = pygame.transform.scale(pygame.image.load('images/floor.png'), (64, 64))
box = pygame.transform.scale(pygame.image.load('images/box.png'), (64, 64))
box_docked = pygame.transform.scale(pygame.image.load('images/box_docked.png'), (64, 64))
worker = pygame.transform.scale(pygame.image.load('images/worker.png'), (64, 64))
worker_docked = pygame.transform.scale(pygame.image.load('images/worker_dock.png'), (64, 64))
docker = pygame.transform.scale(pygame.image.load('images/dock.png'), (64, 64))
background = 255, 226, 191
pygame.init()

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]# LRUD



while True:
    # Chọn lại level khi trò chơi hoàn tất
    
    level, mode = start_game()
    Game = game(level)
    size = Game.load_size()
    screen = pygame.display.set_mode(size)

    Game.start_state.print_matrix()
    s = Search(mode, Game.start_state, moves)#choose alg here
    print_game(Game.start_state.get_matrix(), screen, Game.start_state.box, game.scale)

    display_box(screen,"Computing...")
    pygame.display.update()
    weight, size , path, flag, node = s.search()
    print(weight,size,path,flag,node)
    

    move_list = path #load move from file. If file is empty, change this code to get move list
    index = 0 
    is_drawn = True  # Khởi tạo với True để bắt đầu di chuyển đầu tiên
        
    while True:

        # Chỉ thực hiện di chuyển nếu lần cập nhật màn hình trước đó đã hoàn tất
        if is_drawn and index < len(move_list):
            dx, dy = move_list[index]
            Game.start_state.get_child(dx, dy)  # Thực hiện di chuyển
            index += 1
            is_drawn = False  # Đặt lại flag, chờ việc vẽ hoàn tất

        # Cập nhật màn hình
        print_game(Game.start_state.get_matrix(), screen, Game.start_state.box, game.scale)
        pygame.display.update()
        is_drawn = True  # Đặt lại flag sau khi cập nhật xong màn hình

        # Kiểm tra xem game đã hoàn tất hay chưa
        if Game.start_state.is_completed():
            pygame.display.update()
            # display_end(screen=screen)
            # pygame.time.delay(1000)  # Đợi một lúc trước khi quay lại màn hình chọn
            break  # Quay lại vòng lặp bên ngoài để chọn level mới

        pygame.time.delay(100)