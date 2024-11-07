#!../bin/python
import threading
import sys
import pygame
import os
from events import *
from widgets import sidebar_widgets
from statespace import StateSpace
from search import Search
from game import game
import time
import queue

import pygame_widgets



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
def draw_pause_btn(screen, on_pause):
    button_x, button_y, button_width, button_height = 1000, 350, 180, 40
    radius = 5
    border_thickness = 2
    font = pygame.font.SysFont('Verdana', 14, bold=True)
    button_text = font.render("Pause/Continue", True, (0, 0, 0))
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    
    if on_pause:
      color =  (200, 200, 200)
    else:
      color = (150, 150, 150)

    pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=radius)

    inner_rect = button_rect.inflate(-border_thickness*2, -border_thickness*2)
    pygame.draw.rect(screen, color, inner_rect, border_radius=radius)

    screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2,
                              button_y + (button_height - button_text.get_height()) // 2))
    return button_x, button_y, button_width, button_height
   
def print_game(matrix,screen, step, total_weight=None, on_pause=None, boxes=None):
    positions = [x[:2] for x in boxes]  # Lấy 2 phần tử đầu của mỗi phần tử trong a
    weights = [x[-1] for x in boxes]
    screen.fill(background)
    x = 0
    y = 0
    if total_weight is not None:
      font = pygame.font.Font(None, 36)
      steps_text = font.render(f"Steps: {step}", True, (0, 0, 0))
      weight_text = font.render(f"Weight: {total_weight}", True, (0, 0, 0))
      screen.blit(steps_text, (1000, 150))
      screen.blit(weight_text, (1000, 200))
    if on_pause is not None:
       draw_pause_btn(screen, on_pause)
    

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
    elif event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
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

def start_game(start):
    #start = pygame.display.set_mode((320,240))
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
moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
running = True
result_queue = queue.Queue()
searching = False
search_thread = None
complete_search = False

def handle_algorithm_selection(event):
    if event.type == SOLVE_ASTAR_EVENT:
        return 'A*'
    elif event.type == SOLVE_BFS_EVENT:
        return 'BFS'
    elif event.type == SOLVE_DFS_EVENT:
        return 'DFS'
    elif event.type == SOLVE_UCS_EVENT:
        return 'UCS'
    return None
  
  
def choose_algo(screen, btns):
    w = 1055
    h1 = 100
    x0 = 130
    y0 = 40
    waiting_option = True
    options = ['A*', 'BFS', 'DFS', 'UCS']
    while waiting_option:
        events = pygame.event.get()       
        pygame_widgets.update(events)
        for event in events:
          if event.type == pygame.QUIT:
            running = False
            waiting_option = False
            pygame.quit()
            sys.exit()
            
          algorithm = handle_algorithm_selection(event)
          if algorithm:
            return algorithm
          
        print_game(_game.start_state.get_matrix(), screen, step=0, boxes=_game.start_state.box)
        for btn in btns:          
          btn.draw()
        pygame.display.flip()
  
  
  
def rerender_running(screen, message_box, btns):
  while not stop_event.is_set():
    print_game(_game.start_state.get_matrix(), screen, step=0, boxes=_game.start_state.box)
    for btn in btns:
       btn.draw()
    display_box(screen, message_box)




os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"



def run_search(search_instance):
  
  global complete_search
  try:
      # Chạy thuật toán search trong thread riêng
      weight, size, path, flag, node = search_instance.search()
      # Sử dụng queue để gửi kết quả về main thread
      result_queue.put((weight, size, path, flag, node))
      complete_search = True
  except Exception as e:
      result_queue.put(e)



