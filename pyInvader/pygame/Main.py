import pygame
import os
import random
import time
import ClassObj
import Assets
import Function



WIN = pygame.display.set_mode((Assets.WINDOW_SIZE))
pygame.display.set_caption("WIP V0.04")

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    enemies = []
    health_containers = []
    enemy_vel = 1
    laser_vel = 6
    player_vel = 10
    wave_length = 5
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0
    player = ClassObj.Player(650, 750)

    def render_window():
        WIN.blit(Assets.MAP, (0,0)) #  map

        #   text and UI
        score_label = Assets.main_font.render(f"Score: {player.score}", 1, (255,255,255))
        lives_label = Assets.main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = Assets.main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (10,50))
        WIN.blit(score_label, (10,130))
        player.draw(WIN)

        for health in health_containers:
            health.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)
        
        if lost:
            lost_label = Assets.lost_font.render("You Lost!", 1, (255,255,255))
            WIN.blit(lost_label, (Assets.WINDOW_SIZE[0]/2 - lost_label.get_width()/2, 500)) #  center text

        pygame.display.update()

    while run:
        clock.tick(FPS)

        render_window()
        
        if len(enemies) == 0:  #    rendering enemies
            level += 1
            if lives < 5:
                lives += 1
            wave_length += 3
            if random.randint(0, 1000) * wave_length > 2000:
                health = ClassObj.Health(random.randrange(100, Assets.WINDOW_SIZE[0]-100), random.randrange(-1500, -100))
                health_containers.append(health)

            for i in range(wave_length):
                enemy = ClassObj.Enemy(random.randrange(100, Assets.WINDOW_SIZE[0]-100), random.randrange(-1500, -100), random.choice(['red','blue','green']))
                enemies.append(enemy)

                #if wave_length > 11 and random.randint(0, 1000) < 15: #and random.random() < 1 OLD health canister generation
                    

        for health in health_containers[:]:
            health.move(enemy_vel)                  #       health container movement, generation above ^
      
            if Function.collide(player, health):
                if player.health <= 50: 
                    player.health += 50
                    health_containers.remove(health)
                elif(player.health <= 99):
                    player.health = 100
                    health_containers.remove(health)

            elif health.y + health.get_height() > Assets.WINDOW_SIZE[1]:
                health_containers.remove(health)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if lives <= 0:
            lost = True
            lost_count += 1
                                                #   end game on loss
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        

        keys = pygame.key.get_pressed()#    player movement
        if keys[pygame.K_a] and player.x - player_vel + 20 > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + (player.get_width()-20) < Assets.WINDOW_SIZE[0] : #right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0 : #up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + (player.get_height()-5) < Assets.WINDOW_SIZE[1] : #down
            player.y += player_vel
        
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies[:]: #    enemy movement
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 3 * FPS) == 1:
                enemy.shoot()

            if Function.collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                player.score += 80

            elif enemy.y + enemy.get_height() > Assets.WINDOW_SIZE[1]:
                lives -= 1
                #player.knockout((FPS * 2)) needs init
                enemies.remove(enemy)

            elif player.health <= 0:
                lives -= 1
                player.health = 100
                #player.knockout((FPS * 2)) needs init
                
        player.move_lasers(-(laser_vel+5), enemies)

def main_menu():
    menu_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:

        WIN.blit(Assets.MAP, (0,0))
        menu_label = menu_font.render("Click anywhere to begin..", 1, (255,255,255))
        WIN.blit(menu_label, (Assets.WINDOW_SIZE[0]/2 - menu_label.get_width()/2, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()