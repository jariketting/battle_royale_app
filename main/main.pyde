"""
Main file of the application.
"""

# imports
import time
import random
import Weapons
import Items
from Controller import Controller

state = 0  # stores state of the game (0 = splash screen, 1 = player screen, 2 =?...)
image_dir = "images/"  # directory images are stored in
controller = Controller()

roll = 1 
timer = 0
y_offset = 0

# stores all buttons withing app
buttons = [
    [0, 0, 0, 0],  # start button
    [0, 0, 0, 0],  # add player button
    [0, 0, 0, 0],  # remove player button
    [0, 0, 0, 0],  # dice
    [0, 0, 0, 0],  # round tracker hover
    [0, 0, 0, 0],  # next turn
    [0, 0, 0, 0],  # close attack button
    [0, 0, 0, 0],  # 0 tiles button
    [0, 0, 0, 0],  # 1 tile button
    [0, 0, 0, 0],  # 2 tiles button
    [0, 0, 0, 0]  # radiation zone damage button
]

#stores item buttons
item_buttons = [
    [0, 0, 0, 0],  # shotgun
    [0, 0, 0, 0],  # assault rifle
    [0, 0, 0, 0],  # sniper rifle
    [0, 0, 0, 0],  # armor 1
    [0, 0, 0, 0],  # band aid 1
    [0, 0, 0, 0],  # med kit 1
    [0, 0, 0, 0],  # armor 2
    [0, 0, 0, 0],  # band aid 2
    [0, 0, 0, 0]  # med kit 2
]

card_buttons = [
    [0, 0, 0, 0],  # del weapon
    [0, 0, 0, 0],  # weapon
    [0, 0, 0, 0],  # del first item
    [0, 0, 0, 0],  # first item
    [0, 0, 0, 0],  # del second item
    [0, 0, 0, 0]  # second item
]

player_buttons = [
    [0, 0, 0, 0, None],  # player 1
    [0, 0, 0, 0, None],  # player 2
    [0, 0, 0, 0, None],  # player 3
    [0, 0, 0, 0, None],  # player 4
    [0, 0, 0, 0, None],  # player 5
    [0, 0, 0, 0, None],  # player 6
    [0, 0, 0, 0, None],  # player 7
    [0, 0, 0, 0, None]  # player 8
]

dices = []

"""
Setup the application and change any settings according to the designs specs.
"""
def setup():    
    global dices
    
    size(1366, 768)  # set size of application according to designs specs
    background(19)  # set background color of application
    frameRate(30)  # set framerate
    
    # add one player on default
    controller.add_player('Player 1')
    controller.add_player('Player 2')
    
    # setup dices
    dices = [loadImage(image_dir+"main_screen/dices/1.png"), loadImage(image_dir+"main_screen/dices/2.png"), loadImage(image_dir+"main_screen/dices/3.png")]
    
    # start application with splash screen
    if state == 0:
        splash_screen()
    elif state == 3:
        win_screen()
    

"""
This function will keep looping until the application has been terminated.

The main functionality is to call the correct function based on the state of the game, together with some other small stuff (like the timer showing the splash screen for 3 secs)
"""
def draw():
    # global variables
    global state
    
    clear()
    noStroke()  # remove stroke
    background(19)  # set background color of application
    
    # check what state the game is in
    if state == 0:
        # splash screen has to be displayer for 3 seconds, then the next screen will be shown by chaching the state
        time.sleep(3)  # wait 3 seconds
        state = 1  # change state of game to 1
    elif state == 1:
        # player screen
        player_screen()
    elif state == 2:
        # main screen
        main_screen()
    elif state == 3:
        time.sleep(10)  # wait 10 seconds
        state = 4  # change state of game to 4
    elif state == 4:
        credit_screen()
    
        
