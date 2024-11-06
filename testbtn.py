import pygame
from pygame_widgets.button import Button
import sys

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
screen = pygame.display.set_mode((1216, 640))
pygame.display.set_caption("Multiple Buttons Example")

# Định nghĩa màu sắc
WHITE = (255, 255, 255)

# Tạo các button
buttons = [
    Button(screen, 100, 100, 200, 50, text='Button 1', fontSize=30, onClick=lambda: print("Button 1 clicked!")),
    Button(screen, 100, 200, 200, 50, text='Button 2', fontSize=30, onClick=lambda: print("Button 2 clicked!")),
    Button(screen, 100, 300, 200, 50, text='Button 3', fontSize=30, onClick=lambda: print("Button 3 clicked!"))
]

running = True
while running:
    # Lấy tất cả các sự kiện
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Vẽ nền trắng
    screen.fill(WHITE)

    # Lắng nghe và vẽ từng button
    for button in buttons:
        button.listen(events)  # Truyền danh sách sự kiện vào listen()
        button.draw()

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
