import pygame, sys, random

#general setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
time = pygame.time.get_ticks()
#text
TEXT_FONT = pygame.font.Font('8-BIT WONDER.TTF', 60)
OPTIONS_FONT = pygame.font.Font('8-BIT WONDER.TTF',40)
HEALTH_FONT = pygame.font.Font('8-BIT WONDER.TTF', 40)
music_font = pygame.font.Font('8-BIT WONDER.TTF', 20)
#screen setup
WIDTH = 900
HEIGHT = 700

pygame.display.set_caption("not-pong!")
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
black = (0,0,0)

rows = 5
cols = 3
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#sound setup
bg_music = pygame.mixer.Sound("retro_funk.ogg")
bg_music.set_volume(0.01)
score_sound = pygame.mixer.Sound("score.ogg")
wall_sound = pygame.mixer.Sound("wall.ogg")
wall_sound.set_volume(1)
paddle_music = pygame.mixer.Sound("paddle.ogg")
ded_sound = pygame.mixer.Sound("explo.ogg")
#player and opponent setup
BALL_VEL_X = 7 * random.choice((1,-1))
BALL_VEL_Y = 7 * random.choice((1,-1))
ball = pygame.Rect(WIDTH/2 - 8, HEIGHT/2 + 8, 16,16)
ai = True

PLAYER_VEL = 5

player = []
opponent = []
playercollide = []
player_individual = []
opponentcollide = []

player_health = 15
opponent_health = 15
#gui design
game_name = TEXT_FONT.render("NOTPONG", 1, light_grey)
game_rect = game_name.get_rect()
singleplayer = OPTIONS_FONT.render("singleplayer", 1 , light_grey)
singleplayer_rect = singleplayer.get_rect()
multiplayer = OPTIONS_FONT.render("multiplayer", 1, light_grey)
multiplayer_rect = multiplayer.get_rect()
start = OPTIONS_FONT.render("START",1 ,light_grey)
start_rect = start.get_rect()
options = OPTIONS_FONT.render("OPTIONS",1, light_grey)
options_rect = options.get_rect()
credit = OPTIONS_FONT.render("CREDITS", 1, light_grey)
credit_rect = credit.get_rect()
exit = OPTIONS_FONT.render("EXIT",1 ,light_grey)
exit_rect = exit.get_rect()

for row in range(rows):
    block_row = []
    for col in range(cols):
        hit_check = False
        block_x = 100 + 10 * col
        block_y = 275 + 40 * row
        rect = pygame.Rect(block_x, block_y,10, 40)
        playercollide.append(rect)
        player_individual = [rect, hit_check]
        block_row.append(player_individual)
    player.append(block_row)

for row in range(rows):
    block_row = []
    for col in range(cols):
        hit_check = False
        block_x = WIDTH - (100 + 10 * col)
        block_y = (275 + 40 * row)
        rect = pygame.Rect(block_x, block_y,10, 40)
        opponentcollide.append(rect)
        opponent_individual = [rect, hit_check]
        block_row.append(opponent_individual)
    opponent.append(block_row)

def draw(WIN, player, opponent,ball, additional_ball):
    WIN.fill(bg_color)

    for row in player:
        for block in row:
            if block[1] == False:
                pygame.draw.rect(WIN, light_grey, block[0])

    for row in opponent:
        for block in row:
            if block[1] == False:
                pygame.draw.rect(WIN, light_grey, block[0])
    pygame.draw.ellipse(WIN, light_grey, ball)
    pygame.draw.aaline(WIN, light_grey,(WIDTH / 2.0, 0), (WIDTH / 2, HEIGHT))
    for balls in additional_ball:
        pygame.draw.ellipse(WIN, light_grey, balls)
    player_health_text = HEALTH_FONT.render(str(player_health), 1, (255, 255, 255))
    opponent_health_text = HEALTH_FONT.render(str(opponent_health), 1, (255, 255, 255))
    WIN.blit(opponent_health_text, (900 - opponent_health_text.get_width() - 10, 10))
    WIN.blit(player_health_text, (10, 10))
    pygame.display.update()