"""
When the player clicks on the screen, this function will check if a button was clicked.

Buttons are stored in the buttons var. And are pointed to by it's index key
"""
def mouseReleased():
    # get required global vars
    global buttons, state, controller, timer, item_buttons
    
    boxes = buttons + card_buttons + item_buttons + player_buttons
    
    # go trough each button and check if it is pressed
    for button, cords in enumerate(boxes):
        # check if players clicked location falls withing the buttons cords
        if mouseX >= cords[0] and mouseX <= cords[2] and mouseY >= cords[1] and mouseY <= cords[3]:
            print('Button: '+ str(button))
            
            # some buttons can only be pressed in specific stages of the application, check what state the game is in
            if state == 1:
                if button == 0:
                    # check if min players count is met
                    if len(controller.get_players()) >= 2:
                        state = 2  # change state to two to start the game
                elif button == 1:
                    # only allow the button to be pressed when the player count is lower than eight
                    if len(controller.get_players()) < 8:
                        controller.add_player("Player " + str(len(controller.get_players()) + 1))
                elif button == 2:
                    if len(controller.get_players()) > 1:
                        controller.remove_player(-1)
            elif state == 2:
                turn_state = controller.get_turn_state()
                
                if not controller.is_attacking():
                    card_start = 11
                    item_start = 17
                    
                    if button == 3 and turn_state == 0:
                        controller.set_turn_state(1)
                        timer = 50
                        print('dice')
                    elif button == 5 and (turn_state == 1 or turn_state == 2):
                        controller.next_turn()
                        print('next turn')
                        
                    elif button == card_start + 1 and controller.get_current_player().get_weapon() and turn_state == 0:
                        controller.start_attack()
                        controller.set_turn_state(1)
                        print('click weapon')
                    elif button == card_start and controller.get_current_player().get_weapon():
                        controller.get_current_player().set_weapon(None)
                        print('del weapon')
                        
                    elif button == card_start + 3 and controller.get_current_player().get_first_item() and turn_state == 1:
                        controller.set_turn_state(2)
                        controller.get_current_player().get_first_item().use(controller.get_current_player())
                        controller.get_current_player().set_first_item(None)
                        print('click first item')
                    elif button == card_start + 2 and controller.get_current_player().get_first_item():
                        controller.get_current_player().set_first_item(None)
                        print('del first item')
                        
                    elif button == card_start + 5 and controller.get_current_player().get_second_item() and turn_state == 1:
                        controller.set_turn_state(2)
                        controller.get_current_player().get_second_item().use(controller.get_current_player())
                        controller.get_current_player().set_second_item(None)
                        print('click second item')
                    elif button == card_start + 4 and controller.get_current_player().get_second_item():
                        controller.get_current_player().set_second_item(None)
                        print('del second item')
                        
                    elif button == item_start and not controller.get_current_player().get_weapon():
                        controller.get_current_player().set_weapon(Weapons.Shotgun())
                        print('shotgun')
                    elif button == item_start + 1 and not controller.get_current_player().get_weapon():
                        controller.get_current_player().set_weapon(Weapons.AssaultRifle())
                        print('assault rifle')
                    elif button == item_start + 2 and not controller.get_current_player().get_weapon():
                        controller.get_current_player().set_weapon(Weapons.SniperRifle())
                        print('sniper rifle')
                        
                    elif button == item_start + 3 and not controller.get_current_player().get_first_item():
                        controller.get_current_player().set_first_item(Items.Armor())
                        print('armor 1')
                    elif button == item_start + 4 and not controller.get_current_player().get_first_item():
                        controller.get_current_player().set_first_item(Items.BandAid())
                        print('band aid 1')
                    elif button == item_start + 5 and not controller.get_current_player().get_first_item():
                        controller.get_current_player().set_first_item(Items.FirstAidKit())
                        print('med kit 1')
                        
                    elif button == item_start + 6 and not controller.get_current_player().get_second_item():
                        controller.get_current_player().set_second_item(Items.Armor())
                        print('armor 2')
                    elif button == item_start + 7  and not controller.get_current_player().get_second_item():
                        controller.get_current_player().set_second_item(Items.BandAid())
                        print('band aid 2')
                    elif button == item_start + 8  and not controller.get_current_player().get_second_item():
                        controller.get_current_player().set_second_item(Items.FirstAidKit())
                        print('med kit 2')
                        
                    elif button == 10:
                        controller.do_radiation_zone_damage()                        
                        print('radiation zone damage')
                    
                elif not controller.get_player_attacking():
                    player_start = 26
                    
                    if button == 6:
                        controller.reset_player_attack()
                        controller.set_turn_state(0)
                        print('attacking stopped')
                    elif button >= player_start:
                        controller.set_player_attacking(cords[4])
                        print(cords[4].get_name() + ' being attacked')
                elif controller.get_player_attacking():
                    if button == 6:
                        controller.reset_player_attack()
                        controller.set_turn_state(0)
                        print('attacking stopped')
                    elif button == 7:
                        controller.attack_player(0)
                        controller.reset_player_attack()
                        print('0 tiles clicked')
                    elif button == 8:
                        controller.attack_player(1)
                        controller.reset_player_attack()
                        print('1 tile clicked')
                    elif button == 9:
                        controller.attack_player(2)
                        controller.reset_player_attack()
                        print('2 tiles clicked')

 
