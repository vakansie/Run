import pygame
import numpy as np
pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Squarey")
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x)
             for x in range(pygame.joystick.get_count())]
controller = joysticks[0]
controller.init()
print(controller.get_numaxes(),'asdasdaxis')
pygame.font.init()
font = pygame.font.SysFont('freesanbold.ttf', 50)

energy_dropped = []

class Player:
    def __init__(self, position, speed: int) -> None:
        self.position = np.array([position[0], position[1]], dtype=float)
        self.speed = speed
        self.energy = 100
        self.cooldown = 0
        self.colliders = []
        self.score = 0

    def move(self):
        x, y = round(controller.get_axis(0)), round(controller.get_axis(1))
        self.position += np.array([x, y], dtype=float) * self.speed
    
    def dash(self):
        if self.cooldown != 0: return
        if self.energy < 100: return
        x, y = round(controller.get_axis(2)), round(controller.get_axis(3))
        if x == 0 and y == 0: return
        self.position += np.array([x, y], dtype=float) * 100
        self.cooldown = 20
        self.energy -= 100

    def check_collisions(self):
        for energy in energy_dropped:
            if energy.rect.colliderect(self.rect):
                energy_dropped.remove(energy)
                self.energy += 100
                self.score += 100
                Energy_drop()
        if self.rect.colliderect(chaser.rect):
            self.score -= 1
    
    def check_win(self):
        return player.score > 499
    
    def check_loss(self):
        return player.score < -199
    
    def tik_cooldown(self):
        self.cooldown -= 1
        if self.cooldown < 0: self.cooldown = 0

class Chaser:
    def __init__(self, position, speed: int) -> None:
        self.position = np.array([position[0], position[1]], dtype=float)
        self.speed = speed

    def chase(self):
        dir_to_player = unify_vector(player.position - self.position)
        self.position += dir_to_player * self.speed

class Energy_drop:
    def __init__(self) -> None:
        self.position = (50 + round(np.random.random() * 1100), 50 + round(np.random.random() * 620))
        energy_dropped.append(self)

    def render(self):
        win.blit(self.image, (self.x,self.y))

def unify_vector(vector):
    if not np.any(vector):
        return vector
    return vector / (vector**2).sum()**0.5

def draw_game():
    win.fill((0, 0, 0))
    player.rect = pygame.draw.rect(win, (0, 0, 255), (int(
        player.position[0]), int(player.position[1]), 20, 20))
    chaser.rect = pygame.draw.rect(win, (255, 0, 0), (int(
        chaser.position[0]), int(chaser.position[1]), 40, 40))
    for energy_drop in energy_dropped:
        energy_drop.rect = pygame.draw.rect(win, (0, 128, 128), (int(
        energy_drop.position[0]), int(energy_drop.position[1]), 10, 10))
    score_text = font.render(f'{player.score}', True, (120, 200, 50))
    energy_text = font.render(f'{player.energy}', True, (0, 120, 120))
    score_rect = score_text.get_rect()
    energy_rect = energy_text.get_rect()
    score_rect.center = (1150, 50)
    energy_rect.center = (50, 50)
    win.blit(score_text, score_rect)
    win.blit(energy_text, energy_rect)
    pygame.display.update()

def draw_win():
    text = font.render('VICTORY!', True, (120, 200, 50))
    rect = text.get_rect()
    rect.center = (600, 360)
    win.blit(text, rect)
    pygame.display.update()

def draw_loss():
    text = font.render('DEFEAT!', True, (255, 50, 50))
    rect = text.get_rect()
    rect.center = (600, 360)
    win.blit(text, rect)
    pygame.display.update()

def run_game():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.time.delay(5)
        player.move()
        chaser.chase()
        player.dash()
        player.check_collisions()
        player.tik_cooldown()
        draw_game()
        if player.check_win():
            draw_win()
            run = False
            pygame.time.delay(5000)
        if player.check_loss():
            draw_loss()
            run = False
            pygame.time.delay(5000)

player = Player(position=(100, 100), speed=4)
chaser = Chaser(position=(300, 300), speed=4)
drop = Energy_drop()
draw_game()
run_game()