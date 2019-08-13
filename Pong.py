import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0,0]
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_vert_pos = HEIGHT/2
paddle2_vert_pos = HEIGHT/2
paddle1_pos = [(0,HEIGHT/2-HALF_PAD_HEIGHT),(PAD_WIDTH,HEIGHT/2-HALF_PAD_HEIGHT),(PAD_WIDTH,HEIGHT/2+HALF_PAD_HEIGHT),(0,HEIGHT/2+HALF_PAD_HEIGHT)]
paddle2_pos = [(WIDTH-PAD_WIDTH,HEIGHT/2-HALF_PAD_HEIGHT),(WIDTH,HEIGHT/2-HALF_PAD_HEIGHT),(WIDTH,HEIGHT/2+HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH,HEIGHT/2+HALF_PAD_HEIGHT)]
paddle1_vel = 0
paddle2_vel = 0
LEFT = False
RIGHT = True
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH/2,HEIGHT/2]
    if direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240)/60
        ball_vel[1] = -random.randrange(60, 180)/60
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/60
        ball_vel[1] = -random.randrange(60, 180)/60

# define event handlers
def button_handler():
    new_game()
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  
    global score1, score2 
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vert_pos, paddle2_vert_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
     # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, "Red", "Yellow")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vert_pos+paddle1_vel-HALF_PAD_HEIGHT >= 0 and paddle1_vert_pos+paddle1_vel+HALF_PAD_HEIGHT <= HEIGHT:
        paddle1_vert_pos += paddle1_vel    
    paddle1_pos[0] = [0,paddle1_vert_pos-HALF_PAD_HEIGHT]    
    paddle1_pos[1] = [PAD_WIDTH,paddle1_vert_pos-HALF_PAD_HEIGHT]
    paddle1_pos[2] = [PAD_WIDTH,paddle1_vert_pos+HALF_PAD_HEIGHT]
    paddle1_pos[3] = [0,paddle1_vert_pos+HALF_PAD_HEIGHT]
    if paddle2_vert_pos+paddle2_vel-HALF_PAD_HEIGHT >= 0 and paddle2_vert_pos+paddle2_vel+HALF_PAD_HEIGHT <= HEIGHT:
        paddle2_vert_pos += paddle2_vel    
    paddle2_pos[0] = [WIDTH-PAD_WIDTH,paddle2_vert_pos-HALF_PAD_HEIGHT]    
    paddle2_pos[1] = [WIDTH,paddle2_vert_pos-HALF_PAD_HEIGHT]
    paddle2_pos[2] = [WIDTH,paddle2_vert_pos+HALF_PAD_HEIGHT]
    paddle2_pos[3] = [WIDTH-PAD_WIDTH,paddle2_vert_pos+HALF_PAD_HEIGHT]
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 3, 'Green', 'White')
    canvas.draw_polygon(paddle2_pos, 3, 'Green', 'White')
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1] <= paddle1_vert_pos+HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_vert_pos-HALF_PAD_HEIGHT:
            ball_vel[0] = - (ball_vel[0]+ball_vel[0]/10)
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if ball_pos[0] >= WIDTH-BALL_RADIUS-PAD_WIDTH:       
        if ball_pos[1] <= paddle2_vert_pos+HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_vert_pos-HALF_PAD_HEIGHT:
            ball_vel[0] = - (ball_vel[0]+ball_vel[0]/10)   
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    # draw scores
    canvas.draw_text('Player 1', [120,50], 20, 'White') 
    canvas.draw_text(str(score1), [150,80], 20, 'Cyan')
    canvas.draw_text('Player 2', [420,50], 20, 'White')
    canvas.draw_text(str(score2), [450,80], 20, 'Cyan')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel = -10
    elif key == simplegui.KEY_MAP['S']:
        paddle1_vel = 10
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -10  
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 10    

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['S']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0  
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0  

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', button_handler, 100)

# start frame
new_game()
frame.start()
