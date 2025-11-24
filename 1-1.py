import pygame
import sys
import random

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 遊戲設定 - 網格系統
GRID_SIZE = 40  # 每個格子的像素大小
GRID_HEIGHT = 15  # 關卡高度 (15格)
SCREEN_GRID_WIDTH = 20  # 螢幕顯示寬度 (20格)
SCREEN_WIDTH = SCREEN_GRID_WIDTH * GRID_SIZE  # 800像素
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE  # 600像素
FPS = 60

# 字體
FONT = "resources\\fonts\\super-mario-bros-nes.otf"

# 馬力歐圖片陣列
MARIO = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Idle.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Jump.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Run1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Run2.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Run3.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Big_Slide.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Death.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Idle.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Jump.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Run1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Run2.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Run3.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Mario_Small_Slide.png"),
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario1.png"),# stop
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario2.png"),# run1
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario3.png"),# run2
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario4.png"),# run3
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario5.png"),# jump
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario6.png"),# slide
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Fire Mario7.png"),
    pygame.image.load("resources\\graphics\\Mario Universe.com\\Big Mario1.png"),
]

# 烏龜圖片陣列
KOOPA = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Koopa_Walk1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Koopa_Walk2.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Koopa_Shell.png"),
]

BLOCK = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\GroundBlock.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\HardBlock.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\MysteryBlock.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\EmptyBlock.png"),
]

BRICK = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Brick.png")
]

COIN = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Coin.png")
]

MASHROOM = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\MagicMushroom.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\1upMushroom.png")
]

STAR = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Starman.png")
]

SUNFLOWER = [
    pygame.image.load("resources\\graphics\\the Mario encyclopedia\\SMB_Sprite_Fire_Flower.png") # https://www.mariowiki.com/List_of_power-ups
]

FIREBALL = [
    pygame.image.load("resources\\graphics\\Icon Archive\\Ph03nyx-Super-Mario-Retro-Fire-Ball.256.png")
]

GOOMBA = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Goomba_Walk1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Goomba_Flat.png")
]

PIPE = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\PipeBottom.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\PipeTop.png")
]

FLAG = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\FlagPole.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Flag.png")
]

CASTLE = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Castle.png")
]

CLOUD = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Cloud1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Cloud2.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Cloud3.png"),
]

BUSH = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Bush1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Bush2.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Bush3.png"),
]

HILL = [
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Hill1.png"),
    pygame.image.load("resources\\graphics\\unity-super-mario-tutorial\\Hill2.png"),
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
game_time = 400
time_counter = 0
game_won = False
game_paused = False
game_muted = False
live = 3
is_fire_mario = False
fireballs = pygame.sprite.Group()
checkpoint_x = 0
checkpoint_activated = False
initial_player_x = 0
initial_player_y = 0
invincible_star_timer = 0
growing_timer = 0 # 小馬力歐變大馬力歐計時器
transforming_timer = 0  # 大馬力歐變火焰馬力歐計時器
fire_to_big_timer = 0  # 火焰馬力歐變大馬力歐計時器
big_to_small_timer = 0  # 大馬力歐變小馬力歐計時器
score_popups = []
respawn_timer = 0
calculating_score = False  # 是否正在計算分數
score_calculation_timer = 0  # 分數計算計時器
target_points = 0  # 目標分數
start_points = 0  # 起始分數
start_coins = 0  # 起始金幣
start_time = 0  # 起始時間
death_sound_playing = False  # 死亡音效是否正在播放
death_sound_timer = 0  # 死亡音效計時器
walking_to_castle = False
star_music_playing = False  # 星星音樂是否正在播放
game_over_sound_played = False  # Game Over音效是否已播放
hurry_sound_played = False  # 時間緊急音效是否已播放過
hurry_sound_end_timer = 0  # 時間緊急音效結束計時器
game_sound_channel = None  # 背景音樂頻道
hurry_sound_channel = None  # 緊急音效頻道
star_sound_channel = None  # 星星音樂頻道
show_hitboxes = False

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
    "                                                                1                                                                                                                        HHHHH        L            ",
    "                Q   B$BQB                                                    B$B              2     B3    Q  Q  Q     B          BB      H  H          HH  H            BBQB            HHHHHH        L   C        ",
    "                                              P           P                                                                             HH  HH        HHH  HH                          HHHHHHH        L            ",
    "                                      P       P           P                                                                            HHH  HHH      HHHH  HHH                        HHHHHHHH        L            ",
    "   M                  E     P         P E     P    E E    P                       A              E E       K      E  E      E E E E   HHHH  HHHH    HHHHH  HHHH     P         E E  P HHHHHHHHH        H            ",
    "=====================================================================  ===============   ================================================================  ========================================================",
    "=====================================================================  ===============   ================================================================  ========================================================",
]

# 音效載入
game_sound = pygame.mixer.Sound("resources\\sounds\\Myinstants\\game_sound.mp3")
hurry_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_warning.wav")
jump_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_jump-small.wav")
long_jump_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_jump-super.wav")
coin_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_coin.wav")
powerup_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_powerup.wav")
kick_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_kick.wav")
flagpole_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_flagpole.wav")
stomp_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_stomp.wav")
bump_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_bump.wav")
smash_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_breakblock.wav")
star_sound = pygame.mixer.Sound("resources\\sounds\\Myinstants\\Star.mp3")
level_complete_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_stage_clear.wav")
death_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_mariodie.wav")
pause_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_pause.wav")
plus_live_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_1-up.wav")
game_over_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_gameover.wav")
appear_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_powerup_appears.wav")
fireball_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_fireball.wav")
firework_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_fireworks.wav")
pipe_sound = pygame.mixer.Sound("resources\\sounds\\The Mushroom Kingdom\\smb_pipe.wav")

