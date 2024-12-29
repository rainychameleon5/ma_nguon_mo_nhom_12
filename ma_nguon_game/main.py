import pygame
import random
import time

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()
start_sound = pygame.mixer.Sound("start.mp3")
shoot_sound = pygame.mixer.Sound("shoot.mp3")
gift_sound = pygame.mixer.Sound("gift.mp3")
egg_hit_sound = pygame.mixer.Sound("egg_hit.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")
background_music = "background_music.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)

# Kích thước cửa sổ game
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Thiết lập tên cửa sổ
pygame.display.set_caption("Bird Shooting Game")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Tải hình ảnh chim và thay đổi kích thước
bird_img1 = pygame.image.load("bird1.png")
bird_img1 = pygame.transform.scale(bird_img1, (75, 75))  # Kích thước chim
bird_img2 = pygame.image.load("bird2.png")
bird_img2 = pygame.transform.scale(bird_img2, (75, 75))  # Kích thước chim
# Load hình ảnh chim đặc biệt và hộp vật phẩm

bird_egg_img = pygame.image.load("bird_egg.png")  # Thêm ảnh chim mang trứng
bird_egg_img = pygame.transform.scale(bird_egg_img, (75, 75))  # Điều chỉnh kích thước

special_bird_img = pygame.image.load("special_bird.png")
special_bird_img = pygame.transform.scale(special_bird_img, (75, 75))

fast_bird_img = pygame.image.load("fast_bird.png")  # Thêm ảnh chim nhanh
fast_bird_img = pygame.transform.scale(fast_bird_img, (75, 75))  # Điều chỉnh kích thước

item_box_img = pygame.image.load("item_box.png")
item_box_img = pygame.transform.scale(item_box_img, (40, 40))
# Tải và điều chỉnh kích thước hình ảnh trứng
egg_img = pygame.image.load("egg.png")
egg_img = pygame.transform.scale(egg_img, (20, 25))  # Điều chỉnh kích thước phù hợp
# Tải và điều chỉnh kích thước background
background_img = pygame.image.load("background2.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

menu_screen_img = pygame.image.load("game_start.png")
menu_screen_img = pygame.transform.scale(menu_screen_img, (screen_width, screen_height))

game_over_screen_img = pygame.image.load("game_over.png")
game_over_screen_img = pygame.transform.scale(game_over_screen_img, (screen_width, screen_height))

instruction_screen_img = pygame.image.load("guide.png")
instruction_screen_img = pygame.transform.scale(instruction_screen_img, (screen_width, screen_height))

# Tải và điều chỉnh kích thước hình ảnh thanh trượt
bird_x = screen_width
bird_y = random.randint(0, screen_height - bird_img1.get_height())

bird_direction = -1  # Hướng di chuyển của chim (-1: trái, 1: phải)

# Tạo biến đếm số điểm
score = 0
font = pygame.font.Font(None, 36)

# Tạo thanh trượt
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))  # Tăng kích thước cho player.png
player_x = screen_width // 2  # Vị trí ban đầu của thanh trượt theo trục x
player_y = screen_height - player_img.get_height()  # Vị trí ban đầu của thanh trượt theo trục y
player_speed = 0.5  # Tốc độ di chuyển của thanh trượt

# Tạo danh sách đạn
bullets = []
reload_time = 1  # Thời gian nạp đạn 1 giây
last_shot_time = 0  # Thời gian của lần bắn cuối cùng

# Tạo danh sách chim
birds = []
min_birds = 1  # Số lượng chim tối thiểu
max_birds = 10  # Số lượng chim tối đa
spawn_timer = 0  # Bộ đếm thời gian để tạo chim mới
spawn_delay = 2  # Thời gian chờ giữa các lần tạo chim mới (giây)

#Tỉ lệ tạo chim mới
fast_bird_chance = 0.05
special_bird_chance = 0.15
egg_layer_chance = 0.3