"""
Splash screen (state 0)

This is the screen the user will first be presented with when launching the application.
"""
def splash_screen():    
    # draw splash screen image
    bg = loadImage(image_dir+"splash_screen/bg.png")
    image(bg, 0, 0)
    
    
"""
Payer screen (state 1)

In this screen the player will add up to 8 players (min = 2) and can start the game
"""    
def player_screen():
    # get required global vars
    global buttons
    
    # set background
    bg = loadImage(image_dir+"player_screen/bg.png")
    image(bg, 0, 0)
    
    # create start button
    start_button = loadImage(image_dir+"player_screen/start_button.png")
    buttons[0] = [1112, 683, 1349, 751]  # set cords for start button
    image(start_button, buttons[0][0], buttons[0][1])

    # create font for player names
    player_font = createFont("Arial Bold", 28, True)
    textFont(player_font)
    
    player_image = loadImage(image_dir+"player_screen/player.png")

    # starting cords for the player list
    ypos = 100
    xpos = 429

    # display each player on screen
    for player in controller.get_players():
        image(player_image, xpos, ypos)
        
        fill(0)  # set color of name displayed
        text(player.get_name(), xpos + 67, ypos + 37)  # display players name
        
        fill(*player.get_color())  # fill with players color
        rect(xpos, ypos, 56, 53)  # create rect with players color
        
        ypos += 74  # add to ypos, 54 is size of image + 20 for the margin at the botton of each player
    
    # show add player button when player count is under 8
    if len(controller.get_players()) < 8:
        buttons[1] = [xpos, ypos, xpos + 212, ypos + 45]
        add_player_image = loadImage(image_dir+"player_screen/add_player_button.png")
        image(add_player_image, xpos, ypos)
    else:
        buttons[1] = [0,0,0,0] # make sure button can not be pressed
        
    # show remove player button when player count is under 8
    if len(controller.get_players()) > 2:
        buttons[2] = [742, ypos, 742 + 212, ypos + 45]
        add_player_image = loadImage(image_dir+"player_screen/remove_player_button.png")
        image(add_player_image, 742, ypos)
    else:
        buttons[2] = [0,0,0,0] # make sure button can not be pressed