class ScorePopup:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.timer = FPS
        self.start_y = y
        
    def update(self):
        self.timer -= 1
        progress = (FPS - self.timer) / FPS
        self.y = self.start_y - (GRID_SIZE // 2) * progress
        return self.timer > 0
    
    def draw(self, screen, camera_x):
        font = pygame.font.Font(FONT, 16)
        text = font.render(str(self.score), True, WHITE)
        screen.blit(text, (self.x - camera_x, self.y))

def add_score_popup(x, y, score):
    score_popups.append(ScorePopup(x, y - GRID_SIZE, score))

class Player(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.is_big = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.vel_y = 0
        self.vel_x = 0
        self.max_speed = 5
        self.acceleration = self.max_speed / 120
        self.deceleration = self.max_speed / 120
        self.mushroom_speed_ratio = 0.4
        self.star_speed_ratio = 0.6
        self.enemy_speed_ratio = 0.25
        self.koopa_speed_ratio = 0.25
        self.shell_speed_ratio = 1.75
        self.castle_walk_ratio = 0.25
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
        self.is_dead = False
        self.death_jump_done = False
        self.walking_to_castle = False
        self.castle_target_x = 0
        self.castle_walk_stage = 0
        self.animation_frame = 0
        self.animation_timer = 0
        self.run_frame_duration = FPS // 3
        self.is_crouching = False
        self.shooting_timer = 0
        self.hit_wall = False
        
        self.update_size()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
    
    def update_size(self):
        old_bottom = self.rect.bottom if hasattr(self, 'rect') else None
        old_x = self.rect.x if hasattr(self, 'rect') else None
        
        global is_fire_mario
        if is_fire_mario:
            self.base_image = pygame.transform.scale(MARIO[13].copy(), (GRID_SIZE, GRID_SIZE * 2))
        elif self.is_big:
            self.base_image = pygame.transform.scale(MARIO[0].copy(), (GRID_SIZE, GRID_SIZE * 2))
        else:
            self.base_image = pygame.transform.scale(MARIO[7].copy(), (GRID_SIZE, GRID_SIZE))
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        if old_bottom and old_x is not None:
            self.rect.bottom = old_bottom
            self.rect.x = old_x
    
    def get_current_image(self):
        global is_fire_mario
        
        if self.is_dead:
            return 6
        
        if self.is_crouching and self.on_ground:
            if is_fire_mario:
                return 19
            elif self.is_big:
                return 20
        
        if self.on_flag or self.waiting_for_flag:
            return 14 if is_fire_mario else (2 if self.is_big else 9)
        
        if self.walking_to_castle:
            if is_fire_mario:
                run_frames = [14, 15, 16]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
            elif self.is_big:
                run_frames = [2, 3, 4]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
            else:
                run_frames = [9, 10, 11]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
        
        if is_fire_mario:
            if not self.on_ground:
                return 17
            elif self.vel_x == 0:
                return 13
            elif (self.vel_x > 0 and not self.facing_right) or (self.vel_x < 0 and self.facing_right):
                return 18
            else:
                run_frames = [14, 15, 16]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
        elif self.is_big:
            if not self.on_ground:
                return 1
            elif self.vel_x == 0:
                return 0
            elif (self.vel_x > 0 and not self.facing_right) or (self.vel_x < 0 and self.facing_right):
                return 5
            else:
                run_frames = [2, 3, 4]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]
        else:
            if not self.on_ground:
                return 8
            elif self.vel_x == 0:
                return 7
            elif (self.vel_x > 0 and not self.facing_right) or (self.vel_x < 0 and self.facing_right):
                return 12
            else:
                run_frames = [9, 10, 11]
                frame_index = (self.animation_frame // self.run_frame_duration) % 3
                return run_frames[frame_index]

    def grow(self):
        global growing_timer, points
        if not self.is_big:
            self.is_big = True
            growing_timer = FPS
            self.update_size()  
            points += 1000
            add_score_popup(self.rect.x, self.rect.y, 1000)
            powerup_sound.play()

    def die(self):
        """被敵人殺死"""
        global live, respawn_timer, game_over, death_sound_playing, death_sound_timer, death_sound, game_sound_channel, star_sound_channel, hurry_sound_channel
        if not self.is_dead:
            # 停止背景音樂
            if game_sound_channel:
                game_sound_channel.stop()
            if star_sound_channel:
                star_sound_channel.stop()
            if hurry_sound_channel:
                hurry_sound_channel.stop()
            
            if live > 0:
                live -= 1
                self.is_dead = True
                self.death_jump_done = False
                self.vel_x = 0
                self.vel_y = -10
                self.update_image_direction()
    
    def shrink(self):
        global is_fire_mario, big_to_small_timer, fire_to_big_timer
        if is_fire_mario:
            fire_to_big_timer = FPS
            self.invincible = True
            self.invincible_timer = 120
            pipe_sound.play()
        elif self.is_big:
            big_to_small_timer = FPS
            self.invincible = True
            self.invincible_timer = 120
            pipe_sound.play()

    def shoot_fireball(self):
        global is_fire_mario
        if not is_fire_mario or self.is_dead or self.on_flag or self.waiting_for_flag or self.walking_to_castle:
            return
        
        if len(fireballs) >= 4:
            return
        
        fireball_x = self.rect.right - GRID_SIZE // 4 if self.facing_right else self.rect.left - GRID_SIZE // 8
        fireball_y = self.rect.centery
        fireball = Fireball(fireball_x, fireball_y, self.facing_right)
        fireballs.add(fireball)
        all_sprites.add(fireball)
        fireball_sound.play()
        
        self.shooting_timer = FPS // 4  # 顯示射擊圖片15幀

    def update(self):
        global game_won, game_over, reset_timer, growing_timer, transforming_timer, fire_to_big_timer, big_to_small_timer, camera_x, checkpoint_x, checkpoint_activated, initial_player_x, initial_player_y, live, respawn_timer, calculating_score, score_calculation_timer, target_points, start_points, start_coins, start_time, points, death_sound_playing, death_sound_timer, death_sound, game_sound_channel, star_sound_channel, hurry_sound_channel, is_fire_mario
        
        # 遞減射擊計時器
        if self.shooting_timer > 0:
            self.shooting_timer -= 1
        
        # 長大特效 (小馬力歐變大馬力歐)
        if growing_timer > 0:
            growing_timer -= 1
            if growing_timer % 10 == 0:
                self.is_big = not self.is_big
                self.update_size()
                self.update_image_direction()
            if growing_timer == 0:
                self.is_big = True
                self.update_size()
                self.update_image_direction()
            return False
        
        # 變身特效 (大馬力歐變火焰馬力歐)
        if transforming_timer > 0:
            transforming_timer -= 1
            if transforming_timer % 10 == 0:
                # 切換顯示大馬力歐和火焰馬力歐
                is_fire_mario = not is_fire_mario
                self.update_size()
                self.update_image_direction()
            if transforming_timer == 0:
                is_fire_mario = True
                self.update_size()
                self.update_image_direction()
            return False
        
        # 變身特效 (火焰馬力歐變大馬力歐)
        if fire_to_big_timer > 0:
            fire_to_big_timer -= 1
            if fire_to_big_timer % 10 == 0:
                # 切換顯示火焰馬力歐和大馬力歐
                is_fire_mario = not is_fire_mario
                self.update_size()
                self.update_image_direction()
            if fire_to_big_timer == 0:
                is_fire_mario = False
                self.is_big = True
                self.update_size()
                self.update_image_direction()
            return False
        
        # 縮小特效 (大馬力歐變小馬力歐)
        if big_to_small_timer > 0:
            big_to_small_timer -= 1
            if big_to_small_timer % 10 == 0:
                # 切換顯示大馬力歐和小馬力歐
                self.is_big = not self.is_big
                self.update_size()
                self.update_image_direction()
            if big_to_small_timer == 0:
                self.is_big = False
                self.update_size()
                self.update_image_direction()
            return False
        
        # 先檢測是否掉洞（在死亡動畫之前）
        if self.rect.top > SCREEN_HEIGHT and not self.is_dead:
            # 停止背景音樂
            if game_sound_channel:
                game_sound_channel.stop()
            if star_sound_channel:
                star_sound_channel.stop()
            if hurry_sound_channel:
                hurry_sound_channel.stop()
            
            # 掉下洞
            if live > 0:
                live -= 1
                if live > 0:
                    # 扣除生命後還有生命，等待死亡音效播放完畢後復活
                    self.is_dead = True
                    self.visible = False
                    death_sound_playing = True
                    death_sound.play()
                    death_sound_timer = int(death_sound.get_length() * FPS)
                    respawn_timer = death_sound_timer
                else:
                    # 扣除生命後沒有生命了
                    self.is_dead = True
                    self.visible = False
                    death_sound_playing = True
                    death_sound.play()
                    death_sound_timer = int(death_sound.get_length() * FPS)
            return False
        
        if self.is_dead:
            # 如果是被敵人殺死，播放死亡動畫
            if self.death_jump_done == False:
                self.vel_y += 0.8
                self.rect.y += self.vel_y
                
                if self.rect.top > SCREEN_HEIGHT:
                    # 馬力歐消失，播放死亡音效
                    if not death_sound_playing:
                        death_sound.play()
                        death_sound_playing = True
                        death_sound_timer = int(death_sound.get_length() * FPS)
                    
                    self.death_jump_done = True
                    self.visible = False
                    
                    if live > 0:
                        respawn_timer = death_sound_timer
                    else:
                        # 等待死亡音效播放完畢後才Game Over
                        pass
                
                return False
            
            return False
        
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
                        
                        self.facing_right = True
                        self.castle_walk_stage = -2
                        self.pause_timer = FPS // 2
                        
                        img_index = 13 if is_fire_mario else (0 if self.is_big else 7)
                        if self.is_big:
                            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
                        else:
                            base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
                        self.image = base_img
                        
                        self.walking_to_castle = True
                        for castle in castles:
                            self.castle_target_x = castle.rect.centerx
                            break
                        return False
            return False
        
        if self.walking_to_castle:
            if self.castle_walk_stage == -2:
                self.pause_timer -= 1
                
                if self.pause_timer <= 0:
                    self.rect.x += GRID_SIZE
                    
                    self.facing_right = False
                    img_index = 13 if is_fire_mario else (0 if self.is_big else 7)
                    if self.is_big:
                        base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
                    else:
                        base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
                    self.image = pygame.transform.flip(base_img, True, False)
                    
                    self.castle_walk_stage = -1
                    self.pause_timer = FPS // 2
                
                return False
            
            elif self.castle_walk_stage == -1:
                self.pause_timer -= 1
                
                if self.pause_timer <= 0:
                    self.facing_right = True
                    self.castle_walk_stage = 0
                
                return False
            
            elif self.castle_walk_stage == 0:
                # 只播放一次level_complete_sound
                if not hasattr(self, 'level_complete_played'):
                    level_complete_sound.play()
                
                self.vel_x = self.max_speed * self.castle_walk_ratio
                self.facing_right = True
                self.vel_y = 0
                self.rect.x += self.vel_x
                
                on_stair = False
                for stair in stairs:
                    if self.rect.colliderect(stair.rect):
                        self.rect.bottom = stair.rect.top
                        on_stair = True
                        break
                
                if not on_stair:
                    self.castle_walk_stage = 1
                
                return False
            
            elif self.castle_walk_stage == 1:
                self.vel_x = self.max_speed / 4
                self.facing_right = True
                
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
                            self.castle_walk_stage = 2
                            self.on_ground = True
                            break
                
                return False
            
            elif self.castle_walk_stage == 2:
                self.vel_x = self.max_speed / 4
                self.facing_right = True
                self.vel_y = 0
                self.rect.x += self.vel_x
                
                self.animation_frame += 1
                
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vel_y > 0 or self.rect.bottom > platform.rect.top:
                            self.rect.bottom = platform.rect.top
                            self.vel_y = 0
                
                self.update_image_direction()
                
                if self.rect.centerx >= self.castle_target_x:
                    self.visible = False
                    self.won = True
                    # 設置進入計算分數準備階段
                    calculating_score = True
                    score_calculation_timer = 0
                    start_points = points
                    start_coins = coins_collected
                    start_time = game_time
                    target_points = points + (coins_collected * 100) + (game_time * 20)
                
                return False
        
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        self.rect.x += self.vel_x
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_x > 0:
                    self.rect.right = stair.rect.left
                    self.vel_x = 0
                    if self.facing_right:
                        self.hit_wall = True
                elif self.vel_x < 0:
                    self.rect.left = stair.rect.right
                    self.vel_x = 0
                    if not self.facing_right:
                        self.hit_wall = True
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
                    if self.facing_right:
                        self.hit_wall = True
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.vel_x = 0
                    if not self.facing_right:
                        self.hit_wall = True
                    
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_x > 0:
                    self.rect.right = pipe.rect.left
                    self.vel_x = 0
                    if self.facing_right:
                        self.hit_wall = True
                elif self.vel_x < 0:
                    self.rect.left = pipe.rect.right
                    self.vel_x = 0
                    if not self.facing_right:
                        self.hit_wall = True
                    
        for pipe_top in pipe_tops:
            if self.rect.colliderect(pipe_top.rect):
                if self.vel_x > 0:
                    self.rect.right = pipe_top.rect.left
                    self.vel_x = 0
                    if self.facing_right:
                        self.hit_wall = True
                elif self.vel_x < 0:
                    self.rect.left = pipe_top.rect.right
                    self.vel_x = 0
                    if not self.facing_right:
                        self.hit_wall = True
        
        self.rect.y += self.vel_y
        
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

        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_y > 0:
                    self.rect.bottom = pipe.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = pipe.rect.bottom
                    self.vel_y = 0

        for pipe_top in pipe_tops:
            if self.rect.colliderect(pipe_top.rect):
                if self.vel_y > 0:
                    self.rect.bottom = pipe_top.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = pipe_top.rect.bottom
                    self.vel_y = 0
                    
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.vel_y > 0 and self.rect.bottom - brick.rect.top < 20:
                    self.rect.bottom = brick.rect.top
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.vel_x > 0 and self.rect.right - brick.rect.left < 20:
                    self.rect.right = brick.rect.left
                elif self.vel_x < 0 and brick.rect.right - self.rect.left < 20:
                    self.rect.left = brick.rect.right
                elif self.vel_y < 0 and brick.rect.bottom - self.rect.top < 20:
                    self.rect.top = brick.rect.bottom
                    self.vel_y = 0
                    brick.bump()
                    if self.is_big and not brick.is_breaking:
                        brick.break_brick()
                        smash_sound.play()
                    else:
                        stomp_sound.play()
                        
        for secret_brick in secret_bricks:
            if self.rect.colliderect(secret_brick.rect):
                # 生命菇磚塊（隱藏狀態）只能從下方碰撞
                if secret_brick.brick_type == 1 and not secret_brick.is_visible:
                    # 只處理從下方撞擊
                    if self.vel_y < 0 and secret_brick.rect.bottom - self.rect.top < 20:
                        self.rect.top = secret_brick.rect.bottom
                        self.vel_y = 0
                        secret_brick.bump()
                    # 其他方向不碰撞，馬力歐可以穿越
                else:
                    # 其他秘密磚塊或已顯示的生命菇磚塊，正常碰撞
                    if self.vel_y > 0 and self.rect.bottom - secret_brick.rect.top < 20:
                        self.rect.bottom = secret_brick.rect.top
                        self.vel_y = 0
                        self.jumping = False
                        self.on_ground = True
                    elif self.vel_x > 0 and self.rect.right - secret_brick.rect.left < 20:
                        self.rect.right = secret_brick.rect.left
                    elif self.vel_x < 0 and secret_brick.rect.right - self.rect.left < 20:
                        self.rect.left = secret_brick.rect.right
                    elif self.vel_y < 0 and secret_brick.rect.bottom - self.rect.top < 20:
                        self.rect.top = secret_brick.rect.bottom
                        self.vel_y = 0
                        secret_brick.bump()
                    
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0 and self.rect.bottom - qblock.rect.top < 15:
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
                    
        # for pipe in pipes:
        #     if self.rect.colliderect(pipe.rect):
        #         if self.vel_y > 0 and self.rect.bottom - pipe.rect.top < 20:
        #             self.rect.bottom = pipe.rect.top
        #             self.vel_y = 0
        #             self.jumping = False
        #             self.on_ground = True
        #         elif self.vel_x > 0 and self.rect.right - pipe.rect.left < 20:
        #             self.rect.right = pipe.rect.left
        #             self.vel_x = 0
        #             self.hit_wall = True
        #         elif self.vel_x < 0 and pipe.rect.right - self.rect.left < 20:
        #             self.rect.left = pipe.rect.right
        #             self.vel_x = 0
        #             self.hit_wall = True
        
        # for pipe_top in pipe_tops:
        #     if self.rect.colliderect(pipe_top.rect):
        #         if self.vel_y > 0 and self.rect.bottom - pipe_top.rect.top < 20:
        #             self.rect.bottom = pipe_top.rect.top
        #             self.vel_y = 0
        #             self.jumping = False
        #             self.on_ground = True
        #         elif self.vel_x > 0 and self.rect.right - pipe_top.rect.left < 20:
        #             self.rect.right = pipe_top.rect.left
        #         elif self.vel_x < 0 and pipe_top.rect.right - self.rect.left < 20:
        #             self.rect.left = pipe_top.rect.right
        
        for flagpole in flagpoles:
            if self.rect.colliderect(flagpole.rect):
                self.rect.x += GRID_SIZE // 2
                self.waiting_for_flag = True
                height_score = int((SCREEN_HEIGHT - self.rect.y) / GRID_SIZE) * 100
                points += height_score
                add_score_popup(self.rect.x, self.rect.y, height_score)
                
                # 停止所有背景音樂，播放旗桿音效
                if game_sound_channel:
                    game_sound_channel.stop()
                if star_sound_channel:
                    star_sound_channel.stop()
                # 停止hurry_sound
                if hurry_sound_channel:
                    hurry_sound_channel.stop()
                
                flagpole_sound.play()
                
                for flag_img in flag_images:
                    flag_img.start_descending(self.rect.y)
                
                break
        
        if self.rect.left < self.min_x:
            self.rect.left = self.min_x
            if self.vel_x < 0:
                self.vel_x = 0
                if not self.facing_right:
                    self.hit_wall = True
        
        self.update_image_direction()
        
        return False

    def update_image_direction(self):
        global is_fire_mario
        img_index = self.get_current_image()
        
        old_bottom = self.rect.bottom
        old_x = self.rect.x
        
        if self.shooting_timer > 0 and is_fire_mario:
            base_img = pygame.transform.scale(MARIO[14].copy(), (GRID_SIZE, GRID_SIZE * 2))
            if self.facing_right:
                self.image = base_img
            else:
                self.image = pygame.transform.flip(base_img, True, False)
            
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.x = old_x
            return
    
        if self.is_crouching and self.on_ground:
            if is_fire_mario or self.is_big:
                base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 1.25))
            else:
                base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
        else:
            if is_fire_mario:
                base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
            elif self.is_big:
                base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE * 2))
            else:
                base_img = pygame.transform.scale(MARIO[img_index].copy(), (GRID_SIZE, GRID_SIZE))
        
        if self.facing_right:
            self.image = base_img
        else:
            self.image = pygame.transform.flip(base_img, True, False)
        
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.x = old_x
    
        if self.vel_x != 0 and self.on_ground:
            self.animation_frame += 1
        else:
            self.animation_frame = 0
    
    def jump(self):
        if self.on_flag or self.waiting_for_flag:
            return
        if not self.jumping and self.on_ground:
            self.vel_y = -18
            self.jumping = True
            jump_sound.play()

