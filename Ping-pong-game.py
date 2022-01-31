
#README 
#In the mini project video the ball does not start moving until a key is pressed
#so I just added a message to remind user about it.

# Implementationof classic arcade game Pong

import PySimpleGUI
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel = [0, 0]
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = [0 + PAD_WIDTH // 2, HEIGHT // 2]
paddle2_pos = [WIDTH - PAD_WIDTH // 2, HEIGHT // 2]
score1 = "0"
score2 = "0"
key_press = False
message = "Press Any key To Start The Game"

def win1():
    global score1, LEFT
    var = int(score1)
    var += 1
    score1 = str(var)
    
def win2():
    global score2, RIGHT
    var = int(score2)
    var += 1
    score2 = str(var)
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, key_press # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]    
    ball_vel = [0, 0]
    if key_press:
        ball_vel[0] = random.randrange(2, 5)
        ball_vel[1] = random.randrange(1, 3)
      
        if(direction == RIGHT):
            ball_vel[1] = -ball_vel[1]
        else:
            ball_vel[1] = -ball_vel[1]
            ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos,key_press, message, ball_pos, ball_vel,paddle2_pos, paddle1_vel, paddle2_vel,HALF_PAD_HEIGHT, HALF_PAD_WIDTH  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [0 + PAD_WIDTH // 2, HEIGHT // 2]
    paddle2_pos = [WIDTH - PAD_WIDTH // 2, HEIGHT // 2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = "0"
    score2 = "0"
    key_press = False
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    message = "Press Any key To Start The Game"
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, "White", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if((paddle1_pos[1] + HALF_PAD_HEIGHT + paddle1_vel <= HEIGHT) and (paddle1_pos[1]- HALF_PAD_HEIGHT + paddle1_vel >= 0)):
        paddle1_pos[1] += paddle1_vel
    
    if((paddle2_pos[1] + HALF_PAD_HEIGHT + paddle2_vel <= HEIGHT) and (paddle2_pos[1]- HALF_PAD_HEIGHT + paddle2_vel >= 0)):
        paddle2_pos[1] += paddle2_vel
    
    # draw paddles
    a = 0
    b = paddle1_pos[1] - PAD_HEIGHT // 2
    c = PAD_WIDTH
    d = paddle1_pos[1] + PAD_HEIGHT // 2
    canvas.draw_polygon([(a, b), (a, d), (c, d), (c, b)], 2, "White", "white")
    
    a = WIDTH - PAD_WIDTH
    b = paddle2_pos[1] - PAD_HEIGHT // 2
    c = WIDTH
    d = paddle2_pos[1] + PAD_HEIGHT // 2
    canvas.draw_polygon([(a, b), (a, d), (c, d), (c, b)], 2, "White", "white")
    
    # determine whether paddle and ball collide    
    
    if(ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] = -ball_vel[1] 
    
    if(ball_pos[1]  <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    if(ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH):
        if paddle2_pos[1] - HALF_PAD_HEIGHT-5 <= ball_pos[1] <=  paddle2_pos[1] +5+ HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            if(ball_vel[0] < 0):
                ball_vel[0] -= 1
            else:
                ball_vel[0] += 1
        else:
            win1()
            spawn_ball(False)
            
    
    if(ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if paddle1_pos[1] - HALF_PAD_HEIGHT - 5<= ball_pos[1] <=  paddle1_pos[1] +5+ HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            if(ball_vel[0] < 0):
                ball_vel[0] -= 1
            else:
                ball_vel[0] += 1
        else:
            win2()
            spawn_ball(True)
            
    # draw scores
    canvas.draw_text(score1, [200, 100], 40, "White")
    canvas.draw_text(score2, [360, 100], 40, "White")
    canvas.draw_text(message, [30, 250], 40, "Yellow")    
        
def keydown(key):
    global paddle1_vel, paddle2_vel, key_press, message
    
    if not key_press:
        message = ""
        key_press = True
        spawn_ball(True)
    
    if key == PySimpleGUI.KEY_MAP["up"]:
        paddle2_vel = -10
    if key == PySimpleGUI.KEY_MAP["down"]:
        paddle2_vel = 10
   
    if key == ord("w") or key == ord("W"):
        paddle1_vel = -10
    if key == ord("s") or key == ord("S"):
        paddle1_vel = 10

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = PySimpleGUI.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
