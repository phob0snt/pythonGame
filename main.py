import pygame
import random


class Player:
    def __init__(self):
        self.birdDown = pygame.image.load('Assets/bird1.png')
        self.birdUp = pygame.image.load('Assets/bird2.png')
        self.sprite = self.birdDown
        self.posX = screen.get_width() / 4
        self.posY = screen.get_height() / 2
        self.rect = self.birdDown.get_rect()
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.velocity = 0

    def restart(self):
        self.posX = screen.get_width() / 4
        self.posY = screen.get_height() / 2
        self.velocity = 0

    def drawDown(self):
        self.posY += self.velocity
        self.sprite = self.birdDown
        self.rect = screen.blit(self.birdDown, (self.posX, self.posY))
        pass

    def drawUp(self):
        self.posY += self.velocity
        self.sprite = self.birdUp
        self.rect = screen.blit(self.birdUp, (self.posX, self.posY))
        pass

    def update(self):
        self.hitbox = pygame.Rect(self.rect.left + 90, self.rect.top + 120, 75, 50)

    def death(self, gameManager):
        gameManager.death()


class GameManager:
    secondCounter = 0
    secondPassed = 0

    def __init__(self):
        self.isInMenu = True
        self.isInGame = False
        self.isDead = False

    def updateTimer(self):
        self.secondCounter += 1
        if self.secondCounter % 60 == 0:
            self.secondPassed += 1

    def play(self):
        self.secondCounter = 0
        self.secondPassed = 0
        self.isInMenu = False
        self.isInGame = True
        self.isDead = False

    def death(self):
        self.secondCounter = 0
        self.secondPassed = 0
        self.isInMenu = False
        self.isInGame = False
        self.isDead = True


class Ground(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen.get_width():
            self.kill()


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, isTop):
        pygame.sprite.Sprite.__init__(self)
        if isTop:
            self.image = wall_top
        else:
            self.image = wall_bot
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen.get_width():
            self.kill()


pygame.init()
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Gone")

wall_bot = pygame.image.load("Assets/lavaWallBot.png")
wall_top = pygame.image.load("Assets/lavaWallTop.png")
ground_image = pygame.image.load("Assets/lavaGround.png")
menuBG = pygame.image.load("Assets/menuBG.jpg")
deathBG = pygame.image.load("Assets/deathBG.jpg")
player = Player()

scroll_speed = 4

flapHeight = 60

bg = pygame.image.load("Assets/lava.jpg")

FPS = 60





def check_death(rectList, gameManager):
    if player.posY > screen.get_height() - 280:
        player.death(gameManager)
    if player.posY < -250:
        player.death(gameManager)
    for i in range(len(rectList)):
        if player.hitbox.colliderect(rectList[i]):
            player.death(gameManager)


def main():
    isFalling = True
    ground = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    gameManager = GameManager()
    raiseStart_Y = 0
    isRaising = False
    rectList = list()
    clock = pygame.time.Clock()
    isRunning = True
    ground_x_pos, ground_y_pos = 0, 700
    ground.add(Ground(ground_x_pos, ground_y_pos))
    playBtn = pygame.Rect(560, 350, 300, 140)
    exitBtn = pygame.Rect(560, 550, 300, 140)
    while isRunning:
        screen.fill((255, 255, 255))
        clock.tick(FPS)
        gameManager.updateTimer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if gameManager.isInGame and event.type == pygame.MOUSEBUTTONDOWN and not isRaising:
                isRaising = True
            if gameManager.isInMenu and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playBtn.collidepoint(pygame.mouse.get_pos()):
                        gameManager.play()
                        continue
                    if exitBtn.collidepoint(pygame.mouse.get_pos()):
                        isRunning = False
        if gameManager.isInMenu:
            screen.blit(menuBG, (0, 0))
        elif gameManager.isDead:
            screen.blit(deathBG, (0, 0))
            if gameManager.secondPassed > 3:
                player.restart()
                main()
                return
        else:
            screen.blit(bg, (0, 0))
            #print("playing")
            if gameManager.secondPassed < 3:
                continue
            if isRaising:
                player.drawUp()
                if raiseStart_Y == 0:
                    raiseStart_Y = player.posY
                if player.posY > raiseStart_Y - flapHeight:
                    player.velocity = -10
                else:
                    isRaising = False
                    raiseStart_Y = 0
            else:
                player.drawDown()
            player.velocity += 0.5
            player.update()
            #pygame.draw.rect(screen, (255, 100, 100), player.hitbox)
            if len(ground) <= 2:
                ground.add(Ground(screen.get_width(), ground_y_pos))
            if len(walls) < 6:
                tempWall = None
                onTop = False
                if random.randint(0, 1) == 1:
                    onTop = True
                if len(walls) == 0:
                    if onTop:
                        tempWall = Wall(screen.get_width() + random.randint(100, 500), random.randint(-500, -100), True)
                    else:
                        tempWall = Wall(screen.get_width() + random.randint(100, 500), random.randint(200, 500), False)
                else:
                    if onTop:
                        tempWall = Wall(rectList[-1].x + random.randint(400, 900), random.randint(-500, -100), True)
                    else:
                        tempWall = Wall(rectList[-1].x + random.randint(400, 900), random.randint(200, 500), False)
                walls.add(tempWall)
                rectList.append(tempWall.rect)
            check_death(rectList, gameManager)
            walls.draw(screen)
            ground.draw(screen)
            walls.update()
            ground.update()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()