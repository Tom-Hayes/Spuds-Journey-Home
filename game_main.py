#### ====================================================================================================================== ####
#############										   IMPORTS													#############
#### ====================================================================================================================== ####
import pygame
import random
import math
import csv

# import the pygame constants (specifically the key codes and event types)
from pygame.locals import *

#### ====================================================================================================================== ####
#############										 INITIALIZE												   #############
#### ====================================================================================================================== ####

# constants for representing the states from the initial toy
STATE_OPEN = 0
STATE_WAIT = 1
STATE_MOVE = 2
STATE_RIDE = 3
STATE_WIN = 4
STATE_OPEN_2 = 5

# constants for accessing the attributes of the mouse
MOUSE_LMB = 0
MOUSE_RMB = 1
MOUSE_X = 2
MOUSE_Y = 3

# the dimensions of the view used for rendering (i.e., the window)
view_wid = 1200
view_hgt = 800

# the dimensions of the game world
world_wid = 10000
world_hgt = 10000

# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 40
delta_time = 1 / frame_rate
chick_time = 0


# function to read in the game map from a csv file
def read_csv(file_name):
    with open(file_name) as file:
        csvreader = csv.reader(file)
        map_array = []
        for row in csvreader:
            map_array.append(row)

        return map_array

# load in some music poggggggg

pygame.mixer.init()
pygame.mixer.music.load("Music/theme.mp3")

# define Impassable type (nothing can pass through these tiles)
class Impassable:

    def __init__(self):
        self.wid = 100
        self.hgt = 100
        self.x = 0
        self.y = 0

class Rock(Impassable):

    def __init__(self):
        super().__init__()
        load_rock = pygame.image.load("Tiles/rock.png")
        self.image = pygame.transform.scale(load_rock, (100, 100))

class Water(Impassable):

    def __init__(self):
        super().__init__()
        load_water = pygame.image.load("Tiles/water.png")
        self.image = pygame.transform.scale(load_water, (100, 100))

class Stone(Impassable):

    def __init__(self):
        super().__init__()
        load_stone = pygame.image.load("Tiles/stone.png")
        self.image = pygame.transform.scale(load_stone, (100, 100))

class ImpassableGrass(Impassable):

    def __init__(self):
        super().__init__()
        load_grass_i = pygame.image.load("Tiles/grass.png")
        self.image = pygame.transform.scale(load_grass_i, (100, 100))

# define grass class (can be walked on)
class Grass:

    def __init__(self):
        self.wid = 100
        self.hgt = 100
        self.x = 0
        self.y = 0
        load_grass = pygame.image.load("Tiles/grass.png")
        self.image = pygame.transform.scale(load_grass, (100, 100))


# define Cart class
class Cart:

    def __init__(self):
        self.rad = 20
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0
        self.dir = 0

        load_cart = pygame.image.load("Characters/cart.png")
        self.image = pygame.transform.scale(load_cart, (50, 50))

# define Guard class
class Guard:

    def __init__(self):
        self.rad = 10
        self.x = 0
        self.y = 0

        self.dx = 0
        self.dy = 0

        self.type = 0

        load_guard_left = pygame.image.load("Characters/guardleft.png")
        load_guard_right = pygame.image.load("Characters/guardright.png")
        scale_guard_left = pygame.transform.scale(load_guard_left, (75, 75))
        scale_guard_right = pygame.transform.scale(load_guard_right, (75, 75))
        self.image = scale_guard_right
        self.image_right = scale_guard_right
        self.image_left = scale_guard_left

# load in some of the constant images that don't move
load_pound = pygame.image.load("Tiles/Pound.png")
pound = pygame.transform.scale(load_pound, (200, 200))

load_home = pygame.image.load("Tiles/Home.png")
home = pygame.transform.scale(load_home, (200, 200))

load_house_front = pygame.image.load("Tiles/House_Front.png")
house_front = pygame.transform.scale(load_house_front, (200, 200))

load_house_back = pygame.image.load("Tiles/House_Back.png")
house_back = pygame.transform.scale(load_house_back, (200, 200))

load_pig = pygame.image.load("Characters/pig.png")
pig = pygame.transform.scale(load_pig, (50, 80))

load_cat = pygame.image.load("Characters/cat.png")
cat = pygame.transform.scale(load_cat, (38, 38))

load_cat_white = pygame.image.load("Characters/catwhite.png")
cat_white = pygame.transform.scale(load_cat_white, (38, 38))

load_fence = pygame.image.load("Tiles/fence.png")
fence = pygame.transform.scale(load_fence, (10, 100))

load_key = pygame.image.load("Tiles/key.png")
key = pygame.transform.scale(load_key, (30, 30))

load_fish = pygame.image.load("Tiles/fish.png")
fish = pygame.transform.scale(load_fish, (30, 30))

