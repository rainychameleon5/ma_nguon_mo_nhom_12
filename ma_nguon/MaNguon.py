import pygame
import random
import time
# Khởi tạo Pygane
pygame.init()
# Kích thước cửa số game
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Thiết lập tên của số
pygame.display.set_caption("Bird Shooting Game")
# Màu sắc
white = (255, 255, 255)
black = (0,0,0)
# Tải hình ảnh chim và thay đổi kích thước
bird_img1=pygame.image.load("bird1.png")
bird_img1 = pygame.transform.scale(bird_img1,(75, 75)) # Kích thước châm
bird_img2 = pygame.image.load("bird2.png")
bird_img2 = pygame.transform.scale(bird_img2,  (75, 75))
# Kích thước chín
bird_x = screen_width
bird_y = random.randint( 0, screen_height - bird_img1.get_height())
bird_speed= 0.25 # Tốc độ bay của chín
bird_direction = -1 # Hướng di chuyến của chim (-1: trái, 1: phải)
# Tạo biển đến số điển
score = 0
font = pygame.font.Font(None,  36)
# Tạo thanh trượt
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img,  (100, 100)) # Kích thước cho player.png
player_x = screen_width // 2 # Vi trí ban đầu của thanh trượt theo trục x
player_y = screen_height - player_img.get_height() # Vị trí ban đầu của thanh trượt theo trục y
player_speed= 0.5 # Tốc độ di chuyển của thanh trượt
# Tạo danh sách đạn
bullets = []
reload_time = 1 # Thời gian nạp đạn 15 giây
last_shot_time = 0 # Thời gian của lần bần cuối cùng
# Vòng lập chính của game
running = True
while running:
  screen.fill(white) # Vẽ nên trắng cho cửa số game
  # Vẽ chim
  if bird_direction == -1:
    screen.blit(bird_img1, (bird_x, bird_y))
  else:
    screen.blit(bird_img2, (bird_x, bird_y))
  # Di chuyển chin
  bird_x += bird_speed * bird_direction # Chín đã chuyển theo hướng và tốc độ đã định
  if bird_x < 0: # Nếu chim ra khỏi màn hình bên trái
    bird_direction=1 # Đối hướng di chuyển sang phải
    bird_x =0
    bird_y=random.randint( 0, screen_height - bird_img1.get_height())
  elif bird_x > screen_width - bird_img1.get_width(): # Nếu chia ra khỏi màn hình bên phải
    bird_direction = -1 #061 hướng di chuyển sang trái
    bird_x = screen_width - bird_img1.get_width()
    bird_y = random.randint(0, screen_height - bird_img1.get_height())
  # Hiển thị điểm
  score_text = font.render("Score: " + str(score),True, black)
  screen.blit(score_text, (10, 10))
  #Vẽ thanh trượt
  screen.blit(player_img,(player_x, player_y))
  # Xử lý sự kiện
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False  # Kết thúc game
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and time.time() - last_shot_time > reload_time:
        # Nếu nhấn phím Space và đã qua thời gian nạp đạn
        bullet_x = player_x + player_img.get_width() // 2
        bullet_y = player_y
        bullets.append([bullet_x, bullet_y])  # Thên đạn vào danh sách đạn
        last_shot_time = time.time()  # Cập nhật thời gian bốn lần cuối
  # Di chuyển thanh trượt
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and player_x > 0:
    player_x -= player_speed  # Di chuyến thanh trượt sang trái
  if keys[pygame.K_RIGHT] and player_x < screen_width - player_img.get_width():
    player_x += player_speed  # 01 chuyến thanh trượt sang phải
  # Di chuyển đạn
  for bullet in bullets:
    bullet[1] -= 1  # Tốc độ di chuyển của đạn
    pygame.draw.rect(screen, black, pygame.Rect(bullet[0], bullet[1], 5, 10))  # Vẽ đạn
  # Kiểm tra va chạm giữa đạn và chín
  for bullet in bullets:
    if bird_x <= bullet[0] <= bird_x + bird_img1.get_width() and bird_y <= bullet[1] <= bird_y + bird_img1.get_height():
      bullets.remove(bullet)  # Xóa đạn khi va chạn
      score += 1  # Cộng điền
      # Thiết lập lại vị trí chin sau khi trúng đạn
      bird_x = screen_width if bird_direction == -1 else 0
      bird_y=random.randint(0, screen_height - bird_img1.get_height())

  pygame.display.flip()  # Cập nhật màn hình
pygame.quit()