# Thêm các biến mới
power_ups = []  # Danh sách các vật phẩm đang rơi
active_power_ups = {}  # Lưu trữ power-up đang hoạt động
# Các loại power-up
power_up_types = ['double_shot', 'fast_reload', 'speed_up', 'speed_down', 'slow_reload', 'extra_life']


# Thêm biến cho trứng và mạng sống
eggs = []  # Danh sách trứng
lives = 3  # Số mạng ban đầu
egg_speed = 0.3  # Tốc độ rơi của trứng

# thời gian
current_time = time.time()
# Thêm biến cho điểm cao nhất
high_score = 0


# Thêm hàm vẽ text
def draw_text(text, size, x, y, color=white):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)



# Màn hình chờ
def show_start_screen():
    # vẽ màn hình start lên màn hình
    screen.blit(menu_screen_img, (0, 0))
    pygame.display.flip()
    # phát âm thanh start
    pygame.mixer.Sound.play(start_sound, -1)  # Thêm -1 để phát liên tục

    waiting = True
    while waiting:
        # lấy các sự kiện từ pygame
        for event in pygame.event.get():
            # nếu sự kiện là quit thì trả về False
            if event.type == pygame.QUIT:
                return False
            # nếu sự kiện là nhấn phím thì kiểm tra phím nào được nhấn
            if event.type == pygame.KEYDOWN:
                # nếu phím space được nhấn thì dừng âm thanh start và trả về True
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.stop(start_sound)
                    return True
                # nếu phím h được nhấn thì hiển thị hướng dẫn và trả về False
                if event.key == pygame.K_h:
                    if not show_instructions():
                        return False
                    # Vẽ lại màn hình start sau khi xem hướng dẫn
                    screen.blit(menu_screen_img, (0, 0))
                    pygame.display.flip()
                # nếu phím escape được nhấn thì trả về False
                if event.key == pygame.K_ESCAPE:
                    return False
    # nếu không có sự kiện nào được nhấn thì trả về True
    return True