def player_movement(player, keys_pressed, time):
    current_time = pygame.time.get_ticks()
    if keys_pressed[pygame.K_s]:
        for row in player:
            for block in row:
                if current_time - time > 2000:
                    block[0].y += PLAYER_VEL
                else:
                    block[0].y += 0
    if keys_pressed[pygame.K_w]:
        for row in player:
            for block in row:
                if current_time - time > 2000:
                    block[0].y -= PLAYER_VEL
                else:
                    block[0].y += 0
    i = 0

    for row in player:
        check = False
        for block in row:
            if block[0].top <= 0 + i * 40 :
                block[0].top = 0 + i * 40
                check = True
        if check:
            i+=1

    j = 0
    for row in reversed(player):
        check = False
        for block in row:
            if block[0].bottom >= HEIGHT - j * 40 :
                block[0].bottom = HEIGHT - j * 40
                check = True
        if check:
            j+=1

def opponent_movement(opponent):
  current_time = pygame.time.get_ticks()
  i = 0
  for row in opponent:
      check = False
      for block in row:
          if block[0].top <= 0 + i * 40:
              block[0].top = 0 + i * 40
              check = True
      if check:
          i+=1

  j = 0
  for row in reversed(opponent):
      check = False
      for block in row:
          if block[0].bottom >= HEIGHT - j * 40:
              block[0].bottom = HEIGHT - j * 40
              check = True
      if check:
          j += 1

  n = -1
  x = 0
  y = 0
  check = False
  for row in opponent:
      check = False
      for block in row:
          if block[1] == False:
              check = True
      if check:
          n+=1
  if n == -1:
      n = 0
  for i in range(3):
      if opponent[n][i][1] == False:
          x = i
  for i in range(3):
      if opponent[4-n][i][1] == False:
          y = i

  if opponent[n][x][0].bottom - n*20 < ball.y:
      for row in opponent:
          for block in row:
              if current_time - time > 2000:
                  block[0].y -= PLAYER_VEL
              else:
                  block[0].y += 0

  if opponent[4-n][y][0].top + n*20 > ball.y:
      for row in opponent:
          for block in row:
              if current_time - time > 2000:
                  block[0].y += PLAYER_VEL
              else:
                  block[0].y += 0

def second_player_movement(opponent, keys_pressed, time):
    current_time = pygame.time.get_ticks()
    if keys_pressed[pygame.K_DOWN]:
        for row in opponent:
            for block in row:
                if current_time - time > 2000:
                    block[0].y += PLAYER_VEL
                else:
                    block[0].y += 0
    if keys_pressed[pygame.K_UP]:
        for row in opponent:
            for block in row:
                if current_time - time > 2000:
                    block[0].y -= PLAYER_VEL
                else:
                    block[0].y += 0
    i = 0

    for row in opponent:
        check = False
        for block in row:
            if block[0].top <= 0 + i * 40:
                block[0].top = 0 + i * 40
                check = True
        if check:
            i += 1

    j = 0
    for row in reversed(opponent):
        check = False
        for block in row:
            if block[0].bottom >= HEIGHT - j * 40:
                block[0].bottom = HEIGHT - j * 40
                check = True
        if check:
            j += 1

