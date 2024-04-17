import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load("../graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser__cooldown = 600
        self.lasers = pygame.sprite.Group()

        self.laser__sound = pygame.mixer.Sound("../audio/laser.wav")
        self.laser__sound.set_volume(0.1)

        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    def get_input(self):
        # keyboard input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser__sound.play()
        
        # gamepad input
        if len(self.joysticks) > 0:
            print(self.joysticks[0].get_axis(0))
            if self.joysticks[0].get_axis(0) > 0.5:
                self.rect.x += self.speed
            if self.joysticks[0].get_axis(0) < -0.5:
                self.rect.x -= self.speed
            if self.joysticks[0].get_button(0) == 1 and self.ready:
                self.shoot_laser()
                self.ready = False
                self.laser_time = pygame.time.get_ticks()
                self.laser__sound.play()


    
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser__cooldown:
                self.ready = True
    
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, self.rect.bottom))
    
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()