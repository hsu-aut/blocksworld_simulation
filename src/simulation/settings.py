# Caption for the simulation window
CAPTION = "Blocks World Simulation"

# Screen settings
WIDTH = 1000
HEIGHT = 500
FPS = 60

# Colors
WHITE = (240, 240, 240)
BORDER_COLOR = (50, 50, 50)
SHADOW_COLOR = (180, 180, 180)
TEXT_COLOR = (30, 30, 30)

COLOR_LIST = [
    (255, 140, 140), 
    (140, 255, 140), 
    (140, 140, 255),
    (255, 215, 140), 
    (200, 140, 255), 
    (140, 255, 255),
    (255, 255, 140), 
    (255, 140, 255), 
    (140, 255, 200),
    (255, 200, 140), 
    (255, 140, 200), 
    (200, 255, 140),
    (140, 200, 255), 
    (200, 140, 200), 
    (140, 200, 140),
    (200, 200, 255), 
    (215, 255, 140), 
    (140, 255, 215),
    (255, 140, 215), 
    (215, 140, 255), 
    (140, 215, 255),
    (255, 255, 200), 
    (200, 255, 255), 
    (255, 200, 255),
    (255, 215, 215), 
    (215, 255, 215)
]

# Physics settings
GRAVITY = 0.4

# Box settings
BOX_WIDTH = 100
BOX_HEIGHT = 50

# Stack settings
STACK_NUMBER = 3
STACK_X_POSITION_LEFT = 100
STACK_X_POSITION_RIGHT = 900
# calculate stack positions based on the number of stacks
STACK_X_POSITIONS = [
    STACK_X_POSITION_LEFT + i * (STACK_X_POSITION_RIGHT - STACK_X_POSITION_LEFT) // (STACK_NUMBER - 1)
    for i in range(STACK_NUMBER)
]

# Ground settings
GROUND_Y = HEIGHT - 40

# Robot settings
ROBOT_SPEED = 8
ROBOT_BASE_Y = 100

# Font settings
MAIN_FONT_NAME = "Arial"
MAIN_FONT_SIZE = 28
LABEL_FONT_SIZE = 20

# Initial boxes
BOX_NUMBER = 4
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
INITIAL_BOX_LETTERS = [LETTERS[i % len(LETTERS)] for i in range(BOX_NUMBER)]