load_potion = pygame.image.load("Tiles/potion.png")
potion = pygame.transform.scale(load_potion, (30, 30))

#load in text images
load_chick_text = pygame.image.load("Text/chick_text.png")
chick_text = pygame.transform.scale(load_chick_text, (350, 150))

load_pig_text = pygame.image.load("Text/pig_text.png")
pig_text = pygame.transform.scale(load_pig_text, (350, 150))

load_cat_text = pygame.image.load("Text/cat_text.png")
cat_text = pygame.transform.scale(load_cat_text, (350, 250))

load_white_cat_text_1 = pygame.image.load("Text/white_cat_text_1.png")
white_cat_text_1 = pygame.transform.scale(load_white_cat_text_1, (350, 100))

load_white_cat_text_2 = pygame.image.load("Text/white_cat_text_2.png")
white_cat_text_2 = pygame.transform.scale(load_white_cat_text_2, (350, 100))

# load in game screens
load_paused = pygame.image.load("Text/paused.png")
paused = pygame.transform.scale(load_paused, (800, 500))

load_win = pygame.image.load("Text/win_screen.png")
win_screen = pygame.transform.scale(load_win, (view_wid, view_hgt))

load_title = pygame.image.load("Text/title.png")
title_screen = pygame.transform.scale(load_title, (view_wid, view_hgt))

load_instructions = pygame.image.load("Text/instructions.png")
instructions_screen = pygame.transform.scale(load_instructions, (view_wid, view_hgt))

# load in the characters that animate
load_chick_1 = pygame.image.load("Characters/chick1.png")
load_chick_2 = pygame.image.load("Characters/chick2.png")
load_chick_3 = pygame.image.load("Characters/chick3.png")
scale_chick_1 = pygame.transform.scale(load_chick_1, (25, 25))
scale_chick_2 = pygame.transform.scale(load_chick_2, (25, 25))
scale_chick_3 = pygame.transform.scale(load_chick_3, (25, 25))
chick = [scale_chick_1, scale_chick_2, scale_chick_3]


#### ====================================================================================================================== ####
#############										   handle_input													#############
#### ====================================================================================================================== ####

def get_all_inputs():
    # get the state of the mouse (i.e., button states and pointer position)
    mouse_dict = {}
    (mouse_dict[MOUSE_LMB], _, mouse_dict[MOUSE_RMB]) = pygame.mouse.get_pressed()
    (mouse_dict[MOUSE_X], mouse_dict[MOUSE_Y]) = pygame.mouse.get_pos()

    # get the state of the keyboard
    keybd_tupl = pygame.key.get_pressed()

    # look in the event queue for the quit event
    quit_ocrd = False
    for evnt in pygame.event.get():
        if evnt.type == QUIT:
            quit_ocrd = True

    # return all possible inputs
    return mouse_dict, keybd_tupl, quit_ocrd


# **********************************************************************
# **********************************************************************

def generate_background_surface(list_of_impassables, list_of_grasses, map_array):
    # create a new surface to hold the background and fill with colour
    backgd_sfc = pygame.Surface((world_wid, world_hgt))

    y = 0
    for row in map_array:
        x = 0
        for columnCell in row:
            # Check to see what colour the tile should be
            if columnCell == "w":
                w = Water()
                w.x = x
                w.y = y
                list_of_impassables.append(w)
                backgd_sfc.blit(w.image, (w.x, w.y))
            elif columnCell == "i":
                i = ImpassableGrass()
                i.x = x
                i.y = y
                list_of_impassables.append(i)
                backgd_sfc.blit(i.image, (i.x, i.y))
            elif columnCell == "g":
                g = Grass()
                g.x = x
                g.y = y
                list_of_grasses.append(g)
                backgd_sfc.blit(g.image, (g.x, g.y))
            elif columnCell == 's':
                s = Stone()
                s.x = x
                s.y = y
                list_of_impassables.append(s)
                backgd_sfc.blit(s.image, (s.x, s.y))
            elif columnCell == "r":
                r = Rock()
                r.x = x
                r.y = y
                list_of_impassables.append(r)
                backgd_sfc.blit(r.image, (r.x, r.y))
            x = x + 100
        y = y + 100

    # Load the list of non-movers
    backgd_sfc.blit(pound, (1500, 1000))
    backgd_sfc.blit(home, (8100, 1000))
    backgd_sfc.blit(house_front, (7900, 1000))
    backgd_sfc.blit(house_front, (7500, 1000))
    backgd_sfc.blit(house_front, (7300, 1000))
    backgd_sfc.blit(house_back, (7900, 1800))
    backgd_sfc.blit(house_back, (8100, 1800))

    backgd_sfc.blit(pig, (3120, 4325))
    backgd_sfc.blit(cat, (3338, 8440))
    backgd_sfc.blit(cat_white, (6931, 8236))
    
    return backgd_sfc


