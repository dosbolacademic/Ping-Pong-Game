import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random


WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
min_position = (BALL_RADIUS+PAD_WIDTH, BALL_RADIUS)
max_position = (WIDTH-BALL_RADIUS-PAD_WIDTH, HEIGHT-BALL_RADIUS)
bounce_speed = [1.1, 1]

pad_right_pos = pad_left_pos = HEIGHT / 2
pad_right_speed = pad_left_speed = 0


def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [direction * random.randrange(120, 240), -random.randrange(60, 180)]


def new_game():
    global pad_right_pos, pad_left_pos, pad_right_speed, pad_left_speed, scores
    scores = [0,0]
    spawn_ball(random.choice([-1,1]))
    
def draw(canvas):
    global score1, score2, pad_left_pos, pad_right_pos, ball_pos, ball_vel
         

    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        

    update_ball()
            

    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")
    
    pad_left_pos = constrained_pos(pad_left_pos, HALF_PAD_HEIGHT, HEIGHT-HALF_PAD_HEIGHT, pad_left_speed)
    pad_right_pos = constrained_pos(pad_right_pos, HALF_PAD_HEIGHT, HEIGHT-HALF_PAD_HEIGHT, pad_right_speed)
    
    
    canvas.draw_line((HALF_PAD_WIDTH, pad_left_pos - HALF_PAD_HEIGHT), 
                     (HALF_PAD_WIDTH, pad_left_pos + HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'white')  
    canvas.draw_line((WIDTH-HALF_PAD_WIDTH, pad_right_pos - HALF_PAD_HEIGHT), 
                     (WIDTH-HALF_PAD_WIDTH, pad_right_pos + HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'white')
    
       
    bounce_or_score()
    
    
    canvas.draw_text(str(scores[0]), (WIDTH*0.2, HEIGHT*0.3), HEIGHT*0.2, 'white')
    canvas.draw_text(str(scores[1]), (WIDTH*0.7, HEIGHT*0.3), HEIGHT*0.2, 'white')

def bounce_or_score():
    if ball_pos[0] == min_position[0] and paddle_miss(pad_left_pos):
        score(1)
    elif ball_pos[0] == max_position[0] and paddle_miss(pad_right_pos):
        score(0)
        
def score(who):
    scores[who] += 1
    spawn_ball(who*2-1)
                
def paddle_miss(paddle_pos):
    return not (paddle_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle_pos + HALF_PAD_HEIGHT)
        
def update_ball():  
    for i in (0,1):
        ball_pos[i] = constrained_pos(ball_pos[i],min_position[i],max_position[i],ball_vel[i]/60.0)
        if ball_pos[i] in (min_position[i], max_position[i]):
            ball_vel[i] *= -bounce_speed[i]

def constrained_pos(old_position, min_position, max_position, speed):
    position = old_position + speed
    if (position <= min_position): return min_position
    elif (position >= max_position): return max_position
    else: return position
        
def keydown(key):
    speed = 5
    global pad_right_speed, pad_left_speed
    if key == simplegui.KEY_MAP['up']: pad_right_speed = -speed
    elif key == simplegui.KEY_MAP['down']: pad_right_speed = speed
    elif key == simplegui.KEY_MAP['w']: pad_left_speed = -speed
    elif key == simplegui.KEY_MAP['s']: pad_left_speed = speed

def keyup(key):
    global pad_right_speed, pad_left_speed
    if key == simplegui.KEY_MAP['up']: pad_right_speed = max (0, pad_right_speed)
    elif key == simplegui.KEY_MAP['down']: pad_right_speed = min (0, pad_right_speed)
    elif key == simplegui.KEY_MAP['w']: pad_left_speed = max (0, pad_left_speed)
    elif key == simplegui.KEY_MAP['s']: pad_left_speed = min (0, pad_left_speed)


frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)


new_game()
frame.start()
