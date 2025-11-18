import pygame
import sys
import random

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 遊戲設定 - 網格系統
GRID_SIZE = 40  # 每個格子的像素大小
GRID_HEIGHT = 15  # 關卡高度 (15格)
SCREEN_GRID_WIDTH = 30  # 螢幕顯示寬度 (30格)
SCREEN_WIDTH = SCREEN_GRID_WIDTH * GRID_SIZE  # 1200像素
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE  # 600像素
FPS = 60

# 馬力歐圖片陣列
MARIO = [
    pygame.image.load("PNG\\Mario_Big_Idle.png"), # MARIO[0]，大馬力歐面相右邊的靜止圖
    pygame.image.load("PNG\\Mario_Big_Jump.png"), # MARIO[1]，大馬力歐面相右邊的跳躍圖
    pygame.image.load("PNG\\Mario_Big_Run1.png"), # MARIO[2]，大馬力歐面相右邊的跑步第一張圖
    pygame.image.load("PNG\\Mario_Big_Run2.png"), # MARIO[3]，大馬力歐面相右邊的跑步第二張圖
    pygame.image.load("PNG\\Mario_Big_Run3.png"), # MARIO[4]，大馬力歐面相右邊的跑步第三張圖
    pygame.image.load("PNG\\Mario_Big_Slide.png"), # MARIO[5]，大馬力歐面相右邊的滑行圖
    pygame.image.load("PNG\\Mario_Small_Death.png"), # MARIO[6]，小馬力歐的死亡圖
    pygame.image.load("PNG\\Mario_Small_Idle.png"), # MARIO[7]，小馬力歐面相右邊的靜止圖，也是遊戲初始畫面時使用的圖片
    pygame.image.load("PNG\\Mario_Small_Jump.png"), # MARIO[8]，小馬力歐面相右邊的跳躍圖
    pygame.image.load("PNG\\Mario_Small_Run1.png"), # MARIO[9]，小馬力歐面相右邊的跑步第一張圖
    pygame.image.load("PNG\\Mario_Small_Run2.png"), # MARIO[10]，小馬力歐面相右邊的跑步第二張圖
    pygame.image.load("PNG\\Mario_Small_Run3.png"), # MARIO[11]，小馬力歐面相右邊的跑步第三張圖
    pygame.image.load("PNG\\Mario_Small_Slide.png"), # MARIO[12]，小馬力歐面相右邊的滑行圖
]

# 烏龜圖片陣列
KOOPA = [
    pygame.image.load("PNG\\Koopa_Walk1.png"), # KOOPA[0]，烏龜走路的第一張圖
    pygame.image.load("PNG\\Koopa_Walk2.png"), # KOOPA[1]，烏龜走路的第二張圖
]

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (107, 140, 255)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)

# 建立視窗
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Bros - World 1-1")
clock = pygame.time.Clock()

# 全局變量
points = 0
coins_collected = 0
game_time = 400  # 遊戲時間 (秒)
time_counter = 0  # 幀計數器
game_won = False
game_paused = False  # 遊戲暫停狀態

# 關卡地圖
level_map = [
    "                                                                                                                                                                                                                   ",
    "                                                                                                                                                                                                                   ",
    "                                                                                                                                                                                                      L            ",
    "                                                                                                                                                                                                     FL            ",
    "                                                                                E E                                                                                                                   L            ",
    "                      Q                                                         BBBBBBBB   BBBQ              $           BBB    BQQB                                                        HH        L            ",
    "                                                                                                                                                                                           HHH        L            ",
    "                                                                                                                                                                                          HHHH        L            ",
    "                                                                                                                                                                                         HHHHH        L            ",
    "                Q   B$BQB                                                    B$B              B     BB    Q  Q  Q     B          BB      H  H          HH  H            BBQB            HHHHHH        L   C        ",
    "                                              P           P                                                                             HH  HH        HHH  HH                          HHHHHHH        L            ",
    "                                      P       P           P                                                                            HHH  HHH      HHHH  HHH                        HHHHHHHH        L            ",
    "  M                   E     P         P       P    E E    P                                      E E       K      E  E      E E E E   HHHH  HHHH    HHHHH  HHHH     P         E E  P HHHHHHHHH        H            ",
    "=====================================================================  ===============   ================================================================  ========================================================",
    "=====================================================================  ===============   ================================================================  ========================================================",
]

