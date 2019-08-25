from psychopy import visual, core  # import some libraries from PsychoPy
import random  # for random choosing of parameters
import keyboard  # for getting keyboard inputs
import numpy as np  # For analysis and output of things

# Set stimulus parameters
spatial_frequency = 1
temporal_frequency = 2
mov_amt = 5  # pixel per frame max
circle_radius = 75
start_distance = 3 * circle_radius  # distance in pixels
timeout = 5  # in seconds

# Getting window information
mywin = visual.Window([800, 600], monitor="leftMonitor", units="pix")
frame_rate = mywin.getActualFrameRate()

# create some stimuli
grating = visual.GratingStim(win=mywin, mask='circle', size=(2 * circle_radius), sf=0.05, ori=45)
target = visual.Circle(win=mywin, radius=circle_radius, edges=100, lineWidth=20)
target.lineColor = [0, 1, 0]

# Background
dot_xys = []
n_dots = 50
overdraw = 100

for dot in range(n_dots):  # Get the positions of each dot
    dot_x = random.uniform(-400 - overdraw, 400 + overdraw)
    dot_y = random.uniform(-300 - overdraw, 300 + overdraw)
    dot_xys.append([dot_x, dot_y])

dot_stim = [visual.ElementArrayStim(
    win=mywin,
    units="pix",
    nElements=n_dots,
    elementTex=None,
    elementMask="circle",
    colors=[random.choice([(1.0, 1.0, 1.0), (-1.0, -1.0, -1.0)]) for _ in range(n_dots)],  # -1 is black here...
    xys=dot_xys,
    sizes=[random.randint(20, 100) for x in range(n_dots)]
) for _ in range(5)]  # Create one dot stim per repeat first, so we have a bunch? maybe change this to pool

win_statement = visual.TextStim(win=mywin, text='You win!')
lose_statement = visual.TextStim(win=mywin, text='You lose')
# draw the stimuli and update the window

timer = core.Clock()
correct = []
for t in range(5):
    # Initialize
    timer.reset()
    # Reset positions
    grating.pos = (random.choice([-start_distance, start_distance]), 0)
    in_game = True

    while in_game and timer.getTime() < timeout:
        is_correct = False
        # Have the grating drift
        phase_advance = grating.phase + (2 / frame_rate)
        grating.phase = phase_advance

        # Draw textures
        dot_stim[t].draw()
        grating.draw()
        target.draw()
        # Flip to screen
        mywin.flip()

        # Move the thing
        if keyboard.is_pressed('right'): # Switched to get "orientation"
            grating.pos += (mov_amt, 0)
            dot_stim[t].fieldPos += (mov_amt, 0)
        if keyboard.is_pressed('left'):
            grating.pos -= (mov_amt, 0)
            dot_stim[t].fieldPos -= (mov_amt, 0)

        # Check for end conditions
        if abs(grating.pos[0] - target.pos[0]) < circle_radius - 5:  # Win condition
            grating.pos = target.pos
            is_correct = True
            in_game = False
            dot_stim[t].draw()
            grating.draw()
            target.draw()
            mywin.flip()
            core.wait(0.2)

        if abs(grating.pos[0]) > 400 - circle_radius:  # Lose condition
            in_game = False

        if keyboard.is_pressed('esc'):
            mywin.close()
            break

    timer.reset()
    while timer.getTime() < 1:
        if is_correct:
            win_statement.draw()
        else:
            lose_statement.draw()
        mywin.flip()

        if keyboard.is_pressed('esc'):
            mywin.close()
            break

    # Log results
    correct.append(is_correct)

# somethin's rwrang
print('Correct rate: {}%'.format(np.mean(correct)*100))