def main_screen():
    global controller, dices, roll, timer, card_buttons, item_buttons, state

    controller.update_radzone()

    player = controller.get_current_player()
    players = controller.get_players()

    # draw dice    
    if timer >= 0:
        if timer % 5 == 0:
            roll = dice_roll()
        timer = timer - 1
        
    buttons[3] = [1142, 483, 1283, 624]
    image(dices[roll-1], 1142, 483, 141, 141)
    
    # radiation zone damage button
    buttons[10] = [22, 36, 182, 196]
    
    # draw main screen image
    bg = loadImage(image_dir+"main_screen/bg.png")
    image(bg, 0, 0)
    
    # display turn
    font = createFont("Arial Bold", 50, True)
    textFont(font)
    fill(0)
    textAlign(CENTER)
    
    text(controller.get_round(), 1210, 215)
    
    # display current player
    fill(*player.get_color())  # fill with players color
    rect(210, 36, 63, 63)  # create rect with players color
    
    # create font for player name
    player_font = createFont("Arial Bold", 40, True)
    textFont(player_font)
    
    fill(0)  # set color of name displayed
    textAlign(LEFT)
    text(player.get_name(), 283, 80)  # display players name
    
    # display all players
    reversed_players = players[:]
    reversed_players.reverse()
    
    player_font = createFont("Arial Bold", 28, True)
    textFont(player_font)
    
    player_image = loadImage(image_dir+"main_screen/player.png")
    player_image_selected = loadImage(image_dir+"main_screen/player_selected.png")

    # starting cords for the player list
    xpos = 22
    ypos = 695

    # display each player on screen
    for player in reversed_players:
        if player == controller.get_current_player():
            image(player_image_selected, xpos-5, ypos-5)
        else:
            image(player_image, xpos, ypos)
        
        fill(0)  # set color of name displayed
        
        if player.is_dead():
            fill(222)  # set color of name displayed
            
        text(player.get_name(), xpos + 55, ypos + 33)  # display players name
        
        fill(*player.get_color())  # fill with players color
        rect(xpos, ypos, 45, 45)  # create rect with players color
        
        ypos -= 51  # add to ypos, 54 is size of image + 20 for the margin at the botton of each player
        
    
    # display players health and armor
    font = createFont("Arial Bold", 40, True)
    textFont(font)
    fill(255)
    textAlign(RIGHT)
    
    text(controller.get_current_player().get_hp(), 820, 185) 
    text(controller.get_current_player().get_armor(), 820, 270) 
    
    # display weapons and items
    item_bg = loadImage(image_dir+"main_screen/item.png")
    delete_image = loadImage(image_dir+"main_screen/delete_button.png")
    item_font = createFont("Arial Bold", 26, True)
    textFont(item_font)
    textAlign(CENTER)
    
    cur_item = 0
    
    # weapon
    if controller.get_current_player().get_weapon():
        weapon_image = loadImage(image_dir+controller.get_current_player().get_weapon().get_image())
        
        card_buttons[1] = [233, 403, 233 + 232, 403 + 324]
        image(weapon_image, card_buttons[1][0], card_buttons[1][1], 232, 324)
        
        card_buttons[0] = [425, 403, 425 + 40, 403 + 40]
        image(delete_image, card_buttons[0][0], card_buttons[0][1], 40, 40)
        
        for weapon in controller.get_weapons():
            item_buttons[cur_item] = [0, 0, 0, 0]   # change button
            cur_item += 1
        
    else:
        xpos = 233
        ypos = 421
        
        for weapon in controller.get_weapons():
            image(item_bg, xpos, ypos)
            text(weapon.get_name().upper(), xpos + 116, ypos + 33)  # display players name
            
            item_buttons[cur_item] = [xpos, ypos, xpos + 232, ypos + 50]   # add button
            
            ypos += 65
            cur_item += 1
    
    # first item
    if controller.get_current_player().get_first_item():
        item_image = loadImage(image_dir+controller.get_current_player().get_first_item().get_image())
        
        card_buttons[3] = [515, 403, 515 + 232, 403 + 324]
        image(item_image, card_buttons[3][0], card_buttons[3][1], 232, 324)
        
        card_buttons[2] = [707, 403, 707 + 40, 403 + 40]
        image(delete_image, card_buttons[2][0], card_buttons[2][1], 40, 40)
        
        for item in controller.get_items():
            item_buttons[cur_item] = [0, 0, 0, 0]   # change button
            cur_item += 1
    else:
        xpos = 515
        ypos = 421
        
        for item in controller.get_items():
            image(item_bg, xpos, ypos)
            text(item.get_name().upper(), xpos + 116, ypos + 33)  # display players name
            
            item_buttons[cur_item] = [xpos, ypos, xpos + 232, ypos + 50]   # add button
            
            ypos += 65
            cur_item += 1
        
    # second item
    if controller.get_current_player().get_second_item():
        item_image = loadImage(image_dir+controller.get_current_player().get_second_item().get_image())
        
        card_buttons[5] = [795, 403, 795 + 232, 403 + 324]
        image(item_image, card_buttons[5][0], card_buttons[5][1], 232, 324)
        
        card_buttons[4] = [987, 403, 987 + 40, 403 + 40]
        image(delete_image, card_buttons[4][0], card_buttons[4][1], 40, 40)
        
        for item in controller.get_items():
            item_buttons[cur_item] = [0, 0, 0, 0]   # change button
            cur_item += 1
    else:
        xpos = 795
        ypos = 421
        
        for item in controller.get_items():
            image(item_bg, xpos, ypos)
            text(item.get_name().upper(), xpos + 116, ypos + 33)  # display players name
            
            item_buttons[cur_item] = [xpos, ypos, xpos + 232, ypos + 50]   # add button
            
            ypos += 65
            cur_item += 1
    
    # player attack event
    if controller.is_attacking():
        # draw background
        stroke(0)
        fill(255)
        rect(263, 150, 841, 500)
        
        font = createFont("Arial Bold", 26, True)
        textFont(font)
        fill(0)
        textAlign(LEFT)
        
        # draw users weapon
        weapon_image = loadImage(image_dir+controller.get_current_player().get_weapon().get_image())
        image(weapon_image, 273, 160, 232, 324)
        
        buttons[6] = [1064, 150, 1064 + 40, 150 + 40]
        image(delete_image, buttons[6][0], buttons[6][1], 40, 40)
        
        noStroke()
        ypos = 220
        xpos = 515
        
        if controller.get_player_attacking():
            text('How many tiles is the player away?', 515, 190)
            
            for n in range(3):
                fill(19) # set color of rect displayed
                    
                rect(xpos, ypos, 45, 45)
                
                buttons[6 + (n + 1)] = [xpos, ypos, xpos + 45, ypos + 45]
            
                fill(255)  # set color of name displayed
                    
                text(n, xpos + 15, ypos + 33)  # display players name
                
                ypos += 51  # add to ypos, 54 is size of image + 20 for the margin at the botton of each player
            
        else:
            text('Choose player to attack', 515, 190)
            textFont(player_font)
            
            # display each player on screen
            player_start = 0

            for player in controller.get_players():
                if player != controller.get_current_player() and not player.is_dead():
                    fill(19) # set color of rect displayed
                    
                    rect(xpos, ypos, 188, 45)
                    
                    player_buttons[player_start] = [xpos, ypos, xpos + 188, ypos + 45, player]
                
                    fill(255)  # set color of name displayed
                        
                    text(player.get_name(), xpos + 55, ypos + 33)  # display players name
                    
                    fill(*player.get_color())  # fill with players color
                    rect(xpos, ypos, 45, 45)  # create rect with players color
                    
                    ypos += 51  # add to ypos, 54 is size of image + 20 for the margin at the botton of each player
                    player_start += 1
        
    
    # next turn button
    start_button = loadImage(image_dir+"main_screen/next_turn_button.png")
    buttons[5] = [1095, 695, 1334, 739]  # set cords for start button
    image(start_button, buttons[5][0], buttons[5][1])
    
    # radiation zone
    font = createFont("Arial Bold", 50, True)
    textFont(font)
    textAlign(CENTER)
    
    if controller.get_radiation_zone():
        fill(191, 0, 0)
        text('YES', 1210, 365) 
    else:
        fill(0)
        text('NO', 1210, 365) 
    
    buttons[4] = [1136, 260, 1288, 400]
    
    if mouseX >= buttons[4][0] and mouseX <= buttons[4][2] and mouseY >= buttons[4][1] and mouseY <= buttons[4][3]:
        draw_radzone()
        
    if controller.has_winner():
        win_screen()
        state = 3