#### ====================================================================================================================== ####
#############											 MAIN													 #############
#### ====================================================================================================================== ####

def main():
    # initialize pygame
    pygame.init()

    # create a clock
    clock = pygame.time.Clock()
    chick_time = 0

    # create the window and set the caption of the window
    view_sfc = pygame.display.set_mode((view_wid, view_hgt))
    pygame.display.set_caption('Spud\'s Journey Home')

    # play the music
    pygame.mixer.music.play(loops = -1)

    # spud is represented using separate variables, with no encapsulation
    spud_x = 1540
    spud_y = 1200

    # this is the radius of the spud
    spud_rad = 10

    # dimensions of spud
    spud_width = 20
    spud_height = 20

    # load in the 4 image directions of spud
    spud_load_left = pygame.image.load("Spud/Left.png")
    spud_left = pygame.transform.scale(spud_load_left, (40, 40))
    spud_load_right = pygame.image.load("Spud/Right.png")
    spud_right = pygame.transform.scale(spud_load_right, (40, 40))
    spud_load_up = pygame.image.load("Spud/Up.png")
    spud_up = pygame.transform.scale(spud_load_up, (40, 40))
    spud_load_down = pygame.image.load("Spud/Down.png")
    spud_down = pygame.transform.scale(spud_load_down, (40, 40))

    # these are the flags for the direction Spud is moving
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    # this is the radius of interaction between the spud and a cart
    # i.e., the spud must be within this many units of a cart in order to ride
    ride_rad = 50

    # this is the maximum velocity of a moving cart
    max_v = 20

    # this is the index of the cart that the spud is currently riding
    spud_on_which_cart = -1

    # the camera is the rectangle of the world that will be rendered to the window
    camera_rect = pygame.Rect(spud_x - view_wid // 2, spud_y - view_hgt // 2, view_wid, view_hgt)

    # create lists of instances of the three different kinds of game objects
    list_of_impassables = []
    list_of_grasses = []
    list_of_non_movers = []

    # create and set initial positions of carts
    number_of_carts = 1
    list_of_carts = []
    c1 = Cart()
    c1.x = 3500
    c1.y = 9000
    list_of_carts.append(c1)

    # create and set initial positions of guards
    number_of_guards = 20
    list_of_guards = []
    g1 = Guard()
    g1.x = 3600
    g1.y = 8200
    g1.dx = 3
    g1.dy = 10
    g1.type = 1
    list_of_guards.append(g1)

    g2 = Guard()
    g2.x = 3600
    g2.y = 8000
    g2.dx = 8
    g2.dy = 8
    g2.type = 1
    list_of_guards.append(g2)

    g3 = Guard()
    g3.x = 3600
    g3.y = 7500
    g3.dx = 15
    g3.dy = 15
    g3.type = 1
    list_of_guards.append(g3)

    g4 = Guard()
    g4.x = 3600
    g4.y = 7200
    g4.dx = 18
    g4.dy = 18
    g4.type = 1
    list_of_guards.append(g4)

    g5 = Guard()
    g5.x = 3600
    g5.y = 6900
    g5.dx = 10
    g5.dy = 10
    g5.type = 1
    list_of_guards.append(g5)

    g6 = Guard()
    g6.x = 3600
    g6.y = 7100
    g6.dx = 20
    g6.dy = 20
    g6.type = 1
    list_of_guards.append(g6)

    g7 = Guard()
    g7.x = 3600
    g7.y = 7700
    g7.dx = 27
    g7.dy = 27
    g7.type = 1
    list_of_guards.append(g7)

    # type 2 guards
    g8 = Guard()
    g8.x = 4800
    g8.y = 7900
    g8.dx = 10
    g8.dy = 10
    g8.type = 2
    list_of_guards.append(g8)

    g9 = Guard()
    g9.x = 4800
    g9.y = 7300
    g9.dx = 6
    g9.dy = 10
    g9.type = 2
    list_of_guards.append(g9)

    g10 = Guard()
    g10.x = 4800
    g10.y = 7200
    g10.dx =9
    g10.dy = 10
    g10.type = 2
    list_of_guards.append(g10)

    g11 = Guard()
    g11.x = 4800
    g11.y = 7400
    g11.dx = 12
    g11.dy = 10
    g11.type = 2
    list_of_guards.append(g11)

    g12 = Guard()
    g12.x = 4800
    g12.y = 7600
    g12.dx = 5
    g12.dy = 10
    g12.type = 2
    list_of_guards.append(g12)

    g13 = Guard()
    g13.x = 4800
    g13.y = 7800
    g13.dx = 12
    g13.dy = 10
    g13.type = 2
    list_of_guards.append(g13)

    g14 = Guard()
    g14.x = 4800
    g14.y = 8000
    g14.dx = 3
    g14.dy = 10
    g14.type = 2
    list_of_guards.append(g14)

    g15 = Guard()
    g15.x = 4800
    g15.y = 8200
    g15.dx = 13
    g15.dy = 10
    g15.type = 2
    list_of_guards.append(g15)

    g16 = Guard()
    g16.x = 4800
    g16.y = 8400
    g16.dx = 7
    g16.dy = 10
    g16.type = 2
    list_of_guards.append(g16)

    g17 = Guard()
    g17.x = 4800
    g17.y = 8500
    g17.dx = 25
    g17.dy = 10
    g17.type = 2
    list_of_guards.append(g17)

    # type 3 guards
    g18 = Guard()
    g18.x = 4800
    g18.y = 8700
    g18.dx = 18
    g18.dy = 10
    g18.type = 3
    list_of_guards.append(g18)

    g19 = Guard()
    g19.x = 4800
    g19.y = 8900
    g19.dx = 30
    g19.dy = 10
    g19.type = 3
    list_of_guards.append(g19)

    g20 = Guard()
    g20.x = 4800
    g20.y = 9000
    g20.dx = 25
    g20.dy = 10
    g20.type = 3
    list_of_guards.append(g20)


    # call helper to get contents of csv file
    map = read_csv("Map/map_data.csv")

    # create a surface that will be used to hold the image of the world
    backgd_surf = generate_background_surface(list_of_impassables, list_of_grasses, map)

    # this is the initial game state and a variable to hold the state while paused
    game_state = STATE_OPEN
    last_state = -1

    # this variable represents the fence's state
    fence_up = True

    # flag to check and see if you've traded fish with the cat
    traded = False

    # list of items Spud has
    items = {'potion': False, 'key': False, 'fish1': False, 'fish2': False, 'fish3': False, 'fish4': False, 'fish5': False}

    # flag for is you've beaten the game
    at_house = False

    # this prevents states from changing too quickly by ignoring keyboard input for a moment
    # immediately after a state change; it should be set to half the frame rate, meaning
    # that after the user causes a state change the keyboard will be ignored for 0.5 seconds
    cooldown_timer = 0

    # the game loop is a postcondition loop controlled using a Boolean flag
    closed_flag = False
    while not closed_flag:

        #####################################################################################################
        # this is the "inputs" phase of the game loop, where player input is retrieved and stored
        #####################################################################################################

        # get a dictionary for the mouse, a tuple for the keyboard, and a boolean for the window close event
        mouse_dict, keybd_tupl, closed_flag = get_all_inputs()

        # if we are ignoring keyboard input because of a state change
        if cooldown_timer > 0:
            # clear the keyboard tuple and reduce the cooldown timer
            keybd_tupl = tuple([0] * 323)
            cooldown_timer -= 1

        #####################################################################################################
        # this is the "update" phase of the game loop, where the changes to the game world are handled
        #####################################################################################################

        # flags for location markers
        at_chick = False
        at_pig = False
        at_white_cat = False
        at_black_cat = False

        # by default the game state will not change
        next_state = game_state

        # initial title screen
        if game_state == STATE_OPEN:
            # player will press enter to continue
            if keybd_tupl[K_RETURN]:
                next_state = STATE_OPEN_2
                cooldown_timer = frame_rate // 2

        # instructions screen
        if game_state == STATE_OPEN_2:
            # player will press enter to start the game
            if keybd_tupl[K_RETURN]:
                next_state = STATE_MOVE
                cooldown_timer = frame_rate // 2


        # if the game is currently paused then nothing is updated but the game can be unpaused
        if game_state == STATE_WAIT:
            # press escape again to unpause the game
            if keybd_tupl[K_ESCAPE]:
                next_state = last_state
                cooldown_timer = frame_rate // 2

        # if the game is currently in a movement state then spud can be moved
        if game_state == STATE_MOVE or game_state == STATE_RIDE:

            # the user can pause the game with the escape key
            if keybd_tupl[K_ESCAPE]:
                next_state = STATE_WAIT
                last_state = game_state
                cooldown_timer = frame_rate // 2

            # update the positions of the Guards
            for i in range(number_of_guards):
                if list_of_guards[i].type == 1 :
                    # guards will walk back and forth
                    if list_of_guards[i].x + list_of_guards[i].dx> 3400 and list_of_guards[i].x + list_of_guards[i].dx \
                            < 4325:
                        list_of_guards[i].x += list_of_guards[i].dx
                        if list_of_guards[i].dx > 0 :
                            # moving right
                            list_of_guards[i].image = list_of_guards[i].image_right
                        else:
                            list_of_guards[i].image = list_of_guards[i].image_left
                    else:
                        list_of_guards[i].dx = list_of_guards[i].dx * -1
                elif list_of_guards[i].type == 2 :
                    # guards will walk back and forth
                    if list_of_guards[i].x + list_of_guards[i].dx > 4800 and list_of_guards[i].x + list_of_guards[i].dx \
                            < 5600:
                        list_of_guards[i].x += list_of_guards[i].dx
                        if list_of_guards[i].dx > 0 :
                            # moving right
                            list_of_guards[i].image = list_of_guards[i].image_right
                        else:
                            list_of_guards[i].image = list_of_guards[i].image_left
                    else:
                        list_of_guards[i].dx = list_of_guards[i].dx * -1
                elif list_of_guards[i].type == 3 :
                    # guards will walk back and forth
                    if list_of_guards[i].x + list_of_guards[i].dx > 4800 and list_of_guards[i].x + list_of_guards[i].dx \
                            < 6800:
                        list_of_guards[i].x += list_of_guards[i].dx
                        if list_of_guards[i].dx > 0 :
                            # moving right
                            list_of_guards[i].image = list_of_guards[i].image_right
                        else:
                            list_of_guards[i].image = list_of_guards[i].image_left
                    else:
                        list_of_guards[i].dx = list_of_guards[i].dx * -1
            # update the positions of the carts using their attributes
            for cart in list_of_carts:

                # position is increased by velocity
                next_cart_x = cart.x + cart.dx
                next_cart_y = cart.y + cart.dy

                # this flags is used for collision detection
                cart_collided_with_impassable = False
                cart_collided_with_guard = False

                # check the position of the spud against each of the impassables
                for impassable in list_of_impassables:

                    # by testing to ensure that the x value of spud is either less than the left edge of the impasssable
                    # or greater than the right edge of the impassable (and checking the y value of the spud in the same way),
                    # then we can determine if there has been a collision between a point and a rectangle
                    if not (
                            next_cart_x + 50 < impassable.x or next_cart_x >= impassable.x + impassable.wid or \
                            next_cart_y + 50 < impassable.y or next_cart_y >= impassable.y + impassable.hgt):
                        cart_collided_with_impassable = True
                        cart.dx = 0
                        cart.dy = 0
                        cart.ddx = 0
                        cart.ddy = 0

                # check to see if the cart has collided with the guard
                for guard in list_of_guards:
                    if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(guard.x, guard.y, 62, 62)):
                        cart_collided_with_guard = True

                if cart_collided_with_guard:
                    # reset spud's position to the pound and reset the cart to its original place
                    spud_x = 1550
                    spud_y = 1200
                    spud_on_which_cart = -1
                    cart.x = 3500
                    cart.y = 9000
                    cart.dx = 0
                    cart.dy = 0
                    cart.ddx = 0
                    cart.ddy = 0
                    next_cart_x = cart.x + cart.dx
                    next_cart_y = cart.y + cart.dy
                    cart_collided_with_guard = False
                    next_state = STATE_MOVE

                # check to see if cart collided with fence
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(7000, 8300, 10, 100)):
                    fence_up = False

                # check to see if cart collided with potion
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(4700, 5800, 100, 100)):
                    items['potion'] = True

                # check to see if cart collided with fish1
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(1600, 5200, 100, 100)):
                    items['fish1'] = True

                # check to see if cart collided with fish2
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(2900, 6800, 100, 100)):
                    items['fish2'] = True

                # check to see if cart collided with fish3
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(2500, 1000, 100, 100)):
                    items['fish3'] = True

                # check to see if cart collided with fish4
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(6400, 600, 100, 100)):
                    items['fish4'] = True

                # check to see if cart collided with fish5
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(4400, 5800, 100, 100)):
                    items['fish5'] = True

                # check to see if cart collided with chick
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(1700, 8800, 100, 100)):
                    at_chick = True

                # check to see if cart is at house
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(3100, 4300, 100, 100)):
                    at_pig = True

                # check to see if cart collided with with white cat
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(6900, 8200, 100, 100)):
                    at_white_cat = True

                # check to see if cart collided with black cat
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(3300, 8400, 100, 100)):
                    at_black_cat = True

                # check to see if cart collided with black cat
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(8100, 1000, 200, 200)):
                    at_house = True

                # check to see if cart collided with key
                if Rect(next_cart_x, next_cart_y, 50, 50).colliderect(Rect(6800, 2800, 100, 100)):
                    items['key'] = True

                # if there has been no collision then the cart can move
                if not cart_collided_with_impassable and not cart_collided_with_guard:
                    cart.x = next_cart_x
                    cart.y = next_cart_y

                # velocity is increased by acceleration
                cart.dx += cart.ddx
                cart.dy += cart.ddy

                # ...but there is a maximum possible velocity that the magnitude cannot exceed
                cur_v = pygame.math.Vector2(cart.dx, cart.dy)
                if math.sqrt(cur_v.x ** 2 + cur_v.y ** 2) > max_v:
                    cur_v = cur_v.normalize() * max_v

                # velocity is also reduced by friction
                cart.dx = cur_v.x * .99
                cart.dy = cur_v.y * .99

                # acceleration is always set to zero unless it is a cart that the spud is riding
                cart.ddx = 0
                cart.ddy = 0

            # if the spud is currently riding a cart then the control scheme is more akin to a racing game
            if game_state == STATE_RIDE:

                # if the user is pressing up then they want to accelerate in the current direction the cart is facing
                if keybd_tupl[K_UP]:
                    list_of_carts[spud_on_which_cart].ddx = + math.cos(
                        math.radians(list_of_carts[spud_on_which_cart].dir))
                    list_of_carts[spud_on_which_cart].ddy = + math.sin(
                        math.radians(list_of_carts[spud_on_which_cart].dir))

                # if the user is pressing down then they want to accelerate in the opposite direction the cart is facing
                if keybd_tupl[K_DOWN]:
                    list_of_carts[spud_on_which_cart].ddx = -math.cos(
                        math.radians(list_of_carts[spud_on_which_cart].dir))
                    list_of_carts[spud_on_which_cart].ddy = -math.sin(
                        math.radians(list_of_carts[spud_on_which_cart].dir))

                # if the user presses left then they want to turn counterclockwise
                if keybd_tupl[K_LEFT]:
                    if items['potion'] == True:
                        # evil potion makes the controls reversed
                        list_of_carts[spud_on_which_cart].dir = (list_of_carts[spud_on_which_cart].dir + 3) % 360
                    else:
                        list_of_carts[spud_on_which_cart].dir = (list_of_carts[spud_on_which_cart].dir - 3) % 360

                # if the user presses right then they want to turn clockwise
                if keybd_tupl[K_RIGHT]:
                    if items['potion'] == True:
                        # evil potion makes the controls reversed
                        list_of_carts[spud_on_which_cart].dir = (list_of_carts[spud_on_which_cart].dir - 3) % 360
                    else:
                        list_of_carts[spud_on_which_cart].dir = (list_of_carts[spud_on_which_cart].dir + 3) % 360

                # if the user presses return then they want to exit the cart
                if keybd_tupl[K_RETURN]:
                    spud_x = list_of_carts[spud_on_which_cart].x + math.cos(
                        math.radians(list_of_carts[spud_on_which_cart].dir + 90)) * list_of_carts[
                                 spud_on_which_cart].rad + spud_rad
                    spud_y = list_of_carts[spud_on_which_cart].y + math.sin(
                        math.radians(list_of_carts[spud_on_which_cart].dir + 90)) * list_of_carts[
                                 spud_on_which_cart].rad + spud_rad
                    spud_on_which_cart = -1
                    next_state = STATE_MOVE
                    cooldown_timer = frame_rate // 2

                # center the camera on the position of the cart
                camera_rect.center = (list_of_carts[spud_on_which_cart].x, list_of_carts[spud_on_which_cart].y)

            # if the spud is currently riding a cart then the control scheme is more akin to a top-down action game
            if game_state == STATE_MOVE:

                # the future position of the spud can be initialized
                next_spud_x = spud_x
                next_spud_y = spud_y

                # spud moves according to user input with the arrow keys
                if keybd_tupl[K_UP]:
                    next_spud_y = spud_y - 15
                    moving_up = True
                if keybd_tupl[K_DOWN]:
                    next_spud_y = spud_y + 15
                    moving_down = True
                if keybd_tupl[K_LEFT]:
                    next_spud_x = spud_x - 15
                    moving_left = True
                if keybd_tupl[K_RIGHT]:
                    next_spud_x = spud_x + 15
                    moving_right = True

                # these flags are used for collision detection
                spud_collided_with_impassable = False
                spud_collided_with_cart = False
                spud_collided_with_guard = False
                spud_collided_with_fence = False

                # check to see if Spud has collided with the key
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((6800, 2800, 100, 100)):
                    items['key'] = True

                # check to see if Spud has collided with potion
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((4700, 5800, 100, 100)):
                    items['potion'] = True

                # check to see if Spud has collided with fish1
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((1600, 5200, 100, 100)):
                    items['fish1'] = True

                # check to see if Spud has collided with fish2
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((2900, 6800, 100, 100)):
                    items['fish2'] = True

                # check to see if Spud has collided with fish3
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((2500, 1000, 100, 100)):
                    items['fish3'] = True

                # check to see if Spud has collided with fish4
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((6400, 600, 100, 100)):
                    items['fish4'] = True

                # check to see if Spud has collided with fish5
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((4400, 5800, 100, 100)):
                    items['fish5'] = True

                # check to see if Spud has collided with chick
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((1700, 8800, 100, 100)):
                    at_chick = True

                # check to see if Spud has collided with pig
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((3100, 4300, 100, 100)):
                    at_pig = True

                # check to see if Spud has collided with white cat
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((6900, 8200, 100, 100)):
                    at_white_cat = True

                # check to see if Spud has collided with black cat
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((3300, 8400, 100, 100)):
                    at_black_cat = True

                # check to see if Spud is at house
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((8100, 1000, 200, 200)):
                    at_house = True

                # check to see if Spud has collided with the fence
                if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((7000, 8300, 10, 100)) and items['key'] == False and fence_up:
                    spud_collided_with_fence = True
                elif Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect((7000, 8300, 10, 100)) and items['key'] == True:
                    fence_up = False

                # check the position of the spud against each of the guards
                for guard in list_of_guards:
                    if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect(Rect(guard.x, guard.y, 62, 62)):
                        spud_collided_with_guard = True

                # check the position of the spud against each of the impassables
                for impassable in list_of_impassables:

                    # by testing to ensure that the x value of the spud is either less than the left edge of the impassable
                    # or greater than the right edge of the impassable (and checking the y value of the spud in the same way),
                    # then we can determine if there has been a collision between a point and a rectangle
                    if not (next_spud_x + spud_width < impassable.x or next_spud_x >= impassable.x + impassable.wid or next_spud_y + spud_height < impassable.y or next_spud_y >= impassable.y + impassable.hgt):
                        spud_collided_with_impassable = True

                # check the position of the spud against each of the carts
                for i in range(len(list_of_carts)):
                    cart = list_of_carts[i]

                    # if spud is trying to ride a cart
                    if keybd_tupl[K_RETURN]:

                        # the spud will ride the cart only if the spud is within the interaction radius
                        if ((cart.x - next_spud_x) ** 2 + (cart.y - next_spud_y) ** 2) < (
                                (spud_rad + ride_rad + cart.rad) ** 2):
                            spud_on_which_cart = i
                            next_state = STATE_RIDE
                            cooldown_timer = frame_rate // 2

                    else:

                        # otherwise the spud may have collided with the cart
                        if Rect(next_spud_x, next_spud_y, spud_width + 20, spud_height + 20).colliderect(Rect(cart.x, cart.y, 41, 41)):
                            spud_collided_with_cart = True

                if spud_collided_with_guard:
                    # back to the pound :'(
                    spud_x = 1550
                    spud_y = 1200

                # if there has been no collision then the spud can move
                if not spud_collided_with_cart and not spud_collided_with_impassable and not spud_collided_with_guard \
                        and not spud_collided_with_fence:
                    spud_x = next_spud_x
                    spud_y = next_spud_y

                # center the camera on the position of the spud
                camera_rect.center = (spud_x, spud_y)

        #####################################################################################################
        #                                              Render                                               #
        #####################################################################################################

        # if the game is started and we are on the title screen
        if game_state == STATE_OPEN:
            # draw the title screen
            view_sfc.fill((255, 255, 255))
            view_sfc.blit(title_screen, (0, 0))

        elif game_state == STATE_OPEN_2:
            # draw the instruction screen
            view_sfc.fill((255, 255, 255))
            view_sfc.blit(instructions_screen, (0, 0))


        else:

            # clear the display with black
            view_sfc.fill((0, 0, 0))

            # blit the image of the "world"
            view_sfc.blit(backgd_surf, (0, 0), camera_rect)

            # if the fence is still standing, show it
            if fence_up:
                backgd_surf.blit(fence, (7000, 8300))
            else:
                g = Grass()
                g.x = 7000
                g.y = 8300
                backgd_surf.blit(g.image, (g.x, g.y))

            # if the potion is still there, show it
            if items['potion'] == False:
                backgd_surf.blit(potion, (4735, 5835))
            else:
                g = Grass()
                g.x = 4700
                g.y = 5800
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(potion, (1162 , 2))

            # if the key is still there, show it
            if items['key'] == False:
                backgd_surf.blit(key, (6840, 2840))
            else:
                g = Grass()
                g.x = 6800
                g.y = 2800
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(key, (0 , 0))

            # if the fish1 is still there, show it
            if items['fish1'] == False:
                backgd_surf.blit(fish, (1635, 5235))
            else:
                g = Grass()
                g.x = 1600
                g.y = 5200
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(fish, (30 , 0))

            # if the fish2 is still there, show it
            if items['fish2'] == False:
                backgd_surf.blit(fish, (2935, 6835))
            else:
                g = Grass()
                g.x = 2900
                g.y = 6800
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(fish, (60, 0))

            # if the fish3 is still there, show it
            if items['fish3'] == False:
                backgd_surf.blit(fish, (2535, 1035))
            else:
                g = Grass()
                g.x = 2500
                g.y = 1000
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(fish, (90, 0))

            # if the fish4 is still there, show it
            if items['fish4'] == False:
                backgd_surf.blit(fish, (6435, 635))
            else:
                g = Grass()
                g.x = 6400
                g.y = 600
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(fish, (120, 0))

            # if the fish5 is still there, show it
            if items['fish5'] == False:
                backgd_surf.blit(fish, (4435, 5835))
            else:
                g = Grass()
                g.x = 4400
                g.y = 5800
                backgd_surf.blit(g.image, (g.x, g.y))
                view_sfc.blit(fish, (150, 0))

            # if spud is at the chick
            if at_chick == True:
                pygame.draw.rect(view_sfc, (0, 0, 0), (50, 300, 400, 200))
                view_sfc.blit(chick_text, (75, 325))

            # if Spud is at the pig
            if at_pig == True:
                pygame.draw.rect(view_sfc, (0, 0, 0), (50, 300, 400, 200))
                view_sfc.blit(pig_text, (75, 325))

            # if Spud is at the white cat
            if at_white_cat == True:
                pygame.draw.rect(view_sfc, (0, 0, 0), (50, 300, 400, 150))
                if traded == True:
                    view_sfc.blit(white_cat_text_2, (75, 325))
                    # get rid of fish in view_sfc

                # print trade for fish text
                else:
                    view_sfc.blit(white_cat_text_1, (75, 325))
                    has_all_fish = True
                    if items['fish1'] == False:
                        has_all_fish = False
                    if items['fish2'] == False:
                        has_all_fish = False
                    if items['fish3'] == False:
                        has_all_fish = False
                    if items['fish4'] == False:
                        has_all_fish = False
                    if items['fish5'] == False:
                        has_all_fish = False
                    if has_all_fish == True:
                        fence_up = False
                        traded = True

            # if Spud is at the black cat
            if at_black_cat == True:
                pygame.draw.rect(view_sfc, (0, 0, 0), (50, 300, 400, 300))
                view_sfc.blit(cat_text, (75, 325))

            # if Spud is at house
            if at_house == True:
                game_state = STATE_WIN

            # draw all the guards that are within the camera rectangle
            for guard in list_of_guards:
                x = int(round(guard.x, 0))
                y = int(round(guard.y, 0))
                if camera_rect.colliderect(Rect(x - 30, y - 30, 75, 75)):
                    view_sfc.blit(guard.image, (x - camera_rect.left, y - camera_rect.top))

            # draw all the carts that are within the camera rectangle
            for cart in list_of_carts:
                x = int(round(cart.x, 0))
                y = int(round(cart.y, 0))
                if camera_rect.colliderect(Rect(x - cart.rad, y - cart.rad, 2 * cart.rad, 2 * cart.rad)):
                    # rotate the cart if needed
                    rotated_image = pygame.transform.rotate(cart.image, -1*cart.dir);
                    temp_location = [x - camera_rect.left + 25, y - camera_rect.top + 25]
                    rotated_rect = rotated_image.get_rect(center=temp_location)
                    view_sfc.blit(rotated_image, rotated_rect)

            # only draw the spud if he is not currently riding a cart
            if spud_on_which_cart == -1:
                if moving_left == True:
                    view_sfc.blit(spud_left, (view_wid // 2, view_hgt // 2))
                    moving_left = False
                elif moving_right == True:
                    view_sfc.blit(spud_right, (view_wid // 2, view_hgt // 2))
                    moving_right = False
                elif moving_up == True:
                    view_sfc.blit(spud_up, (view_wid // 2, view_hgt // 2))
                    moving_up = False
                else:
                    view_sfc.blit(spud_down, (view_wid // 2, view_hgt // 2))
                    moving_down = False

            # if the chick walk clock is too high then reset it
            if (chick_time + 1) >= 27 :
                chick_time = 0

            # draw the specific frame of the chick
            backgd_surf.blit(chick[chick_time//9], (1735, 8850))
            chick_time = chick_time + 1

        # if the game is paused then display the paused screen
        if game_state == STATE_WAIT:
            pygame.draw.rect(view_sfc, (0, 0, 0), (100, 100, view_wid - 200, view_hgt - 200))
            view_sfc.blit(paused, (200, 150))


        # if the player has won display the victory screen
        if game_state == STATE_WIN:
            next_state = STATE_WIN
            view_sfc.fill((255, 255, 255))
            view_sfc.blit(win_screen, (0,0))


        # update the display regardless
        pygame.display.update()

        # change the game state (if warranted)
        game_state = next_state

        # enforce the minimum frame rate
        clock.tick(frame_rate)


# the entry point
if __name__ == "__main__":
    main()
