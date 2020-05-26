import os
import pygame
import random

pygame.init()
color = 1
voloume = 0.1
complexity = 1
infoObject = pygame.display.Info()
globx = infoObject.current_w // 2
globy = infoObject.current_h // 2
if globx > globy:
    scale = globx
else:
    scale = globy
screen = pygame.display.set_mode((int(globx), int(globy)))
run = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
enemys = pygame.sprite.Group()
enemys_bullets = pygame.sprite.Group()
bufs = pygame.sprite.Group()
pygame.mouse.set_visible(False)
shield_time = 50
score = 0
font_name = pygame.font.match_font('arial')
heath = 3
addmet = 0
adden = 0


def load(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_m(name):
    fullname = os.path.join('sound', name)
    return pygame.mixer.Sound(fullname)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


def newmet():
    m = Meteor()
    all_sprites.add(m)
    mobs.add(m)


def newen():
    e = Enemy()
    all_sprites.add(e)
    enemys.add(e)


def show_go(score):
    waiting = True
    while waiting:
        screen.blit(back, backrect)
        start_button = pygame.Rect((int(globx // 2 - globx // 8), int(globy * 3 // 4.5), int(globx // 4), int(globy * 3 / 4.5)))
        settings_button = pygame.Rect((int(globx // 2 - globx // 8), int(globy * 3.5 // 4.5), int(globx // 4), int(globy * 3 / 4.5)))
        draw_text(screen, "Ваш счёт:{}".format(score), 30, globx // 2, globy // 5)
        draw_text(screen, "НАЧАТЬ", 28, globx // 2, globy * 3 // 4.5)
        draw_text(screen, "НАСТРОЙКИ", 21, globx // 2, globy * 3.5 // 4.5)
        if color == 1:
            im = load('char_blue.png', -1)
        elif color == 2:
            im = load('char_green.png', -1)
        elif color == 3:
            im = load('char_red.png', -1)

        im = pygame.transform.scale(im, (int(scale * 0.1), int(scale * 0.1)))
        screen.blit(im, (int(globx // 2 - globx * 0.05), int(globy * 2 / 4.5)))
        pygame.display.flip()
        clock.tick(50)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == 6:
                if start_button.collidepoint(x, y):
                    waiting = False
                if settings_button.collidepoint(x, y):
                    show_setting()

            if event.type == 5:
                if start_button.collidepoint(x, y):
                    waiting = False

                if settings_button.collidepoint(x, y):
                    show_setting()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_setting()

    return True


def show_setting():
    global voloume, color, complexity
    run = True
    volleft_button = pygame.Rect((105, 145), (35, 35))
    volright_button = pygame.Rect((225, 145), (35, 35))
    charleft_button = pygame.Rect((85, 285), (35, 35))
    charright_button = pygame.Rect((255, 285), (35, 35))
    complexityleft_button = pygame.draw.rect(screen, (255, 0, 0), ((115, 450), (35, 35)))
    complexityright_button = pygame.draw.rect(screen, (255, 0, 0), ((235, 450), (35, 35)))
    quit_button = pygame.Rect(145, 555, 85, 35)
    while run:
        screen.blit(back, backrect)
        for i in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if i.type == pygame.QUIT:
                pygame.quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    voloume += 0.1
                    if voloume > 1:
                        voloume = 1
                elif i.key == pygame.K_DOWN:
                    voloume -= 0.1
                    if voloume < 0:
                        voloume = 0
                elif i.key == pygame.K_LEFT:
                    color -= 1
                    if color == 0:
                        color = 3
                elif i.key == pygame.K_RIGHT:
                    color += 1
                    if color == 4:
                        color = 1
                elif i.key == pygame.K_ESCAPE:
                    run = False

            elif i.type == 6:
                if volleft_button.collidepoint(x, y):
                    voloume -= 0.1
                    if voloume < 0:
                        voloume = 0
                if volright_button.collidepoint(x, y):
                    voloume += 0.1
                    if voloume > 1:
                        voloume = 1

                if charleft_button.collidepoint(x, y):
                    color -= 1
                    if color == 0:
                        color = 3

                if charright_button.collidepoint(x, y):
                    color += 1
                    if color == 4:
                        color = 1

                if complexityright_button.collidepoint(x, y):
                    complexity += 1
                    if complexity == 4:
                        complexity = 1

                if complexityleft_button.collidepoint(x, y):
                    complexity -= 1
                    if complexity == 0:
                        complexity = 3

                if quit_button.collidepoint(x, y):
                    run = False

        draw_text(screen, "ГРОМКОСТЬ", 21, globx // 2, globy // 14)
        draw_text(screen, str(int(voloume * 100)), 30, globx // 2, globy // 8)
        draw_text(screen, "ПЕРСОНАЖ", 21, globx // 2, globy // 4)
        draw_text(screen, "СЛОЖНОСТЬ", 21, globx // 2, globy // 1.8)
        if complexity == 1:
            draw_text(screen, "ЛЕГКО", 20, globx // 2, globy // 1.4)
        if complexity == 2:
            draw_text(screen, "НОРМАЛЬНО", 20, globx // 2, globy // 1.4)
        if complexity == 3:
            draw_text(screen, "СЛОЖНО", 20, globx // 2, globy // 1.4)
        if color == 1:
            im = load('char_blue.png', -1)
        elif color == 2:
            im = load('char_green.png', -1)
        elif color == 3:
            im = load('char_red.png', -1)
        im = pygame.transform.scale(im, (int(scale * 0.135), int(scale * 0.125)))
        imstrelka1 = load('stre1.png', -1)
        imstrelka1 = pygame.transform.scale(imstrelka1, (int(scale * 0.05), int(scale * 0.05)))
        imstrelka2 = load("stre2.png", -1)
        imstrelka2 = pygame.transform.scale(imstrelka2, (int(scale * 0.05), int(scale * 0.05)))
        screen.blit(im, (globx // 2.3, globy // 3))
        screen.blit(imstrelka1, (globx // 2.2 - globx // 8, globy // 6.3))
        screen.blit(imstrelka2, (globx // 1.65, globy // 6.3))
        screen.blit(imstrelka1, (globx // 2.2 - globx // 8, globy // 2.3))
        screen.blit(imstrelka2, (globx // 1.65, globy // 2.3))
        screen.blit(imstrelka1, (globx // 2.2 - globx // 8, globy // 1.4))
        screen.blit(imstrelka2, (globx // 1.65, globy // 1.4))
        draw_text(screen, "НАЗАД", 25, 190, 750 * 3 / 4)
        pew.set_volume(voloume)
        bah1.set_volume(voloume)
        bah2.set_volume(voloume)
        bah3.set_volume(voloume)
        music.set_volume(voloume + 0.1)
        buf.set_volume(voloume + 1)
        if int(voloume * 10) == 0:
            music.set_volume(0)
        if int(voloume * 10) == 0:
            buf.set_volume(0)
        pygame.display.flip()
    show_go(0)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + globx // 13 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def draw_shield(rect):
    global color
    if color == 1:
        im = load('char_shield_blue.png', -1)
        im = pygame.transform.scale(im, (int(scale * 0.12), int(scale * 0.12)))
    elif color == 2:
        im = load('char_shield_green.png', -1)
        im = pygame.transform.scale(im, (int(scale * 0.12), int(scale * 0.12)))
    elif color == 3:
        im = load('char_shield_red.png', -1)
        im = pygame.transform.scale(im, (int(scale * 0.12), int(scale * 0.12)))
    x, y, x1, y1 = rect
    screen.blit(im, (x - 10, y - 15, x, y))

class Character(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        global color
        if color == 1:
            im = load('char_blue.png', -1)
        elif color == 2:
            im = load('char_green.png', -1)
        elif color == 3:
            im = load('char_red.png', -1)
        self.image = im
        self.image = pygame.transform.scale(self.image, (int(scale * 0.1), int(scale * 0.1)))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = 200
        self.rect.y = 600
        self.bullettime = 0
        self.shootspeed = 20

    def update(self, *args):
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            self.rect.x = x - 50
            self.rect.y = y - 50

    def powerup(self):
        self.shootspeed -= 2
        if self.shootspeed < 10:
            self.shootspeed = 10

    def shoot(self):
        if self.bullettime >= self.shootspeed:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.bullettime = 0
            pew.play()
        self.bullettime += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global color
        if color == 1:
            im = load('laser_blue.png', -1)
        elif color == 2:
            im = load('laser_green.png', -1)
        elif color == 3:
            im = load('laser_red.png', -1)
        pygame.sprite.Sprite.__init__(self)
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    imlis = [load('met1.png', -1),
             load('met2.png', -1),
             load('met3.png', -1),
             load('met7.png', -1),
             load('met8.png', -1)]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        im = random.choice(Meteor.imlis)
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(globx - self.rect.width)
        self.rect.y = random.randrange(-globx // 4, -globx // 10)
        self.radius = int(self.rect.width * .85 / 2)
        self.speedy = random.randrange(globy // 400, globy // 100)
        self.speedx = random.randrange(- globx // 200, globx // 200)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > globy + 10 or self.rect.left < -25 or self.rect.right > globx + 20:
            self.rect.x = random.randrange(globy)
            self.rect.y = random.randrange(-globx // 4, -globx // 10)
            self.speedy = random.randrange(globy // 400, globy // 100)
            self.speedx = random.randrange(- globx // 200, globx // 200)


class Enemy(pygame.sprite.Sprite):
    imlist = [
        load('enemyBlack1.png', -1),
        load('enemyBlack2.png', -1),
        load('enemyBlack3.png', -1),
        load('enemyBlack4.png', -1),
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        im = random.choice(Enemy.imlist)
        self.image = im

        self.image = pygame.transform.scale(self.image, (51, 51))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(globx)
        self.rect.y = random.randrange(-globy // 7, -globy // 10)
        self.speedy = random.randrange(globy // 100, globy // 60)
        self.shoot()

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.top > globy + 10:
            self.rect.x = random.randrange(globx)
            self.rect.y = random.randrange(-globy // 7, -globy // 10)
            self.speedy = random.randrange(globy // 100, globy // 60)
            self.shoot()

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        enemys_bullets.add(bullet)


class EnemyBullet(pygame.sprite.Sprite):
    im = load('bullet.png', (255, 255, 255))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = EnemyBullet.im
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = globy // 55

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > globy:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = globy // 350

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > globy:
            self.kill()


back = load('black.png')
backrect = back.get_rect()
pew = load_m('pew.wav')
bah1 = load_m('bah.wav')
bah2 = load_m('bah2.wav')
bah3 = load_m('rumble1.ogg')
buf = load_m('buf_sound.wav')
pew.set_volume(voloume)
bah1.set_volume(voloume)
bah2.set_volume(voloume)
bah3.set_volume(voloume)
buf.set_volume(voloume + 1)
game_over = True
music = load_m('DST-RailJet-LongSeamlessLoop.ogg')
music.set_volume(voloume + 0.1)
music.play(loops=-1)
while run:
    if game_over:
        pygame.mouse.set_visible(True)
        game_over = False
        while not show_go(score):
            pass
        pew.set_volume(voloume)
        bah1.set_volume(voloume)
        bah2.set_volume(voloume)
        bah3.set_volume(voloume)
        buf.set_volume(voloume + 1)
        music.set_volume(voloume + 0.1)
        if voloume == 0:
            music.set_volume(0)
        if voloume == 0:
            buf.set_volume(0)
        powerup_images = {}
        if color == 1:
            powerup_images['shield'] = load('Blue_shield.png', -1)
            powerup_images['gun'] = load('Blue_bolt.png', -1)
        elif color == 2:
            powerup_images['shield'] = load('green_shield.png', -1)
            powerup_images['gun'] = load('green_bolt.png', -1)
        elif color == 3:
            powerup_images['shield'] = load('red_shield.png', -1)
            powerup_images['gun'] = load('red_bolt.png', -1)
        if color == 1:
            char_mini = load('mini_blue.png', -1)
        elif color == 2:
            char_mini = load('mini_green.png', -1)
        elif color == 3:
            char_mini = load('mini_red.png', -1)
        all_sprites = pygame.sprite.Group()
        char_sprite = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemys_bullets = pygame.sprite.Group()
        bufs = pygame.sprite.Group()
        pygame.mouse.set_visible(False)
        char = Character(char_sprite)
        explosion_anim = {}
        explosion_anim['lg'] = []
        explosion_anim['sm'] = []
        explosion_anim['player'] = []
        m = Meteor()
        e = Enemy()
        all_sprites.add(char)
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = load(filename, -1)
            img_lg = pygame.transform.scale(img, (int(scale * 0.1), int(scale * 0.1)))
            explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (int(scale * 0.05), int(scale * 0.05)))
            explosion_anim['sm'].append(img_sm)
            explosion_anim['player'].append(img)
        for i in range(globx // 50 + complexity * 2):
            newmet()
        for i in range(globx // 300 + complexity * 2):
            newen()
        score = 0
        heath = 3
        addmet = 0
        adden = 0
    screen.fill((0, 0, 0))
    screen.blit(back, backrect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
    all_sprites.update()
    all_sprites.draw(screen)
    char.shoot()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += hit.radius // 2
        adden += hit.radius // 2
        addmet += hit.radius // 2
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            bufs.add(pow)
        newmet()
        bah1.play()
    hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
    for hit in hits:
        newen()
        score += 50
        adden += 50
        addmet += 50
        expl = Explosion(hit.rect.center, 'lg')
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            bufs.add(pow)
        all_sprites.add(expl)
        bah2.play()
    hits = pygame.sprite.spritecollide(char, mobs, True, pygame.sprite.collide_circle)
    hits2 = pygame.sprite.spritecollide(char, enemys, True, pygame.sprite.collide_circle)
    hits3 = pygame.sprite.spritecollide(char, enemys_bullets, True)

    if hits or hits2 or hits3:
        if shield_time >= 50:
            heath -= 1
        if heath == 0:
            death_explosion = Explosion(char.rect.center, 'player')
            all_sprites.add(death_explosion)
            bah3.play()
            char.kill()
        else:
            shield_time = 0
        if hits:
            newmet()
        if hits2:
            newen()
    if shield_time < 50:
        draw_shield(char.rect)
        shield_time += 1

    hits = pygame.sprite.spritecollide(char, bufs, True)
    for hit in hits:
        buf.play()
        if hit.type == 'shield':
            heath += 1
            if heath > 3:
                heath = 3
        if hit.type == 'gun':
            char.powerup()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_over = True
    if not char.alive() and not death_explosion.alive():
        game_over = True
    draw_text(screen, str(score), 20, globx // 2, globy // 7)
    if adden >= 2000:
        newen()
        adden = 0
    if addmet >= 1000:
        newmet()
        addmet = 0
    draw_lives(screen, globx - globx // 4, globy - globy // 14, heath,
               char_mini)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()