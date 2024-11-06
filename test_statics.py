import pygame

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Steps & Power Display")

# Thiết lập phông chữ
font = pygame.font.Font(None, 36)

# Các biến để lưu số bước và năng lượng
steps = 0
power = 100

# Hàm hiển thị thông tin lên màn hình
def display_info():
    # Tạo văn bản cho số bước và năng lượng
    steps_text = font.render(f"Steps: {steps}", True, (255, 255, 255))
    power_text = font.render(f"Power: {power}", True, (255, 255, 255))
    
    # Hiển thị văn bản lên màn hình
    screen.blit(steps_text, (10, 10))
    screen.blit(power_text, (10, 50))

# Vòng lặp game
running = True
while running:
    screen.fill((0, 0, 0))  # Xóa màn hình
    
    # Kiểm tra các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Cập nhật và hiển thị thông tin số bước và năng lượng
    display_info()
    
    # Cập nhật màn hình
    pygame.display.flip()

pygame.quit()