while True:
  
  searching = False
  complete_search = False
  result_queue = queue.Queue()  # Tạo queue mới
  running = True  # Reset running state
  
  
  # Chọn lại level khi trò chơi hoàn tất
  screen = pygame.display.set_mode((1216, 640))
  btns = sidebar_widgets(screen)
  level = start_game(screen)
  _game = game(level)

  size = _game.load_size()
  screen = pygame.display.set_mode(size)
  stop_event = threading.Event()
  option = choose_algo(screen=screen, btns=btns)
  print("Algorithm:", option)
  s = Search(option, _game.start_state, moves)
  
  weight = 0
  size = 0
  path = []
  flag = []
  node = 0
  index = 0
  start_time = time.time()
  while running:
    # 1. Xử lý tất cả events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        # elif event.type in [SOLVE_BFS_EVENT, SOLVE_DFS_EVENT, SOLVE_UCS_EVENT, SOLVE_ASTAR_EVENT]:
        #     if not searching:
        #         searching = True
        #         # Khởi động search thread
        #         search_thread = threading.Thread(target=run_search, args=(event.type,))
        #         search_thread.start()
    if not searching:
      searching = True
      search_thread = threading.Thread(target=run_search, args=(s,))
      search_thread.start()
    if complete_search:
      try:
        result = result_queue.get_nowait()  # Dùng get_nowait() thay vì get()
        if isinstance(result, Exception):
          print("Search failed:", result)
          running = False
        else:
          weight, size, path, flag, node = result
          running = False
      except queue.Empty:
        pass  # Nếu chưa có kết quả, tiếp tục loop
      
    # 2. Render game state
    
    print_game(_game.start_state.get_matrix(), screen, step=0, boxes=_game.start_state.box)
    for btn in btns:
        btn.draw()
        
    if searching:
      display_box(screen, "Computing...")
        
    # 3. Update display
    pygame.display.flip()
    
    pygame.time.delay(30) 
         

  # # Đa luồng để khi nó chạy cái search thì màn hình luôn được render lại
  # thread_render = threading.Thread(target=rerender_running, args=(screen, "Computing...", btns,  ))
  # thread_render.start()
  # weight, size , path, flag, node = s.search()
  # stop_event.set()
  # thread_render.join()
    
  print_game(_game.start_state.get_matrix(), screen, step=0, boxes=_game.start_state.box)
    
  pygame.display.update()

  move_list = path #load move from file. If file is empty, change this code to get move list
  index = 0 
  is_drawn = True  # Khởi tạo với True để bắt đầu di chuyển đầu tiên
  total_weight = 0
  on_pause = False
  end_time = time.time()
  print("Search time:", end_time-start_time)
  while True:
      for event in pygame.event.get():
          if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(1000, 350, 180, 40).collidepoint(event.pos):
              
              on_pause = not on_pause
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
      if on_pause:
        
        print_game(_game.start_state.get_matrix(), screen, index, total_weight, on_pause, boxes=_game.start_state.box)
        continue
      total_weight += flag[index]
        
      # Chỉ thực hiện di chuyển nếu lần cập nhật màn hình trước đó đã hoàn tất
      if is_drawn and index < len(move_list):
          dx, dy = move_list[index]
          _game.start_state.get_child(dx, dy)  # Thực hiện di chuyển
          index += 1
          is_drawn = False  # Đặt lại flag, chờ việc vẽ hoàn tất

      # Cập nhật màn hình
      print_game(_game.start_state.get_matrix(), screen, index, total_weight, on_pause, _game.start_state.box)
      pygame.display.flip()
      pygame.event.post(pygame.event.Event(RENDER_COMPLETE))
      waiting = True
        
      #Đảm bảo vẽ xong mới cập nhật flag
      while waiting:
          for event in pygame.event.get():
              if event.type == RENDER_COMPLETE:
                is_drawn = True # Đặt lại flag sau khi cập nhật xong màn hình
                waiting = False
                    
      # Kiểm tra xem game đã hoàn tất hay chưa
      if _game.start_state.is_completed():
          print("Steps:", index)
          print("Weight:", total_weight)
          pygame.display.update()
          display_end(screen=screen)
          pygame.time.delay(5000)  # Đợi một lúc trước khi quay lại màn hình chọn
          break  # Quay lại vòng lặp bên ngoài để chọn level mới

      pygame.time.delay(50)