def win_screen():
    global controller
    
    background(*controller.get_winner().get_color())
    font = createFont("Arial Bold", 100, True)
    textFont(font)
    fill(255)
    textAlign(CENTER)
    
    text('Winner!', 683, 300)
    
    textSize(62)
    
    text(controller.get_winner().get_name() + ' has won the game', 683, 450)

def credit_screen():
    global y_offset

    textAlign(CENTER)
    fill(255)
    textSize(150)
    text('Made by', 683, 1000 + y_offset)
    textSize(70)
    text('Dani de Jong', 683, 1100 + y_offset)
    text('Jari Ketting', 683, 1200 + y_offset)
    text('Ronan van Kessel', 683, 1300 + y_offset)
    text('Daphne Miedema', 683, 1400 + y_offset)
    y_offset = y_offset - 1
    
    if y_offset < -1500:
        y_offset = 0

    
def dice_roll():
    return int(random.randint(1, 3))
    
    
def draw_radzone():
    global controller
    
    radsize = 20
    boardsize = 26
    
    radzone = controller.get_radzone()
    
    # the 'window' behind the board
    textAlign(CENTER,CENTER)
    font = createFont("Arial", 12, True)
    textFont(font)
    fill(127)
    stroke(0);
    rect(180, 180, 40 + (boardsize+1) * radsize, 40 + (boardsize + 1) * radsize)
    
    # the board loop
    for xx in range(boardsize+1):
        for yy in range(boardsize+1):
            if xx == boardsize and yy != boardsize: #vertical coordinates
                fill(0)
                text(chr(yy+65),(xx+0.5)*radsize+200,(yy+0.5)*radsize+200)
            elif yy == boardsize and xx != boardsize: #horizontal coordinates
                fill(0)
                text(str(xx+1),(xx+0.5)*radsize+200,(yy+0.5)*radsize+200)
            elif xx != boardsize and yy != boardsize: #the tiles
                fill(127,127,255)
                rect(xx*radsize+200,yy*radsize+200,radsize,radsize)
                if (xx >= radzone-1 and xx <= boardsize-radzone) and (yy >= radzone-1 and yy <= boardsize-radzone):
                    fill(127,255,127)
                    rect(xx*radsize+200,yy*radsize+200,radsize,radsize)
                if (xx == radzone-1 or xx == boardsize-radzone) or (yy == radzone-1 or yy == boardsize-radzone):
                    fill(255,255,127)
                    rect(xx*radsize+200,yy*radsize+200,radsize,radsize)
                    
    textAlign(LEFT, TOP)
    noStroke()
    
