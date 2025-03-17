from pygame import*
window = display.set_mode((600,400))
display.set_caption('My first game')
class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x        
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)

        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)

        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)

        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
                    
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
class Enemy(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x<=420:
            self.side = "right"
        if self.rect.x>=win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed                
win_width = 800
win_height = 600
barriers = sprite.Group()
wall_1 = GameSprite('wall.png',win_width / 2 - win_width / 3, win_height / 2,300,50)
wall_2 = GameSprite('wall2.png',370,100,50,400)
monster = Enemy('pacmanenemy.png', win_width - 80,180,80,80,5)
packman = Player("2.png",5,win_height - 80,80,80,0,0)
final_sprite = GameSprite('wincongrats.jpg', win_width - 85,win_height - 100, 80,80)
barriers.add(wall_1)
barriers.add(wall_2)

back =(119,210,250)
keys = {K_LEFT:(-5,0),K_RIGHT:(5,0),K_UP:(0,-5),K_DOWN:(0,5)}
finish = False
end = True
while end:
    time.delay(45)
    for e in event.get():
        if e.type == QUIT:
            end = False
        elif e.type in (KEYDOWN, KEYUP):
            speed = 0 if e.type == KEYUP else 1
            if e.key in keys:
                packman.x_speed = keys[e.key][0]*speed 
                packman.y_speed = keys[e.key][1]*speed 
    if not finish:
        window.fill(back)
        barriers.draw(window)
        packman.update()
        packman.reset()
        monster.update()
        monster.reset()
        final_sprite.reset()
        if sprite.collide_rect(packman, monster):
            finish = True
            img = image.load("gameover.png")
            d = img.get_width()//img.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_height*d,win_height)),(90,0))
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load("wincongrats.jpg")
            d = img.get_width()//img.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_height*d,win_height)),(90,0))
    display.update()