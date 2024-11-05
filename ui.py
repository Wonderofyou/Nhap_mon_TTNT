import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Load ảnh đá
rock_image = pygame.image.load('images/box.png')

# Đặt kích thước của cửa sổ dựa trên kích thước của ảnh đá
rock_width, rock_height = rock_image.get_size()
screen = pygame.display.set_mode((rock_width, rock_height))

# Hàm để hiển thị số lên hình ảnh
def draw_number_on_rock(number):
    screen.fill((255, 255, 255))  # Đặt màu nền trắng
    screen.blit(rock_image, (0, 0))  # Vẽ hình ảnh đá

    # Tạo phông chữ và render số
    font = pygame.font.SysFont(None, 18)  # Cỡ chữ nhỏ hơn cho phù hợp (18)
    text_surface = font.render(str(number), True, (0, 0, 0))  # Màu đen cho số

    # Tính toán vị trí để số nằm giữa hình tròn
    circle_x, circle_y = rock_width // 2, rock_height // 2
    text_rect = text_surface.get_rect(center=(circle_x, circle_y))

    # Vẽ hình tròn trắng làm nền cho số
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 12)
    pygame.draw.circle(screen, (0, 0, 0), (circle_x, circle_y), 12, 2)  # Viền đen xung quanh

    # Vẽ số lên hình tròn
    screen.blit(text_surface, text_rect)

# Vòng lặp chính
running = True
number = 99  # Số mặc định
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Nhập số từ bàn phím
            if event.unicode.isdigit():
                number = int(event.unicode)
    
    # Hiển thị số lên đá
    draw_number_on_rock(number)

    pygame.display.flip()

pygame.quit()
sys.exit()
