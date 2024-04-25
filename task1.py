# Foster Cavender
# CS 1400 - MWF - 8:30

import pygame
from cell import Cell
from player import Player


SCREEN_WIDTH = 800  # Use constants here to be able to use in different places
SCREEN_HEIGHT = 800
CLOCK_TICK = 30
TITLE = "Window Name"
CELL_SIZE = 10


def main():
    # Setup the pygame window and clock
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    ##########
    # Set up game components
    #   images, sounds, other data necessary for game play
    ##########
    images = [[
        # player one
        pygame.image.load("crashtropolis_assets/images/blue-car.png"),
        pygame.image.load("crashtropolis_assets/images/blue-corner.png"),
        pygame.image.load("crashtropolis_assets/images/blue-straight.png")
    ], [
        # player two
        pygame.image.load("crashtropolis_assets/images/red-car.png"),
        pygame.image.load("crashtropolis_assets/images/red-corner.png"),
        pygame.image.load("crashtropolis_assets/images/red-straight.png")
    ]]

    background = pygame.image.load("crashtropolis_assets/images/grid.png")

    countdown = pygame.mixer.Sound("crashtropolis_assets/sounds/countdown.mp3")
    crash = pygame.mixer.Sound("crashtropolis_assets/sounds/crash.wav")

    turn = [pygame.mixer.Sound("crashtropolis_assets/sounds/turn-1.mp3"),
            pygame.mixer.Sound("crashtropolis_assets/sounds/turn-2.mp3")]

    pygame.mixer.music.load("crashtropolis_assets/sounds/background-music.mp3")
    pygame.mixer.music.play(-1, 0.0)

    ##########
    # Set up game data
    ##########
    responsible = 0

    inputs = [[False, False, False, False], [False, False, False, False]]

    # create the player objects
    players = [
        Player(0, 180, [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2]),
        Player(1, 180, [SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 2])
    ]

    # create the cell objects
    cell_grid = []
    for x in range(0, SCREEN_WIDTH // CELL_SIZE):
        cell_grid.append([])
        for y in range(0, SCREEN_HEIGHT // CELL_SIZE):
            cell_grid[x].append(Cell([x, y], CELL_SIZE, images))

    ##########
    # Game Loop
    ##########
    game_over = False
    running = True
    while running:
        ##########
        # Get Input/Events
        ##########
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicked the window's X button
                running = False

        ##########
        # Update state of components/data
        ##########
        #### Always Update ####
        keys = pygame.key.get_pressed()
        inputs[0][0] = True if keys[pygame.K_w] else False
        inputs[0][1] = True if keys[pygame.K_s] else False
        inputs[0][2] = True if keys[pygame.K_a] else False
        inputs[0][3] = True if keys[pygame.K_d] else False
        inputs[1][0] = True if keys[pygame.K_UP] else False
        inputs[1][1] = True if keys[pygame.K_DOWN] else False
        inputs[1][2] = True if keys[pygame.K_LEFT] else False
        inputs[1][3] = True if keys[pygame.K_RIGHT] else False

        #### Update if Game is Not Over ####
        if not game_over:
            for i in range(0, len(players)):
                # move the player
                players[i].move()

                # currently occupied cell index
                cell_x = int(players[i].pos[0] // CELL_SIZE)
                cell_y = int(players[i].pos[1] // CELL_SIZE)

                # check for player offscreen
                if players[i].offscreen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    # play game over sounds
                    pygame.mixer.Sound.play(crash)
                    pygame.mixer.music.stop()

                    # start the game over music
                    pygame.mixer.music.load("./crashtropolis_assets/sounds/gameover-music.mp3")
                    pygame.mixer.music.play(-1, 0.0)

                    game_over = True
                    responsible = i

                    continue

                # update the cells
                change = players[i].direction_change(inputs)
                if change:
                    pygame.mixer.Sound.play(turn[i])
                if cell_grid[cell_x][cell_y].update_cell(
                    players[i].direction,
                    players[i].last_dir,
                    i,
                    change
                ):
                    # play game over sounds
                    pygame.mixer.Sound.play(crash)  
                    pygame.mixer.music.stop()

                    # start the game over music
                    pygame.mixer.music.load("./crashtropolis_assets/sounds/gameover-music.mp3")
                    pygame.mixer.music.play(-1, 0.0)

                    game_over = True
                    responsible = i

        #### Update if Game is Over ####
        else:
            if keys[pygame.K_SPACE] and game_over:
                ### Do Stuff to Reset Game ###
                # reset players
                players = [
                    Player(0, 180, [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2]),
                    Player(1, 180, [SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 2])
                ]

                # reset cell_grid objects
                for x in range(len(cell_grid)):
                    for y in range(len(cell_grid[0])):
                        cell_grid[x][y].reset()

                # start the background music
                pygame.mixer.music.load("crashtropolis_assets/sounds/background-music.mp3")
                pygame.mixer.music.play(-1, 0.0)

                game_over = False  # restart the game
        ##########
        # Update Display
        ##########
        #### Always Display ####
        #### Display while Game is being played ####
        if not game_over:
            screen.fill("black")
            screen.blit(background, [0, 0])
            for x in range(len(cell_grid)):
                for y in range(len(cell_grid[0])):
                    cell_grid[x][y].draw(screen)

        #### Display while Game is Over ####
        else:
            font = pygame.font.SysFont("timesnewroman", 35)
            win_text = font.render("Player " + str(responsible + 1) + " wins! Press space to play again.", True, "white")
            win_text_rect = win_text.get_rect()
            win_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(win_text, win_text_rect)

        #### Draw changes the screen ####
        pygame.display.flip()

        ##########
        # Define the refresh rate of the screen
        ##########
        clock.tick(CLOCK_TICK)


main()