def ball_animations(ball, player, additional_ball, max_ball,additional_ball_vel_x, additional_ball_vel_y):

    global player_health, opponent_health, time, OPTIONS_FONT
    current_time = pygame.time.get_ticks()
    collision_thresh = 3
    global BALL_VEL_X, BALL_VEL_Y
    if current_time - time < 2100:
        ball.x += 0
        ball.y += 0
    else:
        ball.x += BALL_VEL_X
        ball.y += BALL_VEL_Y
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_VEL_Y *= -1
        pygame.mixer.Sound.play(wall_sound)
    if ball.left <= 0 or ball.right >= WIDTH:
        BALL_VEL_X *= -1
        pygame.mixer.Sound.play(wall_sound)
        pygame.display.update()
    if current_time - time < 700:
        number = OPTIONS_FONT.render("3", 1, light_grey)
        WIN.blit(number,(WIDTH/2 - number.get_width()/2, HEIGHT/2 - number.get_height()/2 - 40))
        pygame.display.update()
    if 700 < current_time - time < 1400:
        number = OPTIONS_FONT.render("2", 1, light_grey)
        WIN.blit(number,(WIDTH/2 - number.get_width()/2, HEIGHT/2 - number.get_height()/2 - 40))
        pygame.display.update()
    if 1400 < current_time - time < 2100:
        number = OPTIONS_FONT.render("1", 1, light_grey)
        WIN.blit(number, (WIDTH / 2 - number.get_width() / 2, HEIGHT / 2 - number.get_height() / 2 - 40))
        pygame.display.update()


    row_count = 0
    for row in player:
        block_count = 0
        for block in row:
            if ball.colliderect(block[0]) and block[1] == False:
                if abs(ball.bottom - block[0].top) < collision_thresh and BALL_VEL_Y > 0:
                    BALL_VEL_Y *= -1
                if abs(ball.top - block[0].bottom) < collision_thresh and BALL_VEL_Y < 0:
                    BALL_VEL_Y *= -1
                if abs(ball.right - block[0].left) < collision_thresh and BALL_VEL_X > 0:
                    BALL_VEL_X *= -1
                if abs(ball.left - block[0].right) < collision_thresh and BALL_VEL_X < 0:
                    BALL_VEL_X *= -1
                additional_balls(additional_ball, max_ball, ball, additional_ball_vel_x, additional_ball_vel_y)
                player_health -= 1
                player[row_count][block_count][1] = True
                paddle_music.play()
            block_count += 1
        row_count += 1

    opponent_row_count = 0
    for row in opponent:
        block_count = 0
        for block in row:
            if ball.colliderect(block[0]) and block[1] == False:
                if abs(ball.bottom - block[0].top) < collision_thresh and BALL_VEL_Y > 0:
                    BALL_VEL_Y *= -1
                if abs(ball.top - block[0].bottom) < collision_thresh and BALL_VEL_Y < 0:
                    BALL_VEL_Y *= -1
                if abs(ball.right - block[0].left) < collision_thresh and BALL_VEL_X > 0:
                    BALL_VEL_X *= -1
                if abs(ball.left - block[0].right) < collision_thresh and BALL_VEL_X < 0:
                    BALL_VEL_X *= -1
                additional_balls(additional_ball, max_ball, ball, additional_ball_vel_x, additional_ball_vel_y)
                opponent_health -= 1
                opponent[opponent_row_count][block_count][1] = True
                paddle_music.play()
            block_count += 1
        opponent_row_count += 1

def additional_balls(additional_ball, max_ball,ball,additional_ball_vel_x, additional_ball_vel_y):

    x = 0
    if ball.right >= WIDTH:
        x = WIDTH-16
    else:
        x = ball.x+8
    if len(additional_ball) < max_ball:
        xtra_ball = pygame.Rect(x, ball.bottom - 8, 16,16)
        xtra_ball_vel_x = 7
        xtra_ball_vel_y = 7
        additional_ball_vel_x.append(xtra_ball_vel_x)
        additional_ball_vel_y.append(xtra_ball_vel_y)
        additional_ball.append(xtra_ball)

def additional_ball_animations(additional_ball,additional_ball_vel_x,additional_ball_vel_y,player,opponent):
    global player_health, opponent_health
    collision_thresh = 3
    for ball in range(len(additional_ball)):
        additional_ball[ball].x += additional_ball_vel_x[ball]
        additional_ball[ball].y += additional_ball_vel_y[ball]
        if additional_ball[ball].top <= 0 or additional_ball[ball].bottom >= HEIGHT:
            additional_ball_vel_y[ball] *= -1
            pygame.mixer.Sound.play(wall_sound)
        if additional_ball[ball].left <= 0 or additional_ball[ball].right-8 >= WIDTH:
            additional_ball_vel_x[ball] *= -1
            pygame.mixer.Sound.play(wall_sound)

        row_count = 0
        for row in player:
            block_count = 0
            for block in row:
                if additional_ball[ball].colliderect(block[0]) and block[1] == False:
                    if abs(additional_ball[ball].bottom - block[0].top) < collision_thresh and additional_ball_vel_y[ball] > 0:
                        additional_ball_vel_y[ball] *= -1
                    if abs(additional_ball[ball].top - block[0].bottom) < collision_thresh and additional_ball_vel_y[ball] < 0:
                        additional_ball_vel_y[ball] *= -1
                    if abs(additional_ball[ball].right - block[0].left) < collision_thresh and additional_ball_vel_x[ball] > 0:
                        additional_ball_vel_x[ball] *= -1
                    if abs(additional_ball[ball].left - block[0].right) < collision_thresh and additional_ball_vel_x[ball] < 0:
                        additional_ball_vel_x[ball] *= -1
                    paddle_music.play()
                    player_health -= 1
                    player[row_count][block_count][1] = True
                block_count += 1
            row_count += 1

        opponent_row_count = 0
        for row in opponent:
            block_count = 0
            for block in row:
                if additional_ball[ball].colliderect(block[0]) and block[1] == False:
                    if abs(additional_ball[ball].bottom - block[0].top) < collision_thresh and additional_ball_vel_y[ball] > 0:
                        additional_ball_vel_y[ball] *= -1
                    if abs(additional_ball[ball].top - block[0].bottom) < collision_thresh and additional_ball_vel_y[ball] < 0:
                        additional_ball_vel_y[ball] *= -1
                    if abs(additional_ball[ball].right - block[0].left) < collision_thresh and additional_ball_vel_x[ball] > 0:
                        additional_ball_vel_x[ball] *= -1
                    if abs(additional_ball[ball].left - block[0].right) < collision_thresh and additional_ball_vel_x[ball] < 0:
                        additional_ball_vel_x[ball] *= -1
                    paddle_music.play()
                    opponent_health -= 1
                    opponent[opponent_row_count][block_count][1] = True
                block_count += 1
            opponent_row_count += 1