class Ground(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = BLOCK[0]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Stair(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = BLOCK[1]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Brick(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = BRICK[0]
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
        
    def check_enemies_above(self):
        check_rect = pygame.Rect(self.rect.x, self.rect.y - GRID_SIZE, self.rect.width, GRID_SIZE)
        
        for enemy in enemies:
            if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                continue
            if hasattr(enemy, 'is_dying') and enemy.is_dying:
                continue
            
            if enemy.rect.colliderect(check_rect):
                if hasattr(enemy, 'die_from_shell'):
                    global points
                    enemy.die_from_shell()
                    points += 100
                    add_score_popup(self.rect.x, self.rect.y, 100)
        
    def bump(self):
        if not self.is_bumping and not self.is_breaking:
            self.is_bumping = True
            self.bump_timer = 15
            self.check_enemies_above()
    
    def break_brick(self):
        global points
        points += 50
        self.check_enemies_above()
        
        for i in range(4):
            particle = {
                'x': self.rect.x + (i % 2) * GRID_SIZE // 2,
                'y': self.rect.y + (i // 2) * GRID_SIZE // 2,
                'vel_x': random.uniform(-3, 3),
                'vel_y': random.uniform(-8, -4),
                'size': GRID_SIZE // 4,
                'life': 30
            }
            brick_particles.append(particle)
        
        self.kill()
            
    def update(self):
        if self.is_bumping:
            if self.bump_timer > 7:
                progress = (15 - self.bump_timer) / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            else:
                progress = self.bump_timer / 7
                self.rect.y = self.original_y - (GRID_SIZE // 2) * progress
            
            self.bump_timer -= 1
            if self.bump_timer <= 0:
                self.is_bumping = False
                self.rect.y = self.original_y

class SecretBrick(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, brick_type):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.brick_type = brick_type  # 1=生命菇, 2=5次金幣, 3=星星
        self.hit_count = 0
        self.max_hits = 5 if brick_type == 2 else 1
        self.is_empty = False  # 是否已經空了
        self.is_visible = False  # 是否可見（生命菇磚塊初始不可見）
        
        # 生命菇磚塊初始不可見，其他類型可見
        if brick_type == 1:
            self.is_visible = False
            self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
            self.image.set_alpha(0)  # 完全透明
        else:
            self.is_visible = True
            self.image = BRICK[0]
            self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.original_y = grid_y * GRID_SIZE
        self.bump_timer = 0
        self.is_bumping = False
        
    def check_enemies_above(self):
        check_rect = pygame.Rect(self.rect.x, self.rect.y - GRID_SIZE, self.rect.width, GRID_SIZE)
        
        for enemy in enemies:
            if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                continue
            if hasattr(enemy, 'is_dying') and enemy.is_dying:
                continue
            
            if enemy.rect.colliderect(check_rect):
                if hasattr(enemy, 'die_from_shell'):
                    global points
                    enemy.die_from_shell()
                    points += 100
                    add_score_popup(self.rect.x, self.rect.y, 100)
        
    def bump(self):
        global coins_collected, points
        # 如果已經空了，播放撞擊空磚塊音效但不彈跳
        if self.is_empty:
            bump_sound.play()
            return
            
        if self.is_bumping or self.hit_count >= self.max_hits:
            return
        
        # 第一次撞擊時，如果是隱藏的生命菇磚塊，顯示出來
        if not self.is_visible and self.brick_type == 1:
            self.is_visible = True
            self.image = BRICK[0]
            self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
            
        self.is_bumping = True
        self.bump_timer = 15
        self.hit_count += 1
        
        self.check_enemies_above()
        
        if self.brick_type == 1:  # 生命菇
            mushroom = OneUpMushroom(self.rect.x, self.rect.y - GRID_SIZE // 2)
            all_sprites.add(mushroom)
            powerups.add(mushroom)
            # 變成空磚塊
            self.is_empty = True
            self.image = BLOCK[3]
            self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
            appear_sound.play()
        elif self.brick_type == 2:  # 金幣
            coin = Coin(self.rect.x, self.rect.y - GRID_SIZE)
            all_sprites.add(coin)
            coins.add(coin)
            coin_sound.play()
            coins_collected += 1
            points += 200
            stomp_sound.play()
            # 五次後變成空磚塊
            if self.hit_count >= 5:
                self.is_empty = True
                self.image = BLOCK[3]
                self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        elif self.brick_type == 3:  # 星星
            star = Star(self.rect.x, self.rect.y - GRID_SIZE // 2)
            all_sprites.add(star)
            powerups.add(star)
            appear_sound.play()
            # 變成空磚塊
            self.is_empty = True
            self.image = BLOCK[3]
            self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
    
    def update(self):
        if self.is_bumping:
            if self.bump_timer > 7:
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
    for particle in brick_particles[:]:
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
    for particle in brick_particles[:]:
        particle['vel_y'] += 0.5
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
            self.image = BLOCK[2]
        else:
            self.image = BLOCK[3]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
    
    def reset(self):
        self.hit_count = 0
        self.create_image()
    
    def check_enemies_above(self):
        check_rect = pygame.Rect(self.rect.x, self.rect.y - GRID_SIZE, self.rect.width, GRID_SIZE)
        
        for enemy in enemies:
            if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                continue
            if hasattr(enemy, 'is_dying') and enemy.is_dying:
                continue
            
            if enemy.rect.colliderect(check_rect):
                if hasattr(enemy, 'die_from_shell'):
                    global points
                    enemy.die_from_shell()
                    points += 100
                    add_score_popup(self.rect.x, self.rect.y, 100)
        
    def hit(self):
        if self.hit_count == 0:
            self.is_bumping = True
            self.bump_timer = 15
            
            self.check_enemies_above()
            
            if self.item_type == 'mushroom':
                mushroom = Mushroom(self.rect.x, self.rect.y - GRID_SIZE // 2)
                all_sprites.add(mushroom)
                powerups.add(mushroom)
                appear_sound.play()

            elif self.item_type == 'sunflower':
                appear_sound.play()
                
            else:
                global coins_collected
                coin = Coin(self.rect.x, self.rect.y - GRID_SIZE)
                all_sprites.add(coin)
                coins.add(coin)
                coins_collected += 1
                coin_sound.play()
            
            self.hit_count += 1
            self.create_image()
        else:
            # 已經是空磚塊，播放撞擊音效
            bump_sound.play()
                
    def update(self):
        if self.is_bumping:
            if self.bump_timer > 7:
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
        self.image = COIN[0]
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
            points += 200
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
        if not player.is_big:
            self.base_image = MASHROOM[0]
            self.is_mushroom = True
        else:
            self.base_image = SUNFLOWER[0]
            self.is_mushroom = False
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = player.max_speed * player.mushroom_speed_ratio
        self.vel_y = 0
        self.rising = True
        self.rise_timer = FPS
        self.start_y = y
        self.z_order = -1  # 上升時在磚塊後面
        
    def update(self):
        if self.rising:
            self.rise_timer -= 1
            progress = (FPS - self.rise_timer) / FPS
            self.rect.y = self.start_y - (GRID_SIZE // 2) * progress
            if self.rise_timer <= 0:
                self.rising = False
                self.z_order = 1  # 上升完成後移到磚塊前面
            return
        
        if self.is_mushroom:
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
                elif self.vel_x > 0:
                    self.rect.right = brick.rect.left
                    self.vel_x *= -1
                else:
                    self.rect.left = brick.rect.right
                    self.vel_x *= -1
                    
        
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0 and self.rect.bottom - qblock.rect.top < 20:
                    self.rect.bottom = qblock.rect.top
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.rect.right = qblock.rect.left
                    self.vel_x *= -1
                else:
                    self.rect.left = qblock.rect.right
                    self.vel_x *= -1
        
        for secret_brick in secret_bricks:
            if secret_brick.is_empty and self.rect.colliderect(secret_brick.rect):
                if self.vel_y > 0 and self.rect.bottom - secret_brick.rect.top < 20:
                    self.rect.bottom = secret_brick.rect.top
                    self.vel_y = 0  # 或者 self.bounce_power（針對Star）
                else:
                    if self.vel_x > 0:
                        self.rect.right = secret_brick.rect.left
                    else:
                        self.rect.left = secret_brick.rect.right
                    self.vel_x *= -1
                    
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                self.vel_x *= -1

        if self.rect.colliderect(player.rect):
            global is_fire_mario, transforming_timer, points
            if not player.is_big:
                player.grow()
            else:
                is_fire_mario = False
                transforming_timer = FPS
                points += 1000
                add_score_popup(self.rect.x, self.rect.y, 1000)
                powerup_sound.play()
            self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.base_image = FIREBALL[0]
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE // 2, GRID_SIZE // 2))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 8 if facing_right else -8
        self.vel_y = 0
        # self.start_x = x
        self.gravity = 0.8
        self.bounce_power = -8
        
    def update(self):
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # if abs(self.rect.x - self.start_x) > 15 * GRID_SIZE:
        #     self.kill()
        #     return
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0 and self.rect.bottom - stair.rect.top < 20:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.vel_y > 0:
                    self.rect.bottom = brick.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for qblock in question_blocks:
            if self.rect.colliderect(qblock.rect):
                if self.vel_y > 0:
                    self.rect.bottom = qblock.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for secret_brick in secret_bricks:
            if secret_brick.is_visible and self.rect.colliderect(secret_brick.rect):
                if self.vel_y > 0:
                    self.rect.bottom = secret_brick.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                self.kill()
                return
        
        for pipe_top in pipe_tops:
            if self.rect.colliderect(pipe_top.rect):
                if self.vel_y > 0:
                    self.rect.bottom = pipe_top.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.kill()
                    return
        
        for enemy in enemies:
            if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                continue
            if hasattr(enemy, 'is_dying') and enemy.is_dying:
                continue
            
            if self.rect.colliderect(enemy.rect):
                global points

                if isinstance(enemy, Koopa):
                    if enemy.state == 'shell_moving':
                        enemy.state = 'shell'
                        enemy.vel_x = 0
                    enemy.die_from_star()
                else:
                    enemy.die_from_star()
                
                points += 100
                add_score_popup(enemy.rect.x, enemy.rect.y, 100)
                kick_sound.play()
                self.kill()
                return
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class OneUpMushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = MASHROOM[1]
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = player.max_speed * player.mushroom_speed_ratio
        self.vel_y = 0
        self.rising = True
        self.rise_timer = FPS
        self.start_y = y
        self.z_order = -1  # 上升時在磚塊後面
        
    def update(self):
        if self.rising:
            self.rise_timer -= 1
            progress = (FPS - self.rise_timer) / FPS
            self.rect.y = self.start_y - (GRID_SIZE // 2) * progress
            if self.rise_timer <= 0:
                self.rising = False
                self.z_order = 1  # 上升完成後移到磚塊前面
            return
        
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
        
        for secret_brick in secret_bricks:
            if secret_brick.is_empty and self.rect.colliderect(secret_brick.rect):
                if self.vel_y > 0 and self.rect.bottom - secret_brick.rect.top < 20:
                    self.rect.bottom = secret_brick.rect.top
                    self.vel_y = 0  # 或者 self.bounce_power（針對Star）
                else:
                    if self.vel_x > 0:
                        self.rect.right = secret_brick.rect.left
                    else:
                        self.rect.left = secret_brick.rect.right
                    self.vel_x *= -1
                    
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                self.vel_x *= -1

        if self.rect.colliderect(player.rect):
            global live
            live += 1
            plus_live_sound.play()
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = STAR[0]
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = player.max_speed * player.star_speed_ratio
        self.vel_y = 0
        self.rising = True
        self.rise_timer = FPS
        self.start_y = y
        self.bounce_power = -11
        self.z_order = -1  # 上升時在磚塊後面
        
    def update(self):
        if self.rising:
            self.rise_timer -= 1
            progress = (FPS - self.rise_timer) / FPS
            self.rect.y = self.start_y - (GRID_SIZE // 2) * progress
            if self.rise_timer <= 0:
                self.rising = False
                self.z_order = 1  # 上升完成後移到磚塊前面
            return
        
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
            
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = self.bounce_power
        
        for stair in stairs:
            if self.rect.colliderect(stair.rect):
                if self.vel_y > 0 and self.rect.bottom - stair.rect.top < 20:
                    self.rect.bottom = stair.rect.top
                    self.vel_y = self.bounce_power
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
                    self.vel_y = self.bounce_power
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
                    self.vel_y = self.bounce_power
                else:
                    if self.vel_x > 0:
                        self.rect.right = qblock.rect.left
                    else:
                        self.rect.left = qblock.rect.right
                    self.vel_x *= -1

        for secret_brick in secret_bricks:
            if secret_brick.is_empty and self.rect.colliderect(secret_brick.rect):
                if self.vel_y > 0 and self.rect.bottom - secret_brick.rect.top < 20:
                    self.rect.bottom = secret_brick.rect.top
                    self.vel_y = 0  # 或者 self.bounce_power（針對Star）
                else:
                    if self.vel_x > 0:
                        self.rect.right = secret_brick.rect.left
                    else:
                        self.rect.left = secret_brick.rect.right
                    self.vel_x *= -1
                    
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.vel_y > 0 and self.rect.bottom - pipe.rect.top < 20:
                    self.rect.bottom = pipe.rect.top
                    self.vel_y = self.bounce_power
                else:
                    self.vel_x *= -1
        
        if self.rect.colliderect(player.rect):
            global invincible_star_timer, star_music_playing, game_sound_channel, star_sound_channel, game_muted
            invincible_star_timer = FPS * 10
            
            # 停止背景音樂，播放星星音樂
            if game_sound_channel:
                game_sound_channel.pause()  # 暫停背景音樂
            
            # 只有在非靜音狀態下才播放星星音樂
            if not game_muted:
                star_sound_channel = star_sound.play(-1)  # 循環播放
            else:
                star_sound_channel = star_sound.play(-1)
                star_sound_channel.pause()  # 立即暫停
            star_music_playing = True
            
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.base_image = GOOMBA[0]
        self.base_image = pygame.transform.scale(self.base_image, (GRID_SIZE, GRID_SIZE))
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE
        self.start_x = grid_x * GRID_SIZE
        self.start_y = grid_y * GRID_SIZE
        self.vel_x = -player.max_speed * player.enemy_speed_ratio
        self.vel_y = 0
        self.is_squashed = False
        self.squash_timer = 0
        self.is_dying = False
        self.death_rotation = 0
        self.flip_timer = 0
        self.is_flipped = False
        
    def die_from_shell(self):
        self.is_dying = True
        self.vel_x = 0
        self.vel_y = -10
        self.death_rotation = 0
        
    def die_from_star(self):
        global points
        self.is_dying = True
        self.vel_x = 0
        self.vel_y = -10
        self.death_rotation = 0
        points += 100
        add_score_popup(self.rect.x, self.rect.y, 100)
        kick_sound.play()
        
    def squash(self):
        global points
        self.is_squashed = True
        self.squash_timer = 30
        self.vel_x = 0
        self.vel_y = 0
        points += 100
        add_score_popup(self.rect.x, self.rect.y, 100)
        old_bottom = self.rect.bottom
        old_x = self.rect.x
        self.image = GOOMBA[1]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE//3))
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.x = old_x
        kick_sound.play()
        
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vel_x = -player.max_speed * player.enemy_speed_ratio
        self.vel_y = 0
        self.is_squashed = False
        self.squash_timer = 0
        self.image = GOOMBA[0]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        
    def update(self):
        if self.is_dying:
            self.vel_y += 0.8
            self.rect.y += self.vel_y
            self.death_rotation += 6
            
            original_img = GOOMBA[0]
            original_img = pygame.transform.scale(original_img, (GRID_SIZE, GRID_SIZE))
            
            rotation = min(self.death_rotation, 180)
            self.image = pygame.transform.rotate(original_img, rotation)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            return
        
        if self.is_squashed:
            self.squash_timer -= 1
            if self.squash_timer <= 0:
                self.kill()
            return
        
        self.flip_timer += 1
        if self.flip_timer >= FPS // 3:
            self.flip_timer = 0
            self.is_flipped = not self.is_flipped
            
            old_rect = self.rect.copy()
            if self.is_flipped:
                self.image = pygame.transform.flip(self.base_image, True, False)
            else:
                self.image = self.base_image.copy()
            self.rect = self.image.get_rect()
            self.rect.topleft = old_rect.topleft
        
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
        
        for other_enemy in enemies:
            if other_enemy != self and not self.is_squashed:
                if self.rect.colliderect(other_enemy.rect):
                    if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                        continue
                    if hasattr(other_enemy, 'is_dying') and other_enemy.is_dying:
                        continue
                    if isinstance(other_enemy, Koopa) and other_enemy.state in ['shell', 'shell_moving']:
                        continue
                    if self.vel_x > 0:
                        self.rect.right = other_enemy.rect.left
                    else:
                        self.rect.left = other_enemy.rect.right
                    self.vel_x *= -1
                    if hasattr(other_enemy, 'vel_x'):
                        other_enemy.vel_x *= -1

class Koopa(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.state = 'walking'
        
        self.walk_images = [
            pygame.transform.scale(KOOPA[0].copy(), (GRID_SIZE, int(GRID_SIZE * 1.5))),
            pygame.transform.scale(KOOPA[1].copy(), (GRID_SIZE, int(GRID_SIZE * 1.5)))
        ]
        
        self.shell_image = KOOPA[2]
        self.shell_image = pygame.transform.scale(self.shell_image, (GRID_SIZE, GRID_SIZE))
        
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.bottom = (grid_y + 1) * GRID_SIZE  # 使用bottom來定位，確保底部在正確位置
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.vel_x = -player.max_speed * player.koopa_speed_ratio
        self.vel_y = 0
        self.spin_speed = player.max_speed * player.shell_speed_ratio
        self.animation_frame = 0
        self.walk_frame_duration = FPS // 3
        self.is_dying = False
        self.death_rotation = 0
        
    def die_from_star(self):
        global points
        self.is_dying = True
        self.vel_x = 0
        self.vel_y = -10
        self.death_rotation = 0
        points += 100
        add_score_popup(self.rect.x, self.rect.y, 100)
        kick_sound.play()
        
    def stomp(self):
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
            points += 100
            add_score_popup(self.rect.x, self.rect.y, 100)
            kick_sound.play()
    
    def kick(self, from_left):
        if self.state == 'shell' and self.vel_x == 0:
            self.state = 'shell_moving'
            if from_left:
                self.vel_x = self.spin_speed
            else:
                self.vel_x = -self.spin_speed
            kick_sound.play()
    
    def reset(self):
        self.state = 'walking'
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vel_x = -player.max_speed * player.koopa_speed_ratio
        self.vel_y = 0
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        
    def update(self):
        if self.is_dying:
            self.vel_y += 0.8
            self.rect.y += self.vel_y
            self.death_rotation += 6
            
            original_img = self.shell_image
            
            rotation = min(self.death_rotation, 180)
            self.image = pygame.transform.rotate(original_img, rotation)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            return
        
        if self.state == 'walking':
            self.animation_frame += 1
            frame_index = (self.animation_frame // self.walk_frame_duration) % 2
            base_image = self.walk_images[frame_index]
            
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
            for enemy in enemies:
                if enemy != self and self.rect.colliderect(enemy.rect):
                    if isinstance(enemy, Koopa):
                        if enemy.state == 'walking':
                            enemy.stomp()
                        elif enemy.state == 'shell_moving':
                            self.vel_x *= -1
                            enemy.vel_x *= -1
                    elif hasattr(enemy, 'squash'):
                        if not enemy.is_dying == True:
                            kick_sound.play()
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
        
        if self.state == 'walking':
            for other_enemy in enemies:
                if other_enemy != self:
                    if self.rect.colliderect(other_enemy.rect):
                        if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                            continue
                        if isinstance(other_enemy, Koopa) and other_enemy.state == 'shell_moving':
                            continue
                        if self.vel_x > 0:
                            self.rect.right = other_enemy.rect.left
                        else:
                            self.rect.left = other_enemy.rect.right
                        self.vel_x *= -1
                        if hasattr(other_enemy, 'vel_x'):
                            other_enemy.vel_x *= -1
        
        elif self.state in ['shell', 'shell_moving']:
            for other_enemy in enemies:
                if other_enemy != self:
                    if self.rect.colliderect(other_enemy.rect):
                        if hasattr(other_enemy, 'is_squashed') and other_enemy.is_squashed:
                            continue
                        if self.state == 'shell_moving':
                            continue
                        if hasattr(other_enemy, 'vel_x'):
                            if other_enemy.vel_x > 0:
                                other_enemy.rect.right = self.rect.left
                            else:
                                other_enemy.rect.left = self.rect.right
                            other_enemy.vel_x *= -1
        # 移動中的龜殼超出視窗左右5格時消失
        # if self.state == 'shell_moving':
        #     left_boundary = camera_x - 5 * GRID_SIZE
        #     right_boundary = camera_x + SCREEN_WIDTH + 5 * GRID_SIZE
            
        #     if self.rect.right < left_boundary or self.rect.left > right_boundary:
        #         self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, grid_height):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_height = grid_height
        width = GRID_SIZE * 2
        height = grid_height * GRID_SIZE
        self.image = PIPE[0]
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
        self.image = PIPE[1]
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class FlagPole(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        original_image = FLAG[0]
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
        self.descend_speed = 5
        
        self.image = FLAG[1]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
    
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = self.original_y
    
    def start_descending(self, player_y):
        self.is_descending = True
    
    def update(self):
        if self.is_descending:
            next_y = self.rect.y + self.descend_speed
            hit_stair = False
            
            for stair in stairs:
                if self.rect.left < stair.rect.right and self.rect.right > stair.rect.left:
                    if next_y + self.rect.height >= stair.rect.top and self.rect.y + self.rect.height <= stair.rect.top:
                        self.rect.y = stair.rect.top - self.rect.height
                        hit_stair = True
                        break
            
            if not hit_stair:
                self.rect.y += self.descend_speed

class Castle(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = CASTLE[0]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE * 5, GRID_SIZE * 4))
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * GRID_SIZE
        self.rect.y = grid_y * GRID_SIZE

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=0.3):
        super().__init__()
        self.image = CLOUD[0]
        self.image = pygame.transform.scale(self.image, (GRID_SIZE * 3, GRID_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * GRID_SIZE, 0, GRID_SIZE, SCREEN_HEIGHT)
        self.activated = False

def respawn_player():
    """復活馬力歐並重置敵人和磚塊"""
    global game_time, camera_x, respawn_timer, star_music_playing, game_sound_channel, is_fire_mario, growing_timer, transforming_timer, fire_to_big_timer, big_to_small_timer
    
    game_time = 400
    # 復活馬力歐
    player.is_dead = False
    player.death_jump_done = False
    player.is_big = False
    is_fire_mario = False
    player.update_size()
    player.visible = True
    player.facing_right = True
    
    # 根據是否經過檢查點決定復活位置
    if checkpoint_activated:
        player.rect.x = checkpoint_x
        player.rect.y = (GRID_HEIGHT - 3) * GRID_SIZE
        camera_x = max(0, checkpoint_x - SCREEN_WIDTH // 2)
        player.min_x = camera_x
    else:
        player.rect.x = initial_player_x
        player.rect.y = initial_player_y
        camera_x = 0
        player.min_x = 0
    
    player.vel_x = 0
    player.vel_y = 0
    
    # 重置所有敵人
    for enemy in list(enemies):
        enemy.kill()
    
    # 清空 all_sprites 中的敵人引用
    for sprite in list(all_sprites):
        if sprite in enemies:
            all_sprites.remove(sprite)
    
    # 重新生成初始視野內的敵人
    spawn_threshold = camera_x + SCREEN_WIDTH + 5 * GRID_SIZE
    for x, y, enemy_type in enemy_init_data:
        enemy_x_pos = x * GRID_SIZE
        if enemy_x_pos < spawn_threshold:
            if enemy_type == 'goomba':
                enemy = Enemy(x, y)
            else:
                enemy = Koopa(x, y)
            enemies.add(enemy)
            all_sprites.add(enemy)
    
    # 重置所有敵人生成標記
    for spawn_info in enemy_spawn_list:
        enemy_x_pos = spawn_info['x'] * GRID_SIZE
        # 如果在當前視野範圍內，標記為已生成
        if enemy_x_pos < spawn_threshold:
            spawn_info['spawned'] = True
        else:
            spawn_info['spawned'] = False
    
    # 重置所有磚塊
    for brick in list(bricks):
        brick.kill()
    
    for sprite in list(all_sprites):
        if sprite in bricks:
            all_sprites.remove(sprite)
    
    for x, y in brick_init_data:
        brick = Brick(x, y)
        bricks.add(brick)
        all_sprites.add(brick)
    
    # 重置秘密磚塊
    for secret_brick in secret_bricks:
        secret_brick.hit_count = 0
        secret_brick.is_empty = False
        if secret_brick.brick_type == 1:
            secret_brick.is_visible = False
            secret_brick.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
            secret_brick.image.set_alpha(0)
        else:
            secret_brick.is_visible = True
            secret_brick.image = BRICK[0]
            secret_brick.image = pygame.transform.scale(secret_brick.image, (GRID_SIZE, GRID_SIZE))
    
    # 重置問號磚
    for qblock in question_blocks:
        qblock.reset()
    
    # 清除所有道具
    for powerup in list(powerups):
        powerup.kill()
    
    for sprite in list(all_sprites):
        if sprite in powerups:
            all_sprites.remove(sprite)
    
    # 清除所有金幣
    for coin in list(coins):
        coin.kill()
    
    for sprite in list(all_sprites):
        if sprite in coins:
            all_sprites.remove(sprite)
    
    respawn_timer = 0
    
    # 復活後重新播放背景音樂
    star_music_playing = False
    if not game_muted:  # 只有在非靜音狀態下才播放
        game_sound_channel = game_sound.play(-1)
    else:
        game_sound_channel = game_sound.play(-1)
        game_sound_channel.pause()  # 立即暫停

def load_level(level_map):
    global player, initial_player_x, initial_player_y, brick_init_data, enemy_init_data
    
    all_sprites.empty()
    platforms.empty()
    stairs.empty()
    bricks.empty()
    secret_bricks.empty()
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
    checkpoints.empty()
    fireballs.empty()
    
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
                # 記錄初始位置
                initial_player_x = x * GRID_SIZE
                initial_player_y = y * GRID_SIZE
                
            elif char == 'B':
                brick = Brick(x, y)
                bricks.add(brick)
                all_sprites.add(brick)
                brick_data.append((x, y))
            
            elif char == '1':
                secret_brick = SecretBrick(x, y, 1)
                secret_bricks.add(secret_brick)
                all_sprites.add(secret_brick)
            
            elif char == '2':
                secret_brick = SecretBrick(x, y, 2)
                secret_bricks.add(secret_brick)
                all_sprites.add(secret_brick)
            
            elif char == '3':
                secret_brick = SecretBrick(x, y, 3)
                secret_bricks.add(secret_brick)
                all_sprites.add(secret_brick)
            
            elif char == 'A':
                checkpoint = Checkpoint(x, y)
                checkpoints.add(checkpoint)
                
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
                flag_img = FlagImage(x + 0.5, y)
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
    # 將初始數據設為全局變量，供復活時使用
    brick_init_data = brick_data
    enemy_init_data = enemy_data
    
    return brick_data, enemy_data, platform_data, len(level_map[0]), enemy_spawn_data

def draw_hud():
    font = pygame.font.Font(FONT, 20)
    
    score_text = font.render("SCORE", True, WHITE)
    screen.blit(score_text, (30, 10))
    score_count_text = font.render(f"{points:d}", True, WHITE)
    screen.blit(score_count_text, (45, 50))
    
    coins_text = font.render("COINS", True, WHITE)
    screen.blit(coins_text, (175, 10))
    coins_count_text = font.render(f"{coins_collected:d}", True, WHITE)
    screen.blit(coins_count_text, (190, 50))
    
    level_text = font.render("WORLD", True, WHITE)
    screen.blit(level_text, (350, 10))
    level_count_text = font.render("1—1", True, WHITE)
    screen.blit(level_count_text, (365, 50))
    
    time_text = font.render("TIME", True, WHITE)
    screen.blit(time_text, (500, 10))
    time_count_text = font.render(f"{max(0, game_time):d}", True, WHITE)
    screen.blit(time_count_text, (515, 50))
    
    live_text = font.render("LIVES", True, WHITE)
    screen.blit(live_text, (675, 10))
    live_count_text = font.render(f"{live:d}", True, WHITE)
    screen.blit(live_count_text, (690, 50))
    
    small_font = pygame.font.Font(FONT, 8)
    controls_text1 = small_font.render("Arrow Keys: Move | Space/Up: Jump | P: Pause | M: Mute", True, WHITE)
    screen.blit(controls_text1, (10, SCREEN_HEIGHT - 60))
    
    small_font = pygame.font.Font(FONT, 8)
    controls_text2 = small_font.render("R: Restart | Ctrl: Shooting | B: Show boxes", True, WHITE)
    screen.blit(controls_text2, (10, SCREEN_HEIGHT - 30))

def draw_win_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.Font(FONT, 36)
    font_medium = pygame.font.Font(FONT, 24)
    
    win_text = font_large.render("CONGRATULATIONS!", True, WHITE)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(win_text, win_rect)
    
    score_text = font_medium.render(f"Final Score: {points:d}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    restart_text = font_medium.render("Press R to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
    screen.blit(restart_text, restart_rect)

def draw_game_over_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.Font(FONT, 36)
    font_medium = pygame.font.Font(FONT, 24)
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = font_medium.render(f"Final Score: {points:d}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    restart_text = font_medium.render("Press R to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3))
    screen.blit(restart_text, restart_rect)

# 全局磚塊破碎粒子列表
brick_particles = []

# 全局初始數據
brick_init_data = []
enemy_init_data = []

# 創建精靈群組
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
stairs = pygame.sprite.Group()
bricks = pygame.sprite.Group()
secret_bricks = pygame.sprite.Group()
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
checkpoints = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

brick_init_data, enemy_init_data, platform_init_data, GRID_WIDTH, enemy_spawn_list = load_level(level_map)

game_over = False
reset_timer = 0
camera_x = 0
music_channel = None
current_music = None

# 開始播放遊戲音樂
game_sound_channel = game_sound.play(-1)
current_music = 'normal'

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
                if not game_paused:
                    # 暫停
                    game_paused = True
                    if game_sound_channel:
                        game_sound_channel.pause()
                    if star_sound_channel:
                        star_sound_channel.pause()
                    if hurry_sound_channel:
                        hurry_sound_channel.pause()
                    if not game_muted:
                        pause_sound.play()
                else:
                    # 解除暫停
                    game_paused = False

                    if not game_muted:
                        if star_music_playing and star_sound_channel:
                            star_sound_channel.unpause()
                        elif game_sound_channel:
                            game_sound_channel.unpause()
                        # 恢復hurry_sound（如果它正在播放中）
                        if hurry_sound_channel and 'hurry_sound_end_timer' in locals() and hurry_sound_end_timer > 0:
                            hurry_sound_channel.unpause()
            elif event.key == pygame.K_m:
                if not game_muted:
                    # 靜音 - 暫停所有背景音樂並將音效音量設為0
                    game_muted = True
                    
                    # 暫停背景音樂
                    if game_sound_channel:
                        game_sound_channel.pause()
                    if star_sound_channel:
                        star_sound_channel.pause()
                    if hurry_sound_channel:
                        hurry_sound_channel.pause()
                    
                    # 設置所有音效音量為0
                    jump_sound.set_volume(0)
                    long_jump_sound.set_volume(0)
                    coin_sound.set_volume(0)
                    powerup_sound.set_volume(0)
                    kick_sound.set_volume(0)
                    flagpole_sound.set_volume(0)
                    stomp_sound.set_volume(0)
                    bump_sound.set_volume(0)
                    smash_sound.set_volume(0)
                    level_complete_sound.set_volume(0)
                    death_sound.set_volume(0)
                    pause_sound.set_volume(0)
                    plus_live_sound.set_volume(0)
                    game_over_sound.set_volume(0)
                    appear_sound.set_volume(0)
                    fireball_sound.set_volume(0)
                    pipe_sound.set_volume(0)
                    
                else:
                    # 解除靜音 - 恢復背景音樂並將音效音量設為1
                    game_muted = False
                    
                    # 恢復背景音樂
                    if star_music_playing and star_sound_channel:
                        star_sound_channel.unpause()
                    elif game_sound_channel:
                        game_sound_channel.unpause()
                    
                    # 恢復hurry_sound（如果它正在播放中）
                    if hurry_sound_channel and 'hurry_sound_end_timer' in locals() and hurry_sound_end_timer > 0:
                        hurry_sound_channel.unpause()
                    
                    # 恢復所有音效音量為1
                    jump_sound.set_volume(1)
                    long_jump_sound.set_volume(1)
                    coin_sound.set_volume(1)
                    powerup_sound.set_volume(1)
                    kick_sound.set_volume(1)
                    flagpole_sound.set_volume(1)
                    stomp_sound.set_volume(1)
                    bump_sound.set_volume(1)
                    smash_sound.set_volume(1)
                    level_complete_sound.set_volume(1)
                    death_sound.set_volume(1)
                    pause_sound.set_volume(1)
                    plus_live_sound.set_volume(1)
                    game_over_sound.set_volume(1)
                    appear_sound.set_volume(1)
                    fireball_sound.set_volume(1)
                    pipe_sound.set_volume(1)
            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                if not game_over and not game_won and not game_paused:
                    player.shoot_fireball()
            elif event.key == pygame.K_r:
                # 重置遊戲
                brick_particles.clear()
                score_popups.clear()
                
                for fireball in list(fireballs):
                    fireball.kill()
                
                is_fire_mario = False
                growing_timer = 0
                transforming_timer = 0
                fire_to_big_timer = 0
                big_to_small_timer = 0
        
                brick_init_data, enemy_init_data, platform_init_data, GRID_WIDTH, enemy_spawn_list = load_level(level_map)
                game_over = False
                game_won = False
                camera_x = 0
                player.min_x = 0
                points = 0
                coins_collected = 0
                game_time = 400
                time_counter = 0
                live = 3
                checkpoint_x = 0
                checkpoint_activated = False
                invincible_star_timer = 0
                growing_timer = 0
                hurry_sound_played = False
                hurry_sound_end_timer = 0
                star_music_playing = False
                invincible_star_timer = 0
                calculating_score = False
                death_sound_playing = False
                game_over_sound_played = False
                
                # 停止所有音效
                if star_sound_channel:
                    star_sound_channel.stop()
                if hurry_sound_channel:
                    hurry_sound_channel.stop()
                if game_sound_channel:
                    game_sound_channel.stop()
                game_over_sound.stop()
                level_complete_sound.stop()
                death_sound.stop()
                kick_sound.stop()
                
                # 重新播放背景音樂（要檢查是否靜音）
                if not game_muted:  # 只有在非靜音狀態下才播放
                    game_sound_channel = game_sound.play(-1)
                else:
                    game_sound_channel = game_sound.play(-1)
                    game_sound_channel.pause()  # 立即暫停
                current_music = 'normal'
            elif event.key == pygame.K_b:
                show_hitboxes = not show_hitboxes
    
    if game_over:
        # 顯示 Game Over 畫面
        screen.fill(SKY_BLUE)
        
        for cloud in clouds:
            screen.blit(cloud.image, (cloud.rect.x - camera_x * cloud.speed, cloud.rect.y))
        
        for sprite in all_sprites:
            if sprite not in clouds and sprite != player:
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
        
        draw_brick_particles(screen, camera_x)
        
        draw_hud()
        draw_game_over_screen()
        
        # 播放一次 Game Over 音效
        if not game_over_sound_played:
            game_over_sound.play()
            game_over_sound_played = True
        
        pygame.display.flip()
        continue
        
    elif calculating_score:
        # 等待進入城堡
        if walking_to_castle is True:
            continue
        else:
            # 開始計算分數
            score_calculation_timer += 1
            
            # 計算金幣和時間各需要的時間
            coins_duration = (start_coins / 25) * FPS if start_coins > 0 else 0
            time_duration = (start_time / 100) * FPS if start_time > 0 else 0
            total_frames = coins_duration + time_duration  # 依序計算
            
            if total_frames == 0 or score_calculation_timer >= total_frames:
                # 計算完成
                points = target_points
                coins_collected = 0
                game_time = 0
                calculating_score = False
                game_won = True
            else:
                # 每10幀播放一次coin_sound
                # if score_calculation_timer % 10 == 0:
                #     coin_sound.play()
                # 先處理金幣(每25個金幣1秒)
                if score_calculation_timer <= coins_duration:
                    coins_progress = score_calculation_timer / coins_duration if coins_duration > 0 else 1
                    coins_collected = int(start_coins * (1 - coins_progress))
                    converted_coins = start_coins - coins_collected
                    coins_points = converted_coins * 100
                    time_points = 0
                    game_time = start_time
                # 再處理時間(每100秒1秒)
                else:
                    coins_collected = 0
                    coins_points = start_coins * 100
                    
                    time_elapsed = score_calculation_timer - coins_duration
                    time_progress = time_elapsed / time_duration if time_duration > 0 else 1
                    game_time = int(start_time * (1 - time_progress))
                    converted_time = start_time - game_time
                    time_points = converted_time * 20
                
                # 更新總分數
                points = start_points + coins_points + time_points
        
        # 繪製遊戲畫面
        screen.fill(SKY_BLUE)
        
        for cloud in clouds:
            screen.blit(cloud.image, (cloud.rect.x - camera_x * cloud.speed, cloud.rect.y))
        
        for powerup in powerups:
            if hasattr(powerup, 'z_order') and powerup.z_order == -1:
                screen.blit(powerup.image, (powerup.rect.x - camera_x, powerup.rect.y))
        
        for sprite in all_sprites:
            if sprite not in clouds and sprite != player and sprite not in powerups:
                if hasattr(sprite, 'is_visible') and not sprite.is_visible:
                    continue
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
        
        draw_brick_particles(screen, camera_x)
        
        for powerup in powerups:
            if not hasattr(powerup, 'z_order') or powerup.z_order == 1:
                screen.blit(powerup.image, (powerup.rect.x - camera_x, powerup.rect.y))
        
        for popup in score_popups:
            popup.draw(screen, camera_x)
        
        draw_hud()
        
        pygame.display.flip()
        continue
    
    elif not game_won and not game_paused:
        # 處理死亡音效計時器
        if death_sound_playing:
            death_sound_timer -= 1
            if death_sound_timer <= 0:
                death_sound_playing = False
                if live <= 0:
                    game_over = True
                else:
                   # 死亡音效播放完畢，立即復活
                    respawn_player()
        
        # 時間倒數
        if not player.is_dead and not player.on_flag and not player.waiting_for_flag and not player.walking_to_castle:
            time_counter += 1
            if time_counter >= (FPS//2):  # 每30幀減少1秒遊戲時間
                game_time -= 1
                time_counter = 0
                
                # 時間緊急音樂（只播放一次hurry_sound，然後繼續播放game_sound）
                if game_time == 100 and not hurry_sound_played and invincible_star_timer == 0:
                    if game_sound_channel:
                        game_sound_channel.pause()  # 暫停背景音樂
                    
                    # 只有在非靜音狀態下才播放緊急音效
                    if not game_muted:
                        hurry_sound_channel = hurry_sound.play()  # 播放一次緊急音效
                    hurry_sound_played = True
                    # 設置一個計時器，等hurry_sound播放完後恢復game_sound
                    hurry_sound_end_timer = int(hurry_sound.get_length() * FPS)
                
                if game_time <= 0:
                    player.die()
        
        # 處理hurry_sound播放完畢後恢復game_sound（移到 if not player.is_dead 外面）
        if 'hurry_sound_end_timer' in locals() and hurry_sound_end_timer > 0:
            hurry_sound_end_timer -= 1
            if hurry_sound_end_timer == 0:
                if invincible_star_timer == 0:  # 如果不在無敵狀態
                    if game_sound_channel and not game_muted:  # 檢查靜音狀態
                        game_sound_channel.unpause()  # 恢復背景音樂
        
        keys = pygame.key.get_pressed()

        player.update()
        
        vel_x_after_update = player.vel_x
        hit_wall_flag = player.hit_wall
        
        if not player.walking_to_castle and not player.on_flag and not player.waiting_for_flag and growing_timer == 0 and transforming_timer == 0 and fire_to_big_timer == 0 and big_to_small_timer == 0:
            if keys[pygame.K_DOWN] and player.on_ground and (player.is_big or is_fire_mario):
                player.is_crouching = True
                player.vel_x = 0
                player.hit_wall = False
            else:
                player.is_crouching = False
            
            if not player.is_crouching:
                if keys[pygame.K_LEFT]:
                    if hit_wall_flag and not player.facing_right and player.on_ground and player.vel_x == 0:
                        player.vel_x = 0
                    elif hit_wall_flag and player.facing_right and player.on_ground and player.vel_x == 0:
                        player.hit_wall = False
                    elif player.vel_x > 0:
                        player.vel_x -= player.deceleration * 2
                        if player.vel_x < 0:
                            player.vel_x = 0
                        player.hit_wall = False
                    else:
                        player.vel_x -= player.acceleration
                        if player.vel_x < -player.max_speed:
                            player.vel_x = -player.max_speed
                        player.hit_wall = False
                    player.facing_right = False
                    
                elif keys[pygame.K_RIGHT]:
                    if hit_wall_flag and player.facing_right and player.on_ground and player.vel_x == 0:
                        player.vel_x = 0
                    elif hit_wall_flag and not player.facing_right and player.on_ground and player.vel_x == 0:
                        player.hit_wall = False
                    elif player.vel_x < 0:
                        player.vel_x += player.deceleration * 2
                        if player.vel_x > 0:
                            player.vel_x = 0
                        player.hit_wall = False
                    else:
                        player.vel_x += player.acceleration
                        if player.vel_x > player.max_speed:
                            player.vel_x = player.max_speed
                        player.hit_wall = False
                    player.facing_right = True
                
                else:
                    player.hit_wall = False
                    if player.vel_x > 0:
                        player.vel_x -= player.deceleration
                        if player.vel_x < 0:
                            player.vel_x = 0
                    elif player.vel_x < 0:
                        player.vel_x += player.deceleration
                        if player.vel_x > 0:
                            player.vel_x = 0
        
        all_sprites.update()
        update_brick_particles()
        
        # 檢查點碰撞檢測
        if not checkpoint_activated:
            for checkpoint in checkpoints:
                if player.rect.colliderect(checkpoint.rect):
                    checkpoint_activated = True
                    checkpoint_x = checkpoint.rect.x
                    break
        
        # 處理無敵星星計時器
        if invincible_star_timer > 0:
            invincible_star_timer -= 1
            if invincible_star_timer == 0:
                # 無敵狀態結束
                star_music_playing = False
                if star_sound_channel:
                    star_sound_channel.stop()
                if game_sound_channel and not game_muted:
                    game_sound_channel.unpause()  # 恢復背景音樂
        
        # 更新分數彈出
        for popup in score_popups[:]:
            if not popup.update():
                score_popups.remove(popup)
        
        spawn_threshold = camera_x + SCREEN_WIDTH + 5*GRID_SIZE
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
        
        # 敵人碰撞檢測
        if not player.invincible and not player.is_dead and growing_timer == 0:
            stomped_goombas = []
            for enemy in enemies:
                if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                    continue
                if hasattr(enemy, 'is_dying') and enemy.is_dying:
                    continue
                
                if enemy.rect.colliderect(player.rect):
                    if isinstance(enemy, Enemy):
                        stomp_left = player.rect.left - GRID_SIZE
                        stomp_right = player.rect.right + GRID_SIZE
                        can_stomp = (player.vel_y >= 0 and 
                                   player.rect.bottom - enemy.rect.top < 30 and
                                   player.rect.bottom >= enemy.rect.top and
                                   player.rect.top < enemy.rect.top and
                                   stomp_right > enemy.rect.left and 
                                   stomp_left < enemy.rect.right)
                        
                        if can_stomp:
                            stomped_goombas.append(enemy)
            
            double_stomp_success = False
            if len(stomped_goombas) == 2:
                goomba1, goomba2 = stomped_goombas[0], stomped_goombas[1]
                distance = abs(goomba1.rect.centerx - goomba2.rect.centerx)
                
                if distance <= GRID_SIZE * 2:
                    for goomba in stomped_goombas:
                        goomba.is_squashed = True
                        goomba.squash_timer = 30
                        goomba.vel_x = 0
                        goomba.vel_y = 0
                        old_bottom = goomba.rect.bottom
                        old_x = goomba.rect.x
                        goomba.image = GOOMBA[1]
                        goomba.image = pygame.transform.scale(goomba.image, (GRID_SIZE, GRID_SIZE//3))
                        goomba.rect = goomba.image.get_rect()
                        goomba.rect.bottom = old_bottom
                        goomba.rect.x = old_x
                    
                    points += 10000
                    mid_x = (goomba1.rect.x + goomba2.rect.x) // 2
                    mid_y = min(goomba1.rect.y, goomba2.rect.y)
                    add_score_popup(mid_x, mid_y, 10000)
                    
                    player.vel_y = -10
                    kick_sound.play()
                    
                    double_stomp_success = True
            
            if not double_stomp_success:
                for enemy in enemies:
                    if hasattr(enemy, 'is_squashed') and enemy.is_squashed:
                        continue
                    if hasattr(enemy, 'is_dying') and enemy.is_dying:
                        continue
                    
                    if enemy.rect.colliderect(player.rect):
                        if invincible_star_timer > 0:
                            if isinstance(enemy, Koopa):
                                enemy.die_from_star()
                            else:
                                enemy.die_from_star()
                            continue
                        
                        # 烏龜特殊處理
                        if isinstance(enemy, Koopa):
                            stomp_left = player.rect.left - GRID_SIZE
                            stomp_right = player.rect.right + GRID_SIZE
                            can_stomp = (player.vel_y >= 0 and 
                                       player.rect.bottom - enemy.rect.top < 30 and
                                       player.rect.bottom >= enemy.rect.top and
                                       player.rect.top < enemy.rect.top and
                                       stomp_right > enemy.rect.left and 
                                       stomp_left < enemy.rect.right)
                            
                            if can_stomp and enemy.state == 'walking':
                                enemy.stomp()
                                player.vel_y = -10
                                continue
                            elif can_stomp and enemy.state == 'shell_moving':
                                shell_center = enemy.rect.centerx
                                player_center = player.rect.centerx
                                offset = abs(player_center - shell_center)
                                
                                if offset < GRID_SIZE // 4:
                                    enemy.state = 'shell'
                                    enemy.vel_x = 0
                                    player.vel_y = 0
                                else:
                                    enemy.state = 'shell'
                                    enemy.vel_x = 0
                                    player.vel_y = -10
                                continue
                            elif can_stomp and enemy.state == 'shell':
                                shell_center = enemy.rect.centerx
                                player_center = player.rect.centerx
                                offset = abs(player_center - shell_center)
    
                                if player_center < shell_center:
                                    enemy.kick(True)
                                    player.vel_y = -10
                                else:
                                    enemy.kick(False)
                                    player.vel_y = -10
                                continue
                            elif enemy.state == 'shell' and enemy.vel_x == 0:
                                from_left = player.rect.centerx < enemy.rect.centerx
                                enemy.kick(from_left)
                                continue
                            elif enemy.state == 'shell_moving':
                                if player.rect.centerx < enemy.rect.centerx:
                                    if enemy.vel_x > 0 and player.vel_x > 0:
                                        continue
                                else:
                                    if enemy.vel_x < 0 and player.vel_x < 0:
                                        continue
                                
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
                            elif enemy.state == 'walking':
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
                        # Goomba處理
                        elif hasattr(enemy, 'squash'):
                            stomp_left = player.rect.left - GRID_SIZE
                            stomp_right = player.rect.right + GRID_SIZE
                            can_stomp = (player.vel_y >= 0 and 
                                       player.rect.bottom - enemy.rect.top < 30 and
                                       player.rect.bottom >= enemy.rect.top and
                                       player.rect.top < enemy.rect.top and
                                       stomp_right > enemy.rect.left and 
                                       stomp_left < enemy.rect.right)
                            
                            if can_stomp:
                                enemy.squash()
                                player.vel_y = -10
                                continue
                            else:
                                if player.is_big:
                                    player.shrink()
                                else:
                                    player.die()
                                break
                            
    screen.fill(SKY_BLUE)

    for cloud in clouds:
        screen.blit(cloud.image, (cloud.rect.x - camera_x * cloud.speed, cloud.rect.y))
    
    # 先繪製在磚塊後面的道具（z_order = -1，正在上升的道具）
    for powerup in powerups:
        if hasattr(powerup, 'z_order') and powerup.z_order == -1:
            screen.blit(powerup.image, (powerup.rect.x - camera_x, powerup.rect.y))
    
    # 繪製平台、階梯、磚塊等（跳過隱藏的秘密磚塊）
    for sprite in all_sprites:
        if sprite not in clouds and sprite != player and sprite not in powerups:
            # 如果是秘密磚塊且不可見，跳過繪製
            if isinstance(sprite, SecretBrick) and not sprite.is_visible:
                continue
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
            
    if show_hitboxes:
        for sprite in all_sprites:
            if sprite not in clouds:
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
                debug_rect = pygame.Rect(sprite.rect.x - camera_x, sprite.rect.y, sprite.rect.width, sprite.rect.height)
                pygame.draw.rect(screen, RED, debug_rect, 2)
        
    # 繪製磚塊破碎粒子
    draw_brick_particles(screen, camera_x)
    
    # 繪製在磚塊前面的道具（z_order = 1，上升完成的道具）
    for powerup in powerups:
        if not hasattr(powerup, 'z_order') or powerup.z_order == 1:
            screen.blit(powerup.image, (powerup.rect.x - camera_x, powerup.rect.y))
    
    # 繪製分數彈出
    for popup in score_popups:
        popup.draw(screen, camera_x)
    
    # 最後繪製玩家
    if player.visible:
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
    
    draw_hud()
    
    if game_won:
        draw_win_screen()
    
    pygame.display.flip()

pygame.quit()
sys.exit()