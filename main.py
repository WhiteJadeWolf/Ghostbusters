import pygame
import sqlite3 as sql
import os


from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, MessageBox

pygame.init()

con = sql.connect('ghostbusters.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS leaderboard(id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, timescore INTEGER, finish TEXT, penalty TEXT, diamonds INTEGER, bonus TEXT)")
con.commit()

WIDTH, HEIGHT = 710, 384 
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
TILE_SIZE = 32

clock = pygame.time.Clock()
FPS = 45

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
instructions_font = 'Fonts/BubblegumSans-Regular.ttf'
message_font = pygame.font.SysFont("Verdana",18)
# about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

ghostbusters = Message(WIDTH//2 + 50, HEIGHT//2 - 90, 90, "GhostBusters", title_font, (255, 255, 255), win)
left_key = Message(WIDTH//2 + 10, HEIGHT//2 - 120, 20, "Press left arrow / A key to go left", instructions_font, (255, 255, 255), win)
right_key = Message(WIDTH//2 + 10, HEIGHT//2 - 100, 20, "Press right arrow / D key to go right", instructions_font, (255, 255, 255), win)
up_key = Message(WIDTH//2 + 10, HEIGHT//2 - 80, 20, "Press up arrow key / W to jump", instructions_font, (255, 255, 255), win)
space_key = Message(WIDTH//2 + 10, HEIGHT//2 - 60, 20, "Press space key to shoot", instructions_font, (255, 255, 255), win)
g_key = Message(WIDTH//2 + 10, HEIGHT//2 - 40, 20, "Press g key to throw grenade", instructions_font, (255, 255, 255), win)
diamond_about_1 = Message(WIDTH//2 + 10, HEIGHT//2 , 20, "Every diamond collected deducts 3s from time score", instructions_font, (255, 255, 255), win)
diamond_about_2 = Message(WIDTH//2 + 10, HEIGHT//2 + 20 , 20, "So the more diamonds you collect,", instructions_font, (255, 255, 255), win)
diamond_about_3 = Message(WIDTH//2 + 10, HEIGHT//2 + 40, 20, "your probability to top the leaderboard increases", instructions_font, (255, 255, 255), win)
diamond_about_4 = Message(WIDTH//2 + 10, HEIGHT//2 + 60, 20, "(deduction only counts if you win the game)", instructions_font, (255, 255, 255), win)
game_won_msg = Message(WIDTH//2 + 10, HEIGHT//2 - 5, 20, "You have won the game", instructions_font, (255, 255, 255), win)



t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
controls = t.render('Controls', font_color)
leaderboard = t.render('Leaderboard', font_color)
level_editor = t.render('Level Editor', font_color)
about = t.render('About', font_color)
exit = t.render('Exit', font_color)
main_menu = t.render('Main Menu', font_color)

about_font = pygame.font.SysFont('Times New Roman', 20)
leaderboard_font = pygame.font.SysFont('Times New Roman', 20)
with open('Data/about.txt') as f:
    info = f.read().replace('\n','|||')

def equalspace(x,sample):
	y = 1
	text_rect_s = message_font.render(sample, True, (0, 0, 0)).get_rect()
	n = text_rect_s.width
	text_rect_x = message_font.render(x, True, (0, 0, 0)).get_rect()
	a = text_rect_x.width
	temp = x
	while n >= a:
		x = (y * ' ') + temp + (y * ' ')
		y+=1
		text_rect_x = message_font.render(x, True, (0, 0, 0)).get_rect()
		a = text_rect_x.width
	return x


# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 - 25, ButtonBG, 0.5, play, 1)
leaderboard_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 45, ButtonBG, 0.5, leaderboard, 25)
controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 10, ButtonBG, 0.5, controls, 10)
lvledit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 80, ButtonBG, 0.5, level_editor, 23)
about_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 115, ButtonBG, 0.5, about, 5)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 150, ButtonBG, 0.5, exit, -4)
main_menu_btn = Button(WIDTH//1 - bwidth//4 - 110, HEIGHT//2 + 140, ButtonBG, 0.5, main_menu, 20)

# MUSIC ***********************************************************************

pygame.mixer.music.load('Sounds/mixkit-complex-desire-1093.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

diamond_fx = pygame.mixer.Sound('Sounds/point.mp3')
diamond_fx.set_volume(0.6)
bullet_fx = pygame.mixer.Sound('Sounds/bullet.wav')
jump_fx = pygame.mixer.Sound('Sounds/jump.mp3')
health_fx = pygame.mixer.Sound('Sounds/health.wav')
menu_click_fx = pygame.mixer.Sound('Sounds/menu.mp3')
next_level_fx = pygame.mixer.Sound('Sounds/level.mp3')
grenade_throw_fx = pygame.mixer.Sound('Sounds/grenade throw.wav')
grenade_throw_fx.set_volume(0.6)

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

p_image = pygame.transform.scale(pygame.image.load('Assets/Player/PlayerIdle1.png'), (32,32))
p_rect = p_image.get_rect(center=(470, 200))
p_dy = 1
p_ctr = 1

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200
MAX_LEVEL = 3

level = 1
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0

# RESET ***********************************************************************

def reset_level(level):
	trail_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	enemy_group.empty()
	water_group.empty()
	diamond_group.empty()
	potion_group.empty()
	exit_group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_group)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def reset_player():
	p = Player(250, 50)
	moving_left = False
	moving_right = False

	return p, moving_left, moving_right

# MAIN GAME *******************************************************************

main_menu = True
leaderboard_page = False
about_page = False
controls_page = False
exit_page = False
game_start = False
game_won = True
running = True
elapsed_time = 0
time_score = 0

while running:
	win.fill((0,0,0))
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6, 0))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7, 0))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8, 0))

	if not game_start:
		win.blit(MOON, (-40, 150))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				if not p.jump:
					p.jump = True
					jump_fx.play()
			if event.key == pygame.K_SPACE:
				x, y = p.rect.center
				direction = p.direction
				bullet = Bullet(x, y, direction, (240, 240, 240), 1, win)
				bullet_group.add(bullet)
				bullet_fx.play()
				p.attack = True
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
					grenade_group.add(grenade)
					grenade_throw_fx.play()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				moving_right = False

	if main_menu:
		ghostbusters.update()
		trail_group.update()
		win.blit(p_image, p_rect)
		p_rect.y += p_dy
		p_ctr += p_dy
		if p_ctr > 15 or p_ctr < -15:
			p_dy *= -1
		t = Trail(p_rect.center, (220, 220, 220), win)
		trail_group.add(t)


		if play_btn.draw(win):
			menu_click_fx.play()
			world_data, level_length, w = reset_level(level)
			p, moving_left, moving_right = reset_player()
			game_start = True
			main_menu = False
			game_won = False
			bonus = 0
			dc = 0
			penalty = 0
			penalty_time = 0

			global start_time

			if level == 1:
				start_time = pygame.time.get_ticks()
				penalty = 0 # no penalty
			else:
				if level == 2:
					penalty_time = 100000
					penalty = 2 # penalty at level 2
				elif level == 3:
					penalty_time = 200000
					penalty = 3 # penalty at level 3
			start_time = pygame.time.get_ticks() - penalty_time

		if leaderboard_btn.draw(win):
			pygame.time.wait(50)
			menu_click_fx.play()
			leaderboard_page = True
			main_menu = False

		if about_btn.draw(win):
			pygame.time.wait(50)
			menu_click_fx.play()
			about_page = True
			main_menu = False

		if controls_btn.draw(win):
			pygame.time.wait(50)
			menu_click_fx.play()
			controls_page = True
			main_menu = False

		if lvledit_btn.draw(win):
			pygame.time.wait(50)
			menu_click_fx.play()
			os.startfile("LevelEditor_run.exe")


		if exit_btn.draw(win):
			menu_click_fx.play()
			running = False

	elif leaderboard_page:
		cur.execute("SELECT * FROM leaderboard WHERE finish = 'YES' ORDER BY timescore ASC LIMIT 5")
		leaderboard_data = cur.fetchall()
		lf = open('Data/leaderboard.txt','w+')
		lf.write('--------------------------------------------------------------------------------------------- ')
		lf.write('   ||        Date&Time       || Diamonds || Finished ||    Penalty    || Bonus || Timescore || ')
		lf.write('---------------------------------------------------------------------------------------------')
		for row in leaderboard_data:
			lf.write('  ||' + equalspace(str(row[1]),' Date&Time ') + '||' + equalspace(str(row[5]),' Diamonds ') + '||'+equalspace(str(row[3]),' Finished ') + '||' + equalspace(str(row[4]),' Penalty')+ '||' + equalspace(str(row[6]),' Bonus ') + '||' + equalspace(str(row[2]),' Timescore') + '|| ')
		lf.seek(0)
		l_info = lf.read()

		MessageBox(win, leaderboard_font, 'Leaderboard',l_info)

		for row in leaderboard_data:
			row_text = 'f"{row[0]}. {row[2]} - Time: {row[3]}s - Diamonds: {row[5]}", font_color'

		if main_menu_btn.draw(win):
			menu_click_fx.play()
			pygame.time.wait(50)
			leaderboard_page = False
			main_menu = True

	elif about_page:
		MessageBox(win, about_font, 'GhostBusters', info)
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			pygame.time.wait(50)
			about_page = False
			main_menu = True

	elif controls_page:
		left_key.update()
		right_key.update()
		up_key.update()
		space_key.update()
		g_key.update()
		diamond_about_1.update()
		diamond_about_2.update()
		diamond_about_3.update()
		diamond_about_4.update()

		if main_menu_btn.draw(win):
			menu_click_fx.play()
			pygame.time.wait(50)
			controls_page = False
			main_menu = True

	elif exit_page:
		pass

	elif game_won:
		game_won_msg.update()
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			end_time = pygame.time.get_ticks()
			elapsed_time = end_time - start_time
			time_score = elapsed_time//1000 + bonus
			finish = True
			if penalty == 0:
				cur.execute(f"INSERT INTO leaderboard(date_time,timescore,finish,penalty,diamonds,bonus) VALUES (datetime('now','localtime'),{time_score},'YES','NO',{dc},{bonus})")
				con.commit()
				# print(" game won (no penalty), diamonds =",bonus//3,"time score :",time_score,"s")
			else:
				if penalty == 2:
					cur.execute(f"INSERT INTO leaderboard(date_time,timescore,finish,penalty,diamonds,bonus) VALUES (datetime('now','localtime'),{time_score},'YES','100s - LVL 2',{dc},{bonus})")
					con.commit()
				else:
					cur.execute(f"INSERT INTO leaderboard(date_time,timescore,finish,penalty,diamonds,bonus) VALUES (datetime('now','localtime'),{time_score},'YES','200s - LVL 3',{dc},{bonus})")
					con.commit()
				# print(" game won (penalty at level",penalty,", penalty time = +",penalty_time//1000,"s), diamonds =",bonus//3,"time score :",time_score,"s")
			pygame.time.wait(50)
			controls_page = False
			main_menu = True
			level = 1

			
	elif game_start:
		win.blit(MOON, (-40, -10))
		w.draw_world(win, screen_scroll)

		# Updating Objects ********************************************************

		bullet_group.update(screen_scroll, w)
		grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
		explosion_group.update(screen_scroll)
		trail_group.update()
		water_group.update(screen_scroll)
		water_group.draw(win)
		diamond_group.update(screen_scroll)
		diamond_group.draw(win)
		potion_group.update(screen_scroll)
		potion_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)

		enemy_group.update(screen_scroll, bullet_group, p)
		enemy_group.draw(win)

		if p.jump:
			t = Trail(p.rect.center, (220, 220, 220), win)
			trail_group.add(t)

		screen_scroll = 0
		p.update(moving_left, moving_right, w)
		p.draw(win)

		if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - WIDTH) \
			or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			bg_scroll -= screen_scroll


		# Collision Detetction ****************************************************

		if p.rect.bottom > HEIGHT:
			p.health = 0

		if pygame.sprite.spritecollide(p, water_group, False):
			p.health = 0
			level = 1

		if pygame.sprite.spritecollide(p, diamond_group, True):
			bonus += 3
			dc += 1
			diamond_fx.play()
			pass

		if pygame.sprite.spritecollide(p, exit_group, False):
			next_level_fx.play()
			level += 1
			if level <= MAX_LEVEL:
				health = p.health

				world_data, level_length, w = reset_level(level)
				p, moving_left, moving_right = reset_player() 
				p.health = health

				screen_scroll = 0
				bg_scroll = 0
			else:
				game_won = True


		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				p.health += 15
				health_fx.play()
				if p.health > 100:
					p.health = 100


		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1:
				if not enemy[0].hit:
					enemy[0].hit = True
					enemy[0].health -= 50
				bullet.kill()
			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					if not p.hit:
						p.hit = True
						p.health -= 20
						print(p.health)
					bullet.kill()

		# drawing variables *******************************************************

		if p.alive:
			color = (0, 255, 0)
			if p.health <= 40:
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
		pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i, 40), 1)
		
		if p.health <= 0:
			world_data, level_length, w = reset_level(level)
			p, moving_left, moving_right = reset_player() 

			screen_scroll = 0
			bg_scroll = 0

			end_time = pygame.time.get_ticks()
			elapsed_time = end_time - start_time
			time_score = elapsed_time//1000
			finish = False
			cur.execute(f"INSERT INTO leaderboard(date_time,timescore,finish,penalty,diamonds,bonus) VALUES (datetime('now','localtime'),{time_score},'NO','N.A.',{dc},'N.A.')")
			con.commit()
			# print("game lost (no bonus), time score :",time_score,"s")

			main_menu = True
			about_page = False
			controls_page = False
			leaderboard_page = False
			game_start = False

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 4, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()