def score():
    global player_health, opponent_health, ball, ai
    if player_health == 0 and ai == True:
        text = OPTIONS_FONT.render("YOU LOSE",1,light_grey)
        ded_sound.play()
        WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()*2))
        pygame.display.update()
        pygame.time.delay(2000)
        player_health = 15
        opponent_health =15
        player.clear()
        opponent.clear()
        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = 100 + 10 * col
                block_y = 275 + 40 * row
                rect = pygame.Rect(block_x, block_y, 10, 40)
                playercollide.append(rect)
                player_individual = [rect, hit_check]
                block_row.append(player_individual)
            player.append(block_row)

        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = WIDTH - (100 + 10 * col)
                block_y = (275 + 40 * row)
                rect = pygame.Rect(block_x, block_y, 10, 40)
                opponentcollide.append(rect)
                opponent_individual = [rect, hit_check]
                block_row.append(opponent_individual)
            opponent.append(block_row)

        ball.center = (WIDTH/2, HEIGHT/2)

        game_loop()
    if opponent_health == 0 and ai == True:
        text = OPTIONS_FONT.render("YOU WIN",1,light_grey)
        WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()*2))
        ded_sound.play()
        pygame.display.update()
        pygame.time.delay(2000)
        player_health = 15
        opponent_health =15
        player.clear()
        opponent.clear()
        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = 100 + 10 * col
                block_y = 275 + 40 * row
                rect = pygame.Rect(block_x, block_y, 10, 40)
                playercollide.append(rect)
                player_individual = [rect, hit_check]
                block_row.append(player_individual)
            player.append(block_row)

        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = WIDTH - (100 + 10 * col)
                block_y = (275 + 40 * row)
                rect = pygame.Rect(block_x, block_y, 10, 40)
                opponentcollide.append(rect)
                opponent_individual = [rect, hit_check]
                block_row.append(opponent_individual)
            opponent.append(block_row)

        ball.center = (WIDTH / 2, HEIGHT / 2)
        game_loop()
    if player_health == 0 and ai == False:
        text = OPTIONS_FONT.render("P2 WINS",1,light_grey)
        ded_sound.play()
        WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()*2))
        pygame.display.update()
        pygame.time.delay(2000)
        player_health = 15
        opponent_health =15
        player.clear()
        opponent.clear()
        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = 100 + 10 * col
                block_y = 275 + 40 * row
                rect = pygame.Rect(block_x, block_y, 10, 40)
                playercollide.append(rect)
                player_individual = [rect, hit_check]
                block_row.append(player_individual)
            player.append(block_row)

        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = WIDTH - (100 + 10 * col)
                block_y = (275 + 40 * row)
                rect = pygame.Rect(block_x, block_y, 10, 40)
                opponentcollide.append(rect)
                opponent_individual = [rect, hit_check]
                block_row.append(opponent_individual)
            opponent.append(block_row)

        ball.center = (WIDTH/2, HEIGHT/2)
        ai = True
        game_loop()
    if opponent_health == 0 and ai == False:
        text = OPTIONS_FONT.render("P1 WINS",1,light_grey)
        WIN.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()*2))
        ded_sound.play()
        pygame.display.update()
        pygame.time.delay(2000)
        player_health = 15
        opponent_health =15
        player.clear()
        opponent.clear()
        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = 100 + 10 * col
                block_y = 275 + 40 * row
                rect = pygame.Rect(block_x, block_y, 10, 40)
                playercollide.append(rect)
                player_individual = [rect, hit_check]
                block_row.append(player_individual)
            player.append(block_row)

        for row in range(rows):
            block_row = []
            for col in range(cols):
                hit_check = False
                block_x = WIDTH - (100 + 10 * col)
                block_y = (275 + 40 * row)
                rect = pygame.Rect(block_x, block_y, 10, 40)
                opponentcollide.append(rect)
                opponent_individual = [rect, hit_check]
                block_row.append(opponent_individual)
            opponent.append(block_row)
        ai = True
        ball.center = (WIDTH / 2, HEIGHT / 2)
        game_loop()