# Màn hình game over
def show_game_over_screen():
    global high_score, running
    # nếu điểm số cao hơn điểm cao nhất thì cập nhật điểm cao nhất và phát âm thanh game over
    if score > high_score:
        high_score = score
        pygame.mixer.Sound.play(game_over_sound)

    # vẽ màn hình game over lên màn hình
    screen.blit(game_over_screen_img, (0, 0))
    # Vẽ điểm số và điểm cao nhất
    draw_text(f"Score: {score}", 48, screen_width // 2, screen_height // 2 - 50)
    draw_text(f"High Score: {high_score}", 48, screen_width // 2, screen_height // 2 + 20)
    pygame.display.flip()

    # chờ người dùng nhấn phím để quay lại màn hình start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            # nếu sự kiện là quit thì trả về "quit"
            if event.type == pygame.QUIT:
                return "quit"
            # nếu sự kiện là nhấn phím thì kiểm tra phím nào được nhấn
            if event.type == pygame.KEYDOWN:
                # nếu phím space được nhấn thì kiểm tra xem game đang chạy hay không
                if event.key == pygame.K_SPACE:
                    if not running:  # Nếu từ pause screen
                        return "play_again"
                    return "main_menu"
                # nếu phím enter được nhấn thì trả về "main_menu"
                if event.key == pygame.K_RETURN:
                    return "main_menu"
                # nếu phím escape được nhấn thì trả về "quit"
                if event.key == pygame.K_ESCAPE:
                    return "quit"
    return "quit"   # nếu không có sự kiện nào được nhấn thì trả về "quit"


# Hàm reset game
def reset_game():
    # reset game
    global score, lives, birds, bullets, eggs, power_ups, active_power_ups
    score = 0
    lives = 3
    birds = []
    bullets = []
    eggs = []
    power_ups = []
    active_power_ups = {}
    # tạo chim ban đầu
    for _ in range(min_birds):
        birds.append(create_bird(is_egg_layer=False))


# Hàm tạo chim
def create_bird(is_egg_layer=False, is_special=False, is_fast=False):
    # tạo chim ban đầu
    min_y = 200
    max_y = player_y - 250
    bird_speed = 0.25  # Tốc độ bay của chim
    if is_fast:
        bird_speed = 0.75
    return {
        # vị trí chim
        'x': screen_width,
        'y': player_y - random.randint(min_y, max_y),
        # tốc độ chim
        'speed': bird_speed,
        # hướng chim
        'direction': -1,
        # loại chim
        'is_egg_layer': is_egg_layer,
        'is_special': is_special,
        'is_fast': is_fast,
        # thời gian thả trứng
        'last_egg_time': current_time
    }


# Khởi tạo chim ban đầu
for _ in range(min_birds):
    birds.append(create_bird(is_egg_layer=False))


# Thêm hàm xử lý power-up
def apply_power_up():
    power_type = random.choice(power_up_types)
    current_time = time.time()

    # Xử lý các cặp hiệu ứng đối lập
    if power_type == 'fast_reload':
        if 'slow_reload' in active_power_ups:
            # Nếu đang có slow reload, xóa nó và không thêm fast reload
            del active_power_ups['slow_reload']
        else:
            # Nếu không có slow reload, thêm fast reload
            active_power_ups['fast_reload'] = current_time + 10
    elif power_type == 'slow_reload':
        if 'fast_reload' in active_power_ups:
            # Nếu đang có fast reload, xóa nó và không thêm slow reload
            del active_power_ups['fast_reload']
        else:
            # Nếu không có fast reload, thêm slow reload
            active_power_ups['slow_reload'] = current_time + 10
    elif power_type == 'speed_up':
        if 'speed_down' in active_power_ups:
            # Nếu đang có speed down, xóa nó và không thêm speed up
            del active_power_ups['speed_down']
        else:
            # Nếu không có speed down, thêm speed up
            active_power_ups['speed_up'] = current_time + 10
    elif power_type == 'speed_down':
        if 'speed_up' in active_power_ups:
            # Nếu đang có speed up, xóa nó và không thêm speed down
            del active_power_ups['speed_up']
        else:
            # Nếu không có speed up, thêm speed down
            active_power_ups['speed_down'] = current_time + 10
    #power up, nhân đôi dạn
    elif power_type == 'double_shot':
        active_power_ups['double_shot'] = current_time + 10
    #power up, thêm 1 mạng, tối đa là 3
    elif power_type == 'extra_life':
        global lives
        if lives < 3:
            lives += 1


# Hàm pause screen
def show_pause_screen():
    # Làm tối màn hình hiện tại
    dark_surface = pygame.Surface((screen_width, screen_height))
    dark_surface.set_alpha(128)
    dark_surface.fill((0, 0, 0))
    screen.blit(dark_surface, (0, 0))

    # Hiển thị text pause
    draw_text("GAME PAUSED", 64, screen_width // 2, screen_height // 2 - 50)
    draw_text("Press SPACE to continue", 32, screen_width // 2, screen_height // 2 + 20)
    draw_text("Press ENTER to restart", 32, screen_width // 2, screen_height // 2 + 60)
    draw_text("Press ESC to quit", 32, screen_width // 2, screen_height // 2 + 100)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "continue"
                if event.key == pygame.K_RETURN:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "quit"
    return "continue"


# Thêm hàm hiển thị hướng dẫn
def show_instructions():
    # Sử dụng background thay vì surface tối
    screen.blit(instruction_screen_img, (0, 0))  # Sử dụng background riêng cho hướng dẫn

    # Hiển thị hướng dẫn bằng tiếng Anh
    instructions = [
        "HOW TO PLAY",
        "",
        "Movement: LEFT/RIGHT Arrow Keys",
        "Shoot: SPACE       Pause: ESC",
        "BIRD TYPES:",
        "- Normal Bird: +1 point    - Special Bird: Drops power-ups",
        "- Fast Bird: +15 points    - Egg Layer Bird: Avoid falling eggs",
        "POWER-UPS:",
        "- Double Shot: Shoot 2 bullets - Extra Life: +1 life",
        "- Fast/Slow Reload: Increase/Decrease reload speed",
        "- Speed Up/Down: Increase/Decrease movement speed",
        "Press SPACE to return"
    ]

    y_pos = 50
    for line in instructions:
        if line == "HOW TO PLAY":
            draw_text(line, 48, screen_width // 2, y_pos, black)
            y_pos += 50
        else:
            draw_text(line, 32, screen_width // 2, y_pos, black)
            y_pos += 35

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
    return True


game_active = True
while game_active:
    if not show_start_screen():
        break
    playing = True
    pygame.mixer.music.play(-1)

    while playing:
        reset_game()
        running = True
        while running:
            current_time = time.time()
            # Vẽ background
            screen.blit(background_img, (0, 0))
            # Logic tạo chim mới
            if current_time - spawn_timer > spawn_delay:
                spawn_timer = current_time
                if len(birds) < max_birds and random.random() < 0.5:
                    is_fast = random.random() < fast_bird_chance
                    is_special = not is_fast and random.random() < special_bird_chance
                    is_egg_layer = not is_fast and not is_special and random.random() < egg_layer_chance

                    birds.append(create_bird(is_egg_layer=is_egg_layer, is_special=is_special, is_fast=is_fast))

            # Xử lý power-ups đang rơi
            for power_up in power_ups[:]:
                power_up['y'] += 0.3  # Tốc độ rơi của hộp
                screen.blit(item_box_img, (power_up['x'], power_up['y']))

                # Tạo hình chữ nhật va chạm cho power-up và player
                power_up_rect = pygame.Rect(
                    power_up['x'],
                    power_up['y'],
                    item_box_img.get_width(),
                    item_box_img.get_height()
                )
                player_rect = pygame.Rect(
                    player_x,
                    player_y,
                    player_img.get_width(),
                    player_img.get_height()
                )

                # Kiểm tra va chạm bằng hình chữ nhật
                if power_up_rect.colliderect(player_rect):
                    power_ups.remove(power_up)
                    pygame.mixer.Sound.play(gift_sound)  # Phát âm thanh khi nhận hộp quà

                    apply_power_up()
                    continue  # Thoát vòng lặp sau khi xử lý va chạm

                # Xóa power-up khi chạm đất
                if power_up['y'] > screen_height:
                    power_ups.remove(power_up)

            # Xử lý chim và vẽ chim
            for bird in birds:
                if bird['is_egg_layer']:
                    # Thêm debug print để kiểm tra
                    print(f"Time diff: {current_time - bird['last_egg_time']}")

                    if current_time - bird['last_egg_time'] >= 1.5:  # Thay đổi thành 1.5
                        # Chỉ thả trứng khi chim nằm trong màn hình
                        if 0 <= bird['x'] <= screen_width:
                            eggs.append({
                                'x': bird['x'] + bird_img1.get_width() / 2 - egg_img.get_width() / 2,
                                'y': bird['y'] + bird_img1.get_height()
                            })
                            bird['last_egg_time'] = current_time

                # Di chuyển chim
                bird['x'] += bird['speed'] * bird['direction']

                # Vẽ chim thường hoặc chim đặc biệt
                # Vẽ chim với các loại khác nhau
                if bird['is_fast']:
                    if bird['direction'] == -1:
                        screen.blit(fast_bird_img, (bird['x'], bird['y']))
                    else:
                        flipped_fast_bird = pygame.transform.flip(fast_bird_img, True, False)
                        screen.blit(flipped_fast_bird, (bird['x'], bird['y']))
                elif bird['is_special']:
                    if bird['direction'] == -1:
                        screen.blit(special_bird_img, (bird['x'], bird['y']))
                    else:
                        flipped_special_bird = pygame.transform.flip(special_bird_img, True, False)
                        screen.blit(flipped_special_bird, (bird['x'], bird['y']))
                elif bird['is_egg_layer']:
                    if bird['direction'] == -1:
                        screen.blit(bird_egg_img, (bird['x'], bird['y']))
                    else:
                        flipped_egg_bird = pygame.transform.flip(bird_egg_img, True, False)
                        screen.blit(flipped_egg_bird, (bird['x'], bird['y']))
                else:
                    if bird['direction'] == -1:
                        screen.blit(bird_img1, (bird['x'], bird['y']))
                    else:
                        screen.blit(bird_img2, (bird['x'], bird['y']))
                # Xử lý khi chim ra khỏi màn hình
                if bird['x'] < 0:
                    bird['direction'] = 1
                    bird['x'] = 0
                    bird['y'] = player_y - random.randint(200, player_y - 50)  # Tính từ player lên trên
                    bird['last_egg_time'] = current_time  # Reset thời gian thả trứng
                elif bird['x'] > screen_width - bird_img1.get_width():
                    bird['direction'] = -1
                    bird['x'] = screen_width - bird_img1.get_width()
                    bird['y'] = player_y - random.randint(200, player_y - 50)  # Tính từ player lên trên
                    bird['last_egg_time'] = current_time  # Reset thời gian thả trứng
            # Vẽ và cập nhật trứng
            for egg in eggs[:]:
                egg['y'] += egg_speed
                # Thay thế pygame.draw.ellipse bằng screen.blit
                screen.blit(egg_img, (egg['x'], egg['y']))
                # Tạo hình chữ nhật va chạm cho trứng và người chơi
                # Tạo hình chữ nhật va chạm đơn giản
                egg_rect = pygame.Rect(
                    egg['x'],
                    egg['y'],
                    egg_img.get_width(),
                    egg_img.get_height()
                )

                player_rect = pygame.Rect(
                    player_x,
                    player_y,
                    player_img.get_width(),
                    player_img.get_height()
                )
                # Kiểm tra va chạm bằng hình chữ nhật
                if egg_rect.colliderect(player_rect):
                    eggs.remove(egg)
                    lives -= 1
                    pygame.mixer.Sound.play(egg_hit_sound)

                    if lives <= 0:
                        running = False  # Game over

                # Xóa trứng khi chạm đất
                elif egg['y'] > screen_height:
                    eggs.remove(egg)

            # Khi thả trứng mới, giữ nguyên logic nhưng điều chỉnh vị trí để phù hợp với kích thước hình ảnh
            if bird['is_egg_layer']:
                if current_time - bird['last_egg_time'] > 1.5:  # Thay đổi thành 1.5
                    eggs.append({
                        'x': bird['x'] + bird_img1.get_width() / 2 - egg_img.get_width() / 2,
                        'y': bird['y'] + bird_img1.get_height()
                    })
                    bird['last_egg_time'] = current_time

                # Di chuyển chim
                bird['x'] += bird['speed'] * bird['direction']

                # Xử lý khi chim ra khỏi màn hình
                if bird['x'] < 0:
                    bird['direction'] = 1
                    bird['x'] = 0
                    bird['y'] = random.randint(50, player_y - 250)

                elif bird['x'] > screen_width - bird_egg_img.get_width():
                    bird['direction'] = -1
                    bird['x'] = screen_width - bird_egg_img.get_width()
                    bird['y'] = random.randint(50, player_y - 250)

            # Hiển thị số mạng còn lại
            lives_text = font.render(f"Lives: {lives}", True, white)
            screen.blit(lives_text, (screen_width - 100, 10))

            # Hiển thị điểm
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            # Vẽ thanh trượt
            screen.blit(player_img, (player_x, player_y))

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        pause_action = show_pause_screen()
                        if pause_action == "quit":
                            running = False
                        elif pause_action == "restart":
                            reset_game()
                            pygame.mixer.music.unpause()
                            lives = 3
                            score = 0
                        elif pause_action == "continue":
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_SPACE:
                        current_reload_time = reload_time
                        if 'fast_reload' in active_power_ups:
                            current_reload_time = 0.5
                        elif 'slow_reload' in active_power_ups:
                            current_reload_time = 2
                        if time.time() - last_shot_time > current_reload_time:
                            # Bắn đạn
                            bullet_x = player_x + player_img.get_width() // 2
                            bullet_y = player_y
                            bullets.append([bullet_x, bullet_y])
                            pygame.mixer.Sound.play(shoot_sound)

                            if 'double_shot' in active_power_ups:
                                # Bắn thêm viên đạn thứ hai
                                bullets.append([bullet_x - 10, bullet_y])
                            last_shot_time = time.time()
            # Di chuyển thanh trượt
            current_player_speed = player_speed
            if 'speed_up' in active_power_ups:
                current_player_speed = 0.75
            elif 'speed_down' in active_power_ups:
                current_player_speed = 0.25

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= current_player_speed
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_img.get_width():
                player_x += current_player_speed  # Di chuyển thanh trượt sang phải

            # Di chuyển đạn
            for bullet in bullets:
                bullet[1] -= 1  # Tốc độ di chuyển của đạn
                pygame.draw.rect(screen, black, pygame.Rect(bullet[0], bullet[1], 5, 10))  # Vẽ đạn

            # Kiểm tra va chạm đạn với chim
            for bullet in bullets[:]:
                for bird in birds:
                    if (bird['x'] <= bullet[0] <= bird['x'] + bird_img1.get_width() and
                            bird['y'] <= bullet[1] <= bird['y'] + bird_img1.get_height()):
                        if bullet in bullets:
                            bullets.remove(bullet)

                        if bird['is_fast']:
                            score += 15  # Chim nhanh cho 15 điểm
                        # Nếu là chim đặc biệt, thả hộp vật phẩm
                        elif bird['is_special']:
                            power_ups.append({
                                'x': bird['x'],
                                'y': bird['y']
                            })
                            pygame.mixer.Sound.play(gift_sound)

                        else:
                            score += 1

                            # Đặt lại vị trí chim
                        bird['x'] = screen_width if bird['direction'] == -1 else 0
                        bird['y'] = random.randint(50, player_y - 250)
                        break

            # Cập nhật thời gian power-up
            for power_up_type in list(active_power_ups.keys()):
                if current_time > active_power_ups[power_up_type]:
                    del active_power_ups[power_up_type]

            # Hiển thị power-up đang hoạt động
            power_up_y = 40
            for power_up_type in active_power_ups:
                time_left = int(active_power_ups[power_up_type] - current_time)
                text = ""
                if power_up_type == 'double_shot':
                    text = f"Double Shot: {time_left}s"
                elif power_up_type == 'fast_reload':
                    text = f"Fast Reload: {time_left}s"
                elif power_up_type == 'speed_up':
                    text = f"Speed Up: {time_left}s"
                elif power_up_type == 'speed_down':
                    text = f"Speed Down: {time_left}s"
                elif power_up_type == 'slow_reload':
                    text = f"Slow Reload: {time_left}s"

                if text:  # Chỉ hiển thị nếu có text
                    power_up_text = font.render(text, True, white)
                    screen.blit(power_up_text, (10, power_up_y))

                    power_up_y += 30

            pygame.display.flip()  # Cập nhật màn hình
        # Xử lý màn hình game over
        if game_active:
            game_over_action = show_game_over_screen()
            if game_over_action == "quit":
                playing = False
                game_active = False
            elif game_over_action == "main_menu":
                playing = False
            elif game_over_action == "play_again":
                continue  # Bắt đầu ván mới
    if not show_game_over_screen():
        break

# Kết thúc game
pygame.mixer.music.stop()

pygame.quit()