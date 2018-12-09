import time

state = 0

# setup application
def setup():
    size(1366, 768)
    background(19, 19, 19)
    
    splash_screen()
    

def draw():
    global state
    
    if state == 0:
        time.sleep(3)
        state = 1
        clear()

    
def splash_screen():
    img = loadImage("images/splash_screen.png")
    image(img, 0, 0)
    