def pause(keys_pressed):
    global player_health, opponent_health
    if keys_pressed[pygame.K_ESCAPE]:
        resume = OPTIONS_FONT.render("RESUME", 1, light_grey)
        exi = OPTIONS_FONT.render("Exit", 1, light_grey)
        resume_rect = resume.get_rect()
        exi_rect = exi.get_rect()
        resume_rect.topleft = (WIDTH/2 - resume.get_width()/2-10, HEIGHT/2 - resume.get_height()*2 -20+10)
        exi_rect.topleft = (WIDTH / 2 - exi.get_width() / 2 - 10, HEIGHT / 2 - exi.get_height()*2+40+10)
        paused = True
        while paused:
            pygame.mixer.Sound.play(bg_music)
            click = False
            nx, ny = pygame.mouse.get_pos()
            WIN.fill(bg_color)
            pygame.draw.rect(WIN, black, resume_rect)
            pygame.draw.rect(WIN, black, exi_rect)
            WIN.blit(resume, (WIDTH / 2 - resume.get_width() / 2, HEIGHT / 2 - resume.get_height() * 2 - 20))
            WIN.blit(exi, (WIDTH / 2 - exi.get_width() / 2, HEIGHT / 2 - exi.get_height() * 2 + 40))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1:
                        click = True
            if resume_rect.collidepoint(nx,ny):
                if click:
                    pygame.mixer.Sound.stop(bg_music)
                    paused = False
            if exi_rect.collidepoint(nx,ny):
                if click:
                    pygame.mixer.Sound.stop(bg_music)
                    paused = False
                    player_health = 15
                    opponent_health = 15
                    player.clear()
                    opponent.clear()
                    for row in range(rows):
                        block_row = []
                        for col in range(cols):
                            hit_check = False
                            block_x = 100 + 10 * col
                            block_y = 275 + 40 * row
                            rect = pygame.Rect(block_x, block_y, 10, 40)
                            playercollide.append(rect)
                            player_individual = [rect, hit_check]
                            block_row.append(player_individual)
                        player.append(block_row)

                    for row in range(rows):
                        block_row = []
                        for col in range(cols):
                            hit_check = False
                            block_x = WIDTH - (100 + 10 * col)
                            block_y = (275 + 40 * row)
                            rect = pygame.Rect(block_x, block_y, 10, 40)
                            opponentcollide.append(rect)
                            opponent_individual = [rect, hit_check]
                            block_row.append(opponent_individual)
                        opponent.append(block_row)

                    ball.center = (WIDTH / 2, HEIGHT / 2)
                    game_loop()
            pygame.display.update()

def main():
    additional_ball = []
    additional_ball_vel_x = []
    additional_ball_vel_y = []
    max_ball = 3
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        pause(keys_pressed)
        player_movement(player, keys_pressed, time)
        opponent_movement(opponent)
        ball_animations(ball,player, additional_ball, max_ball,additional_ball_vel_x, additional_ball_vel_y)
        additional_ball_animations(additional_ball, additional_ball_vel_x, additional_ball_vel_y,player,opponent)
        score()
        draw(WIN, player, opponent, ball, additional_ball)

def main_multiplayer():
    global ai
    ai = False
    additional_ball = []
    additional_ball_vel_x = []
    additional_ball_vel_y = []
    max_ball = 3
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        pause(keys_pressed)
        player_movement(player, keys_pressed, time)
        second_player_movement(opponent, keys_pressed, time)
        ball_animations(ball, player, additional_ball, max_ball, additional_ball_vel_x, additional_ball_vel_y)
        additional_ball_animations(additional_ball, additional_ball_vel_x, additional_ball_vel_y, player, opponent)
        score()
        draw(WIN, player, opponent, ball, additional_ball)

def main_menu():
    global game_rect,game_name,start_rect,start,options_rect,options,credit_rect,credit,exit_rect,exit, singleplayer, singleplayer_rect, multiplayer, multiplayer_rect
    bg_music.play()
    WIN.fill(bg_color)
    game_rect.topleft = (WIDTH / 2 - game_name.get_width() / 2 -20, HEIGHT / 2 - game_name.get_height() * 2 +20)
    singleplayer_rect.topleft = (WIDTH/2-singleplayer.get_width()/2 - 10, HEIGHT/2 +20)
    multiplayer_rect.topleft = (WIDTH/2-multiplayer.get_width()/2-10, HEIGHT/2 + 20 + multiplayer.get_height()+10)
    #start_rect.topleft = (WIDTH/2-start.get_width()/2, HEIGHT/2 + 10)
    options_rect.topleft = (WIDTH/2-options.get_width()/2 -10, HEIGHT/2 + 30 + options.get_height()*2+10)
    credit_rect.topleft = (WIDTH/2-credit.get_width()/2-10, HEIGHT/2 + 40 + credit.get_height()*3+10)
    exit_rect.topleft = (WIDTH/2-exit.get_width()/2-10, HEIGHT/2 + 50 + exit.get_height()*4+10)

    pygame.draw.rect(WIN, black, game_rect)
    #pygame.draw.rect(WIN, bg_color, start_rect)
    pygame.draw.rect(WIN, black, singleplayer_rect)
    pygame.draw.rect(WIN,black,multiplayer_rect)
    pygame.draw.rect(WIN, black, options_rect)
    pygame.draw.rect(WIN, black, credit_rect)
    pygame.draw.rect(WIN, black, exit_rect)

    WIN.blit(game_name, (WIDTH/2 - game_name.get_width()/2, HEIGHT/2 - game_name.get_height()*2))
    #WIN.blit(start, (WIDTH/2-start.get_width()/2, HEIGHT/2 + 10))
    WIN.blit(singleplayer,(WIDTH/2-singleplayer.get_width()/2, HEIGHT/2 + 10))
    WIN.blit(multiplayer,(WIDTH/2-multiplayer.get_width()/2, HEIGHT/2 + 20 + multiplayer.get_height()))
    WIN.blit(options, (WIDTH/2-options.get_width()/2, HEIGHT/2 + 30 + options.get_height()*2))
    WIN.blit(credit, (WIDTH/2-credit.get_width()/2, HEIGHT/2 + 40 + credit.get_height()*3))
    WIN.blit(exit, (WIDTH/2-exit.get_width()/2, HEIGHT/2 + 50 + exit.get_height()*4))

    pygame.display.update()

def menu_handle(mx,my,click):
    global game_rect, game_name, start_rect, start, options_rect, options, credit_rect, credit, exit_rect, exit,time, singleplayer_rect, singleplayer, multiplayer_rect, multiplayer

    if singleplayer_rect.collidepoint(mx,my):
        if click:
            time = pygame.time.get_ticks()
            pygame.mixer.Sound.stop(bg_music)
            main()
    if multiplayer_rect.collidepoint(mx,my):
        if click:
            time = pygame.time.get_ticks()
            pygame.mixer.Sound.stop(bg_music)
            main_multiplayer()
    if options_rect.collidepoint(mx,my):
        if click:
            running = True
            while running:
                WIN.fill(bg_color)
                text = OPTIONS_FONT.render("control w s up down",1,light_grey)
                WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()*2))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
                pygame.time.delay(2000)
                running = False
            main_menu()

    if credit_rect.collidepoint(mx, my):
        if click:
            running = True
            while running:
                WIN.fill(bg_color)
                text = ["ZABIR RAMIZ","FAZLE RAHMAN", "Sarwat Saadaat","ABID MAHMUD","TEAM EGGNOG"]
                music = music_font.render("music credit enes deniz and atari", 1 , light_grey)
                for i in range(len(text)):
                    text[i] = OPTIONS_FONT.render(text[i],1,light_grey)
                    WIN.blit(text[i],(WIDTH/2 - text[i].get_width()/2, HEIGHT/2 - text[i].get_height()*i + 40 ))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                WIN.blit(music, (WIDTH/2 - music.get_width()/2, HEIGHT/2 - music.get_height()*5 + 200 ))
                pygame.display.update()
                pygame.time.delay(4000)
                running = False
            main_menu()

    if exit_rect.collidepoint(mx, my):
        if click:
            pygame.quit()
            sys.exit()

def game_loop():
    while True:
        mx,my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        main_menu()
        menu_handle(mx, my, click)

game_loop()