# 音效載入
def create_sound(frequency, duration):
    """創建嗶聲"""
    try:
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate))
        buf = []
        for i in range(n_samples):
            value = int(32767 * 0.3 * (1 if (i // (sample_rate // frequency // 2)) % 2 else -1))
            buf.append((value, value))
        sound = pygame.sndarray.make_sound(buf)
        return sound
    except:
        return None

# pygame.mixer.init()
# game_sound = pygame.mixer.Sound(untitled_3.mp3)
jump_sound = create_sound(440, 0.1)
coin_sound = create_sound(880, 0.1)
powerup_sound = create_sound(660, 0.2)
squash_sound = create_sound(220, 0.15)
kick_sound = create_sound(300, 0.1)
flag_sound = create_sound(1000, 0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.is_big = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.vel_y = 0
        self.vel_x = 0
        self.max_speed = 5  # 最大移動速度
        self.acceleration = self.max_speed / 120  # 加速度（120幀達到最大速度）
        self.deceleration = self.max_speed / 120  # 減速度（120幀減速到0）
        self.jumping = False
        self.on_ground = False
        self.min_x = 0
        self.invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0
        self.visible = True
        self.on_flag = False
        self.flag_slide_speed = 3
        self.won = False
        self.waiting_for_flag = False
        self.facing_right = True
        self.is_dead = False  # 死亡狀態
        self.death_jump_done = False  # 死亡跳躍是否完成
        self.walking_to_castle = False  # 是否正在走向城堡
        self.castle_target_x = 0  # 城堡中心的x座標
        self.castle_walk_stage = 0  # 走向城堡的階段：0=下階梯, 1=走向城堡
        
        # 動畫相關
        self.animation_frame = 0  # 當前動畫幀
        self.animation_timer = 0  # 動畫計時器
        self.run_frame_duration = FPS // 3  # 每張跑步圖片顯示20幀
        
        self.update_size()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
    
    def update_size(self):
        old_bottom = self.rect.bottom if hasattr(self, 'rect') else None
        old_x = self.rect.x if hasattr(self, 'rect') else None
        
        if self.is_big:
            self.base_image = pygame.transform.scale(MARIO[0].copy(), (GRID_SIZE, GRID_SIZE * 2))
        else:
            self.base_image = pygame.transform.scale(MARIO[7].copy(), (GRID_SIZE, GRID_SIZE))
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        if old_bottom and old_x is not None:
            self.rect.bottom = old_bottom
            self.rect.x = old_x
    
    def get_current_image(self):
        """根據狀態獲取當前應該顯示的圖片索引"""
        if self.is_dead:
            return 6  # 死亡圖
        
        # 在旗桿上時使用靜止圖
        if self.on_flag or self.waiting_for_flag:
            return 0 if self.is_big else 7  # 靜止圖
        
        # 走向城堡時使用跑步動畫
        if self.walking_to_castle:
            if self.is_big:
                run_frames = [2, 3, 4]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
            else:
                run_frames = [9, 10, 11]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
        
        if self.is_big:
            # 大馬力歐
            if not self.on_ground:
                return 1  # 跳躍
            elif self.vel_x == 0:
                return 0  # 靜止
            elif (self.vel_x > 0 and not self.facing_right) or (self.vel_x < 0 and self.facing_right):
                return 5  # 滑行（速度與面向相反）
            else:
                # 跑步動畫
                run_frames = [2, 3, 4]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
        else:
            # 小馬力歐
            if not self.on_ground:
                return 8  # 跳躍
            elif self.vel_x == 0:
                return 7  # 靜止
            elif (self.vel_x > 0 and not self.facing_right) or (self.vel_x < 0 and self.facing_right):
                return 12  # 滑行（速度與面向相反）
            else:
                # 跑步動畫
                run_frames = [9, 10, 11]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
    
    def update_image_direction(self):
        """根據移動方向和狀態更新圖片"""
        img_index = self.get_current_image()
        
        if self.is_big:
            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
        else:
            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
        
        # 根據面向方向翻轉
        if self.facing_right:
            self.image = base_img
        else:
            self.image = pygame.transform.flip(base_img, True, False)
        
        # 更新動畫幀計數
        if self.vel_x != 0 and self.on_ground:
            self.animation_frame += 1
        else:
            self.animation_frame = 0
    
    def grow(self):
        global points
        if not self.is_big:
            self.is_big = True
            self.update_size()
            points += 1000
            if powerup_sound:
                powerup_sound.play()
    
    def die(self):
        """小馬力歐死亡"""
        if not self.is_dead:
            self.is_dead = True
            self.death_jump_done = False
            self.vel_x = 0
            self.vel_y = -10  # 向上跳半格的初速度（原本是-15）
            self.update_image_direction()  # 更新為死亡圖片
    
    def shrink(self):
        if self.is_big:
            self.is_big = False
            self.update_size()
            self.invincible = True
            self.invincible_timer = 120
        
    def update(self):
        global game_won, game_over, reset_timer
        
        # 死亡狀態處理
        if self.is_dead:
            self.vel_y += 0.8  # 重力
            self.rect.y += self.vel_y
            
            # 掉出視窗外
            if self.rect.top > SCREEN_HEIGHT:
                game_over = True
                reset_timer = 60
                return True
            
            return False
        
        # 更新圖片方向（根據移動方向和狀態）
        self.update_image_direction()
        
        if self.invincible:
            self.invincible_timer -= 1
            self.blink_timer += 1
            if self.blink_timer >= 5:
                self.visible = not self.visible
                self.blink_timer = 0
            
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True

        if self.waiting_for_flag:
            # 直接開始滑旗桿
            self.on_flag = True
            self.waiting_for_flag = False
        
        if self.on_flag:
            self.vel_x = 0
            self.vel_y = self.flag_slide_speed
            self.rect.y += self.vel_y
            
            for stair in stairs:
                if self.rect.colliderect(stair.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = stair.rect.top
                        self.vel_y = 0
                        self.on_flag = False
                        
                        # 開始暫停流程，面向右邊
                        self.facing_right = True
                        self.castle_walk_stage = -2  # 階段-2：面向右暫停
                        self.pause_timer = FPS // 2  # 0.5秒
                        
                        # 立即更新圖片方向（面向右邊）
                        img_index = 0 if self.is_big else 7
                        if self.is_big:
                            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
                        else:
                            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
                        self.image = base_img
                        
                        self.walking_to_castle = True  # 直接設置，不調用 start_walking_to_castle
                        # 找到城堡的中心位置
                        for castle in castles:
                            self.castle_target_x = castle.rect.centerx
                            break
                        return False
            return False
        
        # 走向城堡
        if self.walking_to_castle:
            # 階段-2：滑到底座，面向右邊暫停
            if self.castle_walk_stage == -2:
                self.pause_timer -= 1
                
                if self.pause_timer <= 0:
                    # 移到旗桿右邊
                    self.rect.x += GRID_SIZE
                    
                    # 轉向左邊
                    self.facing_right = False
                    img_index = 0 if self.is_big else 7
                    if self.is_big:
                        base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
                    else:
                        base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
                    self.image = pygame.transform.flip(base_img, True, False)
                    
                    # 進入下一階段
                    self.castle_walk_stage = -1
                    self.pause_timer = FPS // 2  # 再暫停0.5秒
                
                return False
            
            # 階段-1：在旗桿右邊，面向左邊暫停
            elif self.castle_walk_stage == -1:
                self.pause_timer -= 1
                
                if self.pause_timer <= 0:
                    # 轉向右邊，準備走下底座
                    self.facing_right = True
                    self.castle_walk_stage = 0  # 進入正常的走向城堡階段
                
                return False
            
            # 階段0：在階梯頂部往右走
            elif self.castle_walk_stage == 0:
                self.vel_x = self.max_speed / 4
                self.facing_right = True
                self.vel_y = 0
                self.rect.x += self.vel_x
                
                # 檢測是否還在階梯上
                on_stair = False
                for stair in stairs:
                    if self.rect.colliderect(stair.rect):
                        self.rect.bottom = stair.rect.top
                        on_stair = True
                        break
                
                # 如果不在階梯上了，開始下落
                if not on_stair:
                    self.castle_walk_stage = 1
                
                return False
            
            # 階段1：從階梯右側掉落到地面
            elif self.castle_walk_stage == 1:
                self.vel_x = self.max_speed / 4
                self.facing_right = True
                
                # 應用重力
                self.vel_y += 0.8
                if self.vel_y > 15:
                    self.vel_y = 15
                
                self.rect.x += self.vel_x
                self.rect.y += self.vel_y
                
                # 檢測是否落地
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vel_y > 0:
                            self.rect.bottom = platform.rect.top
                            self.vel_y = 0
                            self.castle_walk_stage = 2  # 進入下一階段
                            self.on_ground = True
                            break
                
                return False
            
            # 階段2：在地面上走向城堡中心
            elif self.castle_walk_stage == 2:
                self.vel_x = self.max_speed / 4
                self.facing_right = True
                self.vel_y = 0
                self.rect.x += self.vel_x
                
                # 保持在地面上
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vel_y > 0 or self.rect.bottom > platform.rect.top:
                            self.rect.bottom = platform.rect.top
                            self.vel_y = 0
                
                # 到達城堡中心
                if self.rect.centerx >= self.castle_target_x:
                    self.visible = False
                    self.won = True
                    game_won = True
                
                return False
        
        # 重力
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        # 先處理水平移動和水平碰撞
        self.rect.x += self.vel_x
        
        # 處理樓梯的水平碰撞
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_x > 0:
                    self.rect.right = stair.rect.left
                elif self.vel_x < 0:
                    self.rect.left = stair.rect.right
        
        # 處理地板的水平碰撞
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
        
        # 再處理垂直移動和垂直碰撞
        self.rect.y += self.vel_y
        
        # 地面檢測
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = stair.rect.bottom
                    self.vel_y = 0
                    
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.vel_y > 0 and self.rect.bottom - brick.rect.top < 20:
                    # 從上方落下：馬力歐底部接近磚塊頂部
                    self.rect.bottom = brick.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_x > 0 and self.rect.right - brick.rect.left < 20:
                    self.rect.right = brick.rect.left
                elif self.vel_x < 0 and brick.rect.right - self.rect.left < 20:
                    self.rect.left = brick.rect.right
                elif self.vel_y < 0 and brick.rect.bottom - self.rect.top < 20:
                    # 從下方撞擊：磚塊底部接近馬力歐頂部
                    self.rect.top = brick.rect.bottom
                    self.vel_y = 0
                    brick.bump()
                    if self.is_big and not brick.is_breaking:
                        brick.break_brick()
                    
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0 and self.rect.bottom - qblock.rect.top < 15:
                    # 從上方落下
                    self.rect.bottom = qblock.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_x > 0 and self.rect.right - qblock.rect.left < 20:
                    self.rect.right = qblock.rect.left
                elif self.vel_x < 0 and qblock.rect.right - self.rect.left < 20:
                    self.rect.left = qblock.rect.right
                elif self.vel_y < 0:
                    self.rect.top = qblock.rect.bottom
                    self.vel_y = 0
                    qblock.hit()
                    
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_y > 0 and self.rect.bottom - pipe.rect.top < 20:
                    self.rect.bottom = pipe.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_x > 0 and self.rect.right - pipe.rect.left < 20:
                    self.rect.right = pipe.rect.left
                elif self.vel_x < 0 and pipe.rect.right - self.rect.left < 20:
                    self.rect.left = pipe.rect.right
        
        for pipe_top in pipe_tops:
            if self.rect.colliderect(pipe_top.rect):
                if self.vel_y > 0 and self.rect.bottom - pipe_top.rect.top < 20:
                    self.rect.bottom = pipe_top.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_x > 0 and self.rect.right - pipe_top.rect.left < 20:
                    self.rect.right = pipe_top.rect.left
                elif self.vel_x < 0 and pipe_top.rect.right - self.rect.left < 20:
                    self.rect.left = pipe_top.rect.right
        
        for flagpole in flagpoles:
            if self.rect.colliderect(flagpole.rect):
                # 馬力歐往右移0.5格
                self.rect.x += GRID_SIZE // 2
                self.waiting_for_flag = True
                height_score = int((SCREEN_HEIGHT - self.rect.y) / GRID_SIZE) * 100
                global points
                points += height_score
                
                for flag_img in flag_images:
                    flag_img.start_descending(self.rect.y)
                
                if flag_sound:
                    flag_sound.play()
                break
        
        if self.rect.left < self.min_x:
            self.rect.left = self.min_x
            
        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False
    
    def jump(self):
        if self.on_flag or self.waiting_for_flag:
            return
        if not self.jumping and self.on_ground:
            self.vel_y = -18
            self.jumping = True
            if jump_sound:
                jump_sound.play()
    
    def start_walking_to_castle(self):
        """開始走向城堡"""
        self.walking_to_castle = True
        self.castle_walk_stage = 0  # 從下階梯開始
        # 找到城堡的中心位置
        for castle in castles:
            self.castle_target_x = castle.rect.centerx
            break

class Ground(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.image.load("PNG\\GroundBlock.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Stair(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.image.load("PNG\\HardBlock.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Brick(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.image.load("PNG\\Brick.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.original_y = grid_y * GRID_SIZE
        self.bump_timer = 0
        self.is_bumping = False
        self.is_breaking = False
        self.break_timer = 0
        self.break_particles = []
        
    def bump(self):
        if not self.is_bumping and not self.is_breaking:
            self.is_bumping = True
            self.bump_timer = 15  # 從30改為15幀
    
    def break_brick(self):
        global points
        points += 50
        
        # 創建破碎粒子
        for i in range(4):
            particle = {
                'x': self.rect.x + (i % 2) * GRID_SIZE // 2,
                'y': self.rect.y + (i // 2) * GRID_SIZE // 2,
                'vel_x': random.uniform(-3, 3),
                'vel_y': random.uniform(-8, -4),
                'size': GRID_SIZE // 4,
                'life': 30  # 粒子生命週期
            }
            brick_particles.append(particle)  # 添加到全局粒子列表
        
        self.kill()  # 磚塊立即消失
            
    def update(self):
        if self.is_bumping:
            if self.bump_timer > 7:  # 15幀的一半
                progress = (15 - self.bump_timer) / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            else:
                progress = self.bump_timer / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            
            self.bump_timer -= 1
            if self.bump_timer <= 0:
                self.is_bumping = False
                self.rect.y = self.original_y
    
def draw_brick_particles(screen, camera_x):
    """繪製所有磚塊破碎粒子"""
    for particle in brick_particles[:]:  # 使用切片來避免迭代時修改列表
        try:
            particle_rect = pygame.Rect(
                particle['x'] - camera_x,
                particle['y'],
                particle['size'],
                particle['size']
            )
            pygame.draw.rect(screen, ORANGE, particle_rect)
        except:
            pass

def update_brick_particles():
    """更新所有磚塊破碎粒子"""
    for particle in brick_particles[:]:  # 使用切片來避免迭代時修改列表
        particle['vel_y'] += 0.5  # 重力
        particle['x'] += particle['vel_x']
        particle['y'] += particle['vel_y']
        particle['life'] -= 1
        
        if particle['life'] <= 0:
            brick_particles.remove(particle)

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, item_type='coin'):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.item_type = item_type
        self.hit_count = 0
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.original_y = grid_y * GRID_SIZE
        self.bump_timer = 0
        self.is_bumping = False
        
    def create_image(self):
        if self.hit_count == 0:
            self.image = pygame.image.load("PNG\\MysteryBlock.png")
        else:
            self.image = pygame.image.load("PNG\\EmptyBlock.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
    
    def reset(self):
        self.hit_count = 0
        self.create_image()
        
    def hit(self):
        if self.hit_count == 0:
            self.is_bumping = True
            self.bump_timer = 15  # 從30改為15幀
            
            if self.item_type == 'mushroom':
                mushroom = Mushroom(self.rect.x, self.rect.y - GRID_SIZE)
                all_sprites.add(mushroom)
                powerups.add(mushroom)
            else:
                coin = Coin(self.rect.x, self.rect.y - GRID_SIZE)
                all_sprites.add(coin)
                coins.add(coin)
            
            self.hit_count += 1
            self.create_image()
                
    def update(self):
        if self.is_bumping:
            if self.bump_timer > 7:  # 15幀的一半
                progress = (15 - self.bump_timer) / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            else:
                progress = self.bump_timer / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            
            self.bump_timer -= 1
            if self.bump_timer <= 0:
                self.is_bumping = False
                self.rect.y = self.original_y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = int(GRID_SIZE * 0.75)
        self.image = pygame.image.load("PNG\\Coin.png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = -10
        self.lifetime = 30
        self.collected = False
        
    def update(self):
        if not self.collected and self.rect.colliderect(player.rect):
            global points, coins_collected
            points += 100
            coins_collected += 1
            self.collected = True
            if coin_sound:
                coin_sound.play()
        
        self.vel_y += 0.5
        self.rect.y += self.vel_y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.image.load("PNG\\MagicMushroom.png")
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - (GRID_SIZE // 2)
        self.vel_x = 2
        self.vel_y = 0
        
    def update(self):
        # 根據移動方向翻轉圖片（原圖向右，向左時翻轉）
        if self.vel_x < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image.copy()
        
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
            
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0 and self.rect.bottom - stair.rect.top < 20:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = stair.rect.left
                    else:
                        self.rect.left = stair.rect.right
                    self.vel_x *= -1
        
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.vel_y > 0 and self.rect.bottom - brick.rect.top < 20:
                    self.rect.bottom = brick.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = brick.rect.left
                    else:
                        self.rect.left = brick.rect.right
                    self.vel_x *= -1
        
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0 and self.rect.bottom - qblock.rect.top < 20:
                    self.rect.bottom = qblock.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = qblock.rect.left
                    else:
                        self.rect.left = qblock.rect.right
                    self.vel_x *= -1
        
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                self.vel_x *= -1

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                # 如果是移動的龜殼，需要判斷碰撞方向
                if isinstance(enemy, Koopa) and enemy.state == 'shell_moving':
                    # 蘑菇往右，龜殼也往右，龜殼從左側撞上
                    if self.vel_x > 0 and enemy.vel_x > 0 and enemy.rect.centerx < self.rect.centerx:
                        enemy.vel_x *= -1  # 龜殼反彈
                        continue  # 蘑菇保持原樣
                    # 蘑菇往左，龜殼也往左，龜殼從右側撞上
                    elif self.vel_x < 0 and enemy.vel_x < 0 and enemy.rect.centerx > self.rect.centerx:
                        enemy.vel_x *= -1  # 龜殼反彈
                        continue  # 蘑菇保持原樣
                
                # 其他情況雙方都反彈
                self.vel_x *= -1
                if hasattr(enemy, 'vel_x'):
                    enemy.vel_x *= -1
                
        if self.rect.colliderect(player.rect):
            player.grow()
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """Goomba 敵人"""
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.base_image = pygame.image.load("PNG\\Goomba_Walk1.png")
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.start_x = grid_x * GRID_SIZE
        self.start_y = grid_y * GRID_SIZE
        self.vel_x = -2
        self.vel_y = 0
        self.is_squashed = False
        self.squash_timer = 0
        self.is_dying = False  # 被龜殼擊中的死亡狀態
        self.death_rotation = 0  # 死亡旋轉角度
        self.flip_timer = 0  # 圖片翻轉計時器
        self.is_flipped = False  # 是否翻轉
        
    def die_from_shell(self):
        """被龜殼擊中而死亡"""
        global points
        self.is_dying = True
        self.vel_x = 0
        self.vel_y = -10  # 向上跳半格（原本是-15）
        self.death_rotation = 0
        points += 200
        
    def squash(self):
        global points
        self.is_squashed = True
        self.squash_timer = 30
        self.vel_x = 0
        self.vel_y = 0
        points += 200
        old_bottom = self.rect.bottom
        old_x = self.rect.x
        self.image = pygame.image.load("PNG\\Goomba_Flat.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE//3))
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.x = old_x
        if squash_sound:
            squash_sound.play()
        
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vel_x = -2
        self.vel_y = 0
        self.is_squashed = False
        self.squash_timer = 0
        self.image = pygame.image.load("PNG\\Goomba_Walk1.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        
    def update(self):
        # 被龜殼擊中的死亡動畫
        if self.is_dying:
            self.vel_y += 0.8  # 重力
            self.rect.y += self.vel_y
            self.death_rotation += 6  # 每幀旋轉6度，60幀=360度，但我們只要180度
            
            # 更新旋轉圖片
            original_img = pygame.image.load("PNG\\Goomba_Walk1.png")
            original_img = pygame.transform.scale(original_img, (GRID_SIZE, GRID_SIZE))
            
            # 旋轉圖片（限制在180度）
            rotation = min(self.death_rotation, 180)
            self.image = pygame.transform.rotate(original_img, rotation)
            # 更新rect中心位置
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            # 掉出視窗外就消失
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            return
        
        if self.is_squashed:
            self.squash_timer -= 1
            if self.squash_timer <= 0:
                self.kill()
            return
        
        # 正常行走時的圖片翻轉動畫（每20幀翻轉一次）
        self.flip_timer += 1
        if self.flip_timer >= FPS // 3:  # 20幀
            self.flip_timer = 0
            self.is_flipped = not self.is_flipped
            
            old_rect = self.rect.copy()  # 保存原始位置
            if self.is_flipped:
                self.image = pygame.transform.flip(self.base_image, True, False)
            else:
                self.image = self.base_image.copy()
            self.rect = self.image.get_rect()  # 重新獲取rect
            self.rect.topleft = old_rect.topleft  # 恢復位置
        
        # 正常移動邏輯
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
            
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0 and self.rect.bottom - stair.rect.top < 20:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = stair.rect.left
                    else:
                        self.rect.left = stair.rect.right
                    self.vel_x *= -1
        
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.vel_y > 0 and self.rect.bottom - brick.rect.top < 20:
                    self.rect.bottom = brick.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = brick.rect.left
                    else:
                        self.rect.left = brick.rect.right
                    self.vel_x *= -1
        
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0 and self.rect.bottom - qblock.rect.top < 20:
                    self.rect.bottom = qblock.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = qblock.rect.left
                    else:
                        self.rect.left = qblock.rect.right
                    self.vel_x *= -1
        
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_y > 0 and self.rect.bottom - pipe.rect.top < 20:
                    self.rect.bottom = pipe.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x > 0:
                        self.rect.right = pipe.rect.left
                    else:
                        self.rect.left = pipe.rect.right
                    self.vel_x *= -1
        
        # 敵人互撞 - Goomba與其他敵人
        for other_enemy in enemies:
            if other_enemy != self and not self.is_squashed:
                if self.rect.colliderect(other_enemy.rect):
                    # 如果對方是被踩扁的，不處理
                    if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                        continue
                    # 如果對方正在死亡，不處理
                    if hasattr(other_enemy, 'is_dying') and other_enemy.is_dying:
                        continue
                    # 如果對方是靜止或旋轉的龜殼，不處理（龜殼會處理）
                    if isinstance(other_enemy, Koopa) and other_enemy.state in ['shell', 'shell_moving']:
                        continue
                    # 雙方都反向
                    if self.vel_x > 0:
                        self.rect.right = other_enemy.rect.left
                    else:
                        self.rect.left = other_enemy.rect.right
                    self.vel_x *= -1
                    # 對方也反向
                    if hasattr(other_enemy, 'vel_x'):
                        other_enemy.vel_x *= -1

class Koopa(pygame.sprite.Sprite):
    """烏龜敵人 - 改進版本"""
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.state = 'walking'  # walking, shell, shell_moving, spinning
        
        # 載入烏龜行走動畫（使用KOOPA陣列）
        self.walk_images = [
            pygame.transform.scale(KOOPA[0].copy(), (GRID_SIZE, int(GRID_SIZE * 1.5))),
            pygame.transform.scale(KOOPA[1].copy(), (GRID_SIZE, int(GRID_SIZE * 1.5)))
        ]
        
        self.shell_image = pygame.image.load("PNG\\Koopa_Shell.png")
        self.shell_image = pygame.transform.scale(self.shell_image, (GRID_SIZE, GRID_SIZE))
        
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.start_x = grid_x * GRID_SIZE
        self.start_y = grid_y * GRID_SIZE
        self.vel_x = -2
        self.vel_y = 0
        self.spin_speed = 8  # 提高龜殼速度，確保比馬力歐快(馬力歐是5)
        self.animation_frame = 0  # 動畫幀計數器
        self.walk_frame_duration = FPS // 3  # 每張圖片顯示20幀
        
    def stomp(self):
        """被踩 - 大小瑪利歐都能踩成龜殼"""
        global points
        if self.state == 'walking':
            self.state = 'shell'
            old_bottom = self.rect.bottom
            old_x = self.rect.x
            self.image = self.shell_image
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.x = old_x
            self.vel_x = 0
            points += 200
            if squash_sound:
                squash_sound.play()
    
    def kick(self, from_left):
        """踢龜殼 - 大小瑪利歐都能踢，不會受傷"""
        global points
        if self.state == 'shell' and self.vel_x == 0:
            self.state = 'shell_moving'  # 改為 shell_moving 而不是 spinning
            if from_left:
                self.vel_x = self.spin_speed
            else:
                self.vel_x = -self.spin_speed
            points += 100
            if kick_sound:
                kick_sound.play()
    
    def reset(self):
        self.state = 'walking'
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vel_x = -2
        self.vel_y = 0
        self.image = self.walk_image
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        
    def update(self):
        # 更新動畫（行走狀態）
        if self.state == 'walking':
            self.animation_frame += 1
            frame_index = (self.animation_frame // self.walk_frame_duration) % 2
            base_image = self.walk_images[frame_index]
            
            # 根據移動方向翻轉圖片（原圖向左，向右時翻轉）
            if self.vel_x > 0:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image

        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
            
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        if self.state == 'shell_moving':
            # 移動的龜殼(shell_moving)與其他敵人的互動
            for enemy in enemies:
                if enemy != self and self.rect.colliderect(enemy.rect):
                    if isinstance(enemy, Koopa):
                        # 與其他烏龜的互動
                        if enemy.state == 'walking':
                            enemy.stomp()  # 變成龜殼
                        elif enemy.state == 'shell_moving':
                            # 兩個移動中的龜殼互撞 - 改變彼此方向
                            self.vel_x *= -1
                            enemy.vel_x *= -1
                    elif hasattr(enemy, 'squash'):
                        # 擊殺 Goomba - 使用死亡動畫
                        enemy.die_from_shell()
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_y > 0 and self.rect.bottom - platform.rect.top < 20:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                    elif self.vel_x > 0 and self.rect.right - platform.rect.left < 20:
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0 and platform.rect.right - self.rect.left < 20:
                        self.rect.left = platform.rect.right        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0 and self.rect.bottom - stair.rect.top < 20:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x != 0:
                        if self.vel_x > 0:
                            self.rect.right = stair.rect.left
                        else:
                            self.rect.left = stair.rect.right
                        self.vel_x *= -1

        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_y > 0 and self.rect.bottom - pipe.rect.top < 20:
                    self.rect.bottom = pipe.rect.top
                    self.vel_y = 0
                else:
                    if self.vel_x != 0:
                        if self.vel_x > 0:
                            self.rect.right = pipe.rect.left
                        else:
                            self.rect.left = pipe.rect.right
                        self.vel_x *= -1
        
        # 烏龜與其他敵人互撞
        if self.state == 'walking':
            for other_enemy in enemies:
                if other_enemy != self:
                    if self.rect.colliderect(other_enemy.rect):
                        # 如果對方是被踩扁的，不處理
                        if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                            continue
                        # 如果對方是移動的龜殼，不處理（會被撞死）
                        if isinstance(other_enemy, Koopa) and other_enemy.state == 'shell_moving':
                            continue
                        # 雙方都反向
                        if self.vel_x > 0:
                            self.rect.right = other_enemy.rect.left
                        else:
                            self.rect.left = other_enemy.rect.right
                        self.vel_x *= -1
                        # 對方也反向
                        if hasattr(other_enemy, 'vel_x'):
                            other_enemy.vel_x *= -1
        
        # 龜殼（靜止和移動）也會阻擋其他敵人
        elif self.state in ['shell', 'shell_moving']:
            for other_enemy in enemies:
                if other_enemy != self:
                    if self.rect.colliderect(other_enemy.rect):
                        # 如果對方是被踩扁的，不處理
                        if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                            continue
                        # 如果這是移動的龜殼，已經在上面處理擊殺了
                        if self.state == 'shell_moving':
                            continue
                        # 靜止龜殼阻擋其他敵人
                        if hasattr(other_enemy, 'vel_x'):
                            if other_enemy.vel_x > 0:
                                other_enemy.rect.right = self.rect.left
                            else:
                                other_enemy.rect.left = self.rect.right
                            other_enemy.vel_x *= -1

class Pipe(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, grid_height):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_height = grid_height
        width = GRID_SIZE * 2
        height = grid_height * GRID_SIZE
        self.image = pygame.image.load("PNG\\PipeBottom.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class PipeTop(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        width = GRID_SIZE * 2
        height = GRID_SIZE
        self.image = pygame.image.load("PNG\\PipeTop.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class FlagPole(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        original_image = pygame.image.load("PNG\\FlagPole.png")
        original_width = original_image.get_width()
        original_height = original_image.get_height()
        
        target_height = GRID_SIZE * 10
        aspect_ratio = original_width / original_height
        target_width = int(target_height * aspect_ratio)
        self.image = pygame.transform.scale(original_image, (target_width, target_height))
        
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE + (GRID_SIZE - self.rect.width) // 2
        self.rect.y = grid_y * GRID_SIZE

class FlagImage(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.original_y = grid_y * GRID_SIZE
        self.is_descending = False
        self.descend_speed = 5  # 降落速度
        
        self.image = pygame.image.load("PNG\\Flag.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
    
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = self.original_y
    
    def start_descending(self, player_y):
        self.is_descending = True
    
    def update(self):
        if self.is_descending:
            # 假設旗幟將在下一幀到達的位置
            next_y = self.rect.y + self.descend_speed
            hit_stair = False
            
            # --- 碰撞檢測邏輯 ---
            for stair in stairs:
                # 檢查旗子是否在旗杆所在的階梯水平範圍內
                if self.rect.left < stair.rect.right and self.rect.right > stair.rect.left:
                    # 檢查下一幀是否會與階梯頂部碰撞
                    if next_y + self.rect.height >= stair.rect.top and self.rect.y + self.rect.height <= stair.rect.top:
                        # 碰撞發生：將旗幟精確地停在階梯頂部
                        self.rect.y = stair.rect.top - self.rect.height
                        hit_stair = True
                        break
            
            # --- 持續下滑邏輯 ---
            if not hit_stair:
                self.rect.y += self.descend_speed

class Castle(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.image.load("PNG\\Castle.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE * 5, GRID_SIZE * 4))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=0.3):
        super().__init__()
        self.image = pygame.image.load("PNG\\Cloud1.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE * 3, GRID_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

def load_level(level_map):
    global player
    
    all_sprites.empty()
    platforms.empty()
    stairs.empty()
    bricks.empty()
    question_blocks.empty()
    enemies.empty()
    pipes.empty()
    pipe_tops.empty()
    coins.empty()
    powerups.empty()
    flagpoles.empty()
    flag_images.empty()
    castles.empty()
    clouds.empty()
    
    brick_data = []
    enemy_data = []
    platform_data = []
    enemy_spawn_data = []
    
    cloud_positions = [(200, 80), (500, 60), (800, 90), (1200, 70), (1600, 80), 
                      (2000, 60), (2400, 90), (2800, 70), (3200, 80), (3600, 60),
                      (4000, 90), (4400, 70), (4800, 80), (5200, 60), (5600, 90),
                      (6000, 70), (6400, 80), (6800, 60), (7200, 90)]
    for x, y in cloud_positions:
        cloud = Cloud(x, y)
        clouds.add(cloud)
        all_sprites.add(cloud)
    
    pipe_positions = {}
    
    for y, row in enumerate(level_map):
        for x, char in enumerate(row):
            if char == 'P':
                if x not in pipe_positions:
                    pipe_positions[x] = []
                pipe_positions[x].append(y)
    
    flagpole_start_y = None
    flagpole_x = None
    
    for y, row in enumerate(level_map):
        x = 0
        while x < len(row):
            char = row[x]
            
            if char == 'M':
                player = Player(x, y)
                all_sprites.add(player)
                
            elif char == 'B':
                brick = Brick(x, y)
                bricks.add(brick)
                all_sprites.add(brick)
                brick_data.append((x, y))
                
            elif char == 'Q':
                qblock = QuestionBlock(x, y, 'coin')
                question_blocks.add(qblock)
                all_sprites.add(qblock)
                
            elif char == '$':
                qblock = QuestionBlock(x, y, 'mushroom')
                question_blocks.add(qblock)
                all_sprites.add(qblock)
                
            elif char == 'E':
                enemy_x_pos = x * GRID_SIZE
                if enemy_x_pos < SCREEN_WIDTH:
                    enemy = Enemy(x, y)
                    enemies.add(enemy)
                    all_sprites.add(enemy)
                    enemy_data.append((x, y, 'goomba'))
                else:
                    enemy_spawn_data.append({'x': x, 'y': y, 'type': 'goomba', 'spawned': False})
                    enemy_data.append((x, y, 'goomba'))
            
            elif char == 'K':
                enemy_x_pos = x * GRID_SIZE
                if enemy_x_pos < SCREEN_WIDTH:
                    koopa = Koopa(x, y)
                    enemies.add(koopa)
                    all_sprites.add(koopa)
                    enemy_data.append((x, y, 'koopa'))
                else:
                    enemy_spawn_data.append({'x': x, 'y': y, 'type': 'koopa', 'spawned': False})
                    enemy_data.append((x, y, 'koopa'))
                
            elif char == 'P':
                if x in pipe_positions and y == min(pipe_positions[x]):
                    pipe_top = PipeTop(x, y - 1)
                    pipe_tops.add(pipe_top)
                    all_sprites.add(pipe_top)
                
                pipe_height = GRID_HEIGHT - y - 1
                pipe = Pipe(x, y, pipe_height)
                pipes.add(pipe)
                all_sprites.add(pipe)
                x += 1
            
            elif char == 'H':
                stair = Stair(x, y)
                stairs.add(stair)
                all_sprites.add(stair)
            
            elif char == 'L':
                if flagpole_start_y is None or flagpole_x != x:
                    flagpole_start_y = y
                    flagpole_x = x
                    flagpole = FlagPole(x, y)
                    flagpoles.add(flagpole)
                    all_sprites.add(flagpole)
            
            elif char == 'F':
                flag_img = FlagImage(x + 0.5, y)  # 往右移0.5格（原本是+1，現在改為+0.5）
                flag_images.add(flag_img)
                all_sprites.add(flag_img)
            
            elif char == 'C':
                castle = Castle(x, y)
                castles.add(castle)
                all_sprites.add(castle)
                
            elif char == '=':
                ground = Ground(x, y)
                platforms.add(ground)
                all_sprites.add(ground)
                platform_data.append((x, y, 1, 1))
                
            x += 1
    
    return brick_data, enemy_data, platform_data, len(level_map[0]), enemy_spawn_data

def draw_hud():
    font = pygame.font.Font(None, 36)
    
    score_text = font.render(f"SCORE: {points:06d}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    coins_text = font.render(f"COINS: {coins_collected:02d}", True, WHITE)
    screen.blit(coins_text, (250, 10))
    
    time_text = font.render(f"TIME: {max(0, game_time):03d}", True, WHITE)
    screen.blit(time_text, (500, 10))
    
    status_text = font.render(f"MARIO: {'BIG' if player.is_big else 'SMALL'}", True, WHITE)
    screen.blit(status_text, (750, 10))
    
    small_font = pygame.font.Font(None, 24)
    controls_text = small_font.render("Arrow Keys: Move | Space/Up: Jump | P: Pause | R: Restart", True, WHITE)
    screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

def draw_win_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    
    win_text = font_large.render("CONGRATULATIONS!", True, WHITE)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(win_text, win_rect)
    
    score_text = font_medium.render(f"Final Score: {points:06d}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    restart_text = font_medium.render("Press R to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
    screen.blit(restart_text, restart_rect)

# 全局磚塊破碎粒子列表
brick_particles = []

# 創建精靈群組
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
stairs = pygame.sprite.Group()
bricks = pygame.sprite.Group()
question_blocks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
pipes = pygame.sprite.Group()
pipe_tops = pygame.sprite.Group()
coins = pygame.sprite.Group()
powerups = pygame.sprite.Group()
flagpoles = pygame.sprite.Group()
flag_images = pygame.sprite.Group()
castles = pygame.sprite.Group()
clouds = pygame.sprite.Group()

brick_init_data, enemy_init_data, platform_init_data, GRID_WIDTH, enemy_spawn_list = load_level(level_map)

game_over = False
reset_timer = 0
camera_x = 0

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not game_over and not game_won and not game_paused:
                    player.jump()
            elif event.key == pygame.K_p:
                game_paused = not game_paused  # 切換暫停狀態
            elif event.key == pygame.K_r:
                brick_particles.clear()  # 清空磚塊破碎粒子
                brick_init_data, enemy_init_data, platform_init_data, GRID_WIDTH, enemy_spawn_list = load_level(level_map)
                game_over = False
                game_won = False
                camera_x = 0
                player.min_x = 0
                player.is_big = False
                player.update_size()
                points = 0
                coins_collected = 0
                game_time = 400
                time_counter = 0
    
    if game_over:
        reset_timer -= 1
        if reset_timer <= 0:
            brick_particles.clear()  # 清空磚塊破碎粒子
            brick_init_data, enemy_init_data, platform_init_data, GRID_WIDTH, enemy_spawn_list = load_level(level_map)
            game_over = False
            game_won = False
            camera_x = 0
            player.min_x = 0
            player.is_big = False
            player.update_size()
            points = 0
            coins_collected = 0
            game_time = 400
            time_counter = 0
    elif not game_won and not game_paused:  # 添加暫停檢查
        time_counter += 1
        if time_counter >= FPS:
            game_time -= 1
            time_counter = 0
            if game_time <= 0:
                game_over = True
                reset_timer = 120
        
        keys = pygame.key.get_pressed()
        
        # 只有在非走向城堡狀態時才處理玩家輸入
        if not player.walking_to_castle:
            # 處理左右移動 - 加速減速系統
            if keys[pygame.K_LEFT]:
                # 按左鍵
                if player.vel_x > 0:
                    # 原本向右移動，現在按左 - 快速減速（滑行）
                    player.vel_x -= player.deceleration * 2
                    if player.vel_x < 0:
                        player.vel_x = 0
                else:
                    # 向左加速
                    player.vel_x -= player.acceleration
                    if player.vel_x < -player.max_speed:
                        player.vel_x = -player.max_speed
                player.facing_right = False
                
            elif keys[pygame.K_RIGHT]:
                # 按右鍵
                if player.vel_x < 0:
                    # 原本向左移動，現在按右 - 快速減速（滑行）
                    player.vel_x += player.deceleration * 2
                    if player.vel_x > 0:
                        player.vel_x = 0
                else:
                    # 向右加速
                    player.vel_x += player.acceleration
                    if player.vel_x > player.max_speed:
                        player.vel_x = player.max_speed
                player.facing_right = True
                
            else:
                # 沒有按左右鍵 - 自然減速
                if player.vel_x > 0:
                    player.vel_x -= player.deceleration
                    if player.vel_x < 0:
                        player.vel_x = 0
                elif player.vel_x < 0:
                    player.vel_x += player.deceleration
                    if player.vel_x > 0:
                        player.vel_x = 0
        
        fell = player.update()
        if fell:
            if not player.is_dead:
                # 掉下洞直接結束遊戲，不播放死亡動畫
                game_over = True
                reset_timer = 60
        else:
            all_sprites.update()
            update_brick_particles()  # 更新磚塊破碎粒子
            
            spawn_threshold = camera_x + SCREEN_WIDTH + GRID_SIZE
            for spawn_info in enemy_spawn_list:
                if not spawn_info['spawned']:
                    enemy_x_pos = spawn_info['x'] * GRID_SIZE
                    if enemy_x_pos <= spawn_threshold:
                        if spawn_info['type'] == 'goomba':
                            enemy = Enemy(spawn_info['x'], spawn_info['y'])
                        else:
                            enemy = Koopa(spawn_info['x'], spawn_info['y'])
                        enemies.add(enemy)
                        all_sprites.add(enemy)
                        spawn_info['spawned'] = True
            
            max_camera_x = (GRID_WIDTH - SCREEN_GRID_WIDTH) * GRID_SIZE
            if player.rect.x > SCREEN_WIDTH // 2:
                new_camera_x = player.rect.x - SCREEN_WIDTH // 2
                if new_camera_x > max_camera_x:
                    new_camera_x = max_camera_x
                if new_camera_x > camera_x:
                    camera_x = new_camera_x
            
            player.min_x = camera_x
            
            # 只有活著的馬力歐才會與敵人碰撞
            if not player.invincible and not player.is_dead:
                for enemy in enemies:
                    if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                        continue
                    if hasattr(enemy, 'is_dying') and enemy.is_dying:
                        continue  # 忽略死亡中的栗寶寶
                    
                    if enemy.rect.colliderect(player.rect):
                        # 烏龜特殊處理
                        if isinstance(enemy, Koopa):
                            # 優先檢查是否從上方踩（提高踩踏判定：左右各增加1格空間，總共3格寬）
                            stomp_left = player.rect.left - GRID_SIZE
                            stomp_right = player.rect.right + GRID_SIZE
                            # 從上方踩的判定：玩家向下移動或剛著地，且底部接近敵人頂部
                            can_stomp = (player.vel_y >= 0 and 
                                       player.rect.bottom - enemy.rect.top < 30 and
                                       player.rect.bottom >= enemy.rect.top and
                                       player.rect.top < enemy.rect.top and
                                       stomp_right > enemy.rect.left and 
                                       stomp_left < enemy.rect.right)
                            
                            if can_stomp and enemy.state == 'walking':
                                # 從上方踩行走烏龜 - 變成龜殼，不受傷
                                enemy.stomp()
                                player.vel_y = -10
                                continue  # 繼續檢查其他敵人
                            elif can_stomp and enemy.state == 'shell_moving':
                                # 從上方踩移動中的龜殼 - 檢查踩踏位置
                                shell_center = enemy.rect.centerx
                                player_center = player.rect.centerx
                                offset = abs(player_center - shell_center)
                                
                                if offset < GRID_SIZE // 4:  # 踩在正中間（±0.25格範圍）
                                    # 站在龜殼上，不跳動
                                    enemy.state = 'shell'
                                    enemy.vel_x = 0
                                    player.vel_y = 0
                                else:
                                    # 踩在側邊，龜殼停下來並彈跳
                                    enemy.state = 'shell'
                                    enemy.vel_x = 0
                                    player.vel_y = -10
                                continue
                            elif can_stomp and enemy.state == 'shell':
                                # 從上方踩靜止龜殼 - 根據踩踏位置決定行為
                                shell_center = enemy.rect.centerx
                                player_center = player.rect.centerx
                                offset = abs(player_center - shell_center)
                                
                                if offset < GRID_SIZE // 4:  # 踩在正中間（±0.25格範圍）
                                    # 站在龜殼上，只彈跳
                                    player.vel_y = -10
                                elif player_center < shell_center:
                                    # 踩在左邊，龜殼往右移動
                                    enemy.kick(True)  # from_left = True
                                    player.vel_y = -10
                                else:
                                    # 踩在右邊，龜殼往左移動
                                    enemy.kick(False)  # from_left = False
                                    player.vel_y = -10
                                continue
                            # 檢查是否是靜止龜殼
                            elif enemy.state == 'shell' and enemy.vel_x == 0:
                                # 靜止龜殼，踢它
                                from_left = player.rect.centerx < enemy.rect.centerx
                                enemy.kick(from_left)
                                continue
                            # 檢查是否是移動中的龜殼
                            elif enemy.state == 'shell_moving':
                                # 判斷碰撞的方向和移動方向
                                # 如果馬力歐在龜殼左側
                                if player.rect.centerx < enemy.rect.centerx:
                                    # 龜殼往右移動 (vel_x > 0)，且馬力歐也往右移動 (vel_x > 0)
                                    # 馬力歐碰到龜殼左側，不受傷
                                    if enemy.vel_x > 0 and player.vel_x > 0:
                                        continue
                                # 如果馬力歐在龜殼右側
                                else:
                                    # 龜殼往左移動 (vel_x < 0)，且馬力歐也往左移動 (vel_x < 0)
                                    # 馬力歐碰到龜殼右側，不受傷
                                    if enemy.vel_x < 0 and player.vel_x < 0:
                                        continue
                                
                                # 其他情況：移動中的龜殼會造成傷害
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
                            # 行走烏龜 - 會傷害（但前面已經檢查過踩踏了）
                            elif enemy.state == 'walking':
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
                        # Goomba處理（提高踩踏判定：左右各增加1格空間，總共3格寬，與烏龜一致）
                        elif hasattr(enemy, 'squash'):
                            stomp_left = player.rect.left - GRID_SIZE
                            stomp_right = player.rect.right + GRID_SIZE
                            # 從上方踩的判定：玩家向下移動或剛著地，且底部接近敵人頂部
                            can_stomp = (player.vel_y >= 0 and 
                                       player.rect.bottom - enemy.rect.top < 30 and
                                       player.rect.bottom >= enemy.rect.top and
                                       player.rect.top < enemy.rect.top and
                                       stomp_right > enemy.rect.left and 
                                       stomp_left < enemy.rect.right)
                            
                            if can_stomp:
                                enemy.squash()
                                player.vel_y = -10
                                continue  # 繼續檢查其他敵人，不執行後面的傷害判定
                            else:
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
    
    screen.fill(SKY_BLUE)
    
    for cloud in clouds:
        screen.blit(cloud.image, (cloud.rect.x - camera_x * cloud.speed, cloud.rect.y))
    
    for sprite in all_sprites:
        if sprite not in clouds and sprite != player:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    # for enemy in enemies:
    #     screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
    #     # 顯示敵人的碰撞框（紅色）
    #     debug_rect = pygame.Rect(enemy.rect.x - camera_x, enemy.rect.y, enemy.rect.width, enemy.rect.height)
    #     pygame.draw.rect(screen, RED, debug_rect, 2)
    
    # 繪製磚塊破碎粒子
    draw_brick_particles(screen, camera_x)
    
    if player.visible:
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
    
    draw_hud()
    
    if game_won:
        draw_win_screen()
    
    pygame.display.flip()

pygame.quit()
sys.exit()