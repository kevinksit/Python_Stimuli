from psychopy import visual, core, monitors  # import some libraries from PsychoPy
import random
import keyboard
import numpy as np
from psychopy.tools import monitorunittools

mon = monitors.Monitor('leftMonitor')
# Set stimulus parameters
spatial_frequency = 1
temporal_frequency = 2
mov_amt = 5  # pixel per frame max
circle_radius = 75
start_distance = 3 * circle_radius  # distance in pixels
timeout = 5  # in seconds

# Getting window information
mywin = visual.Window([800, 600], monitor=mon, units="pix")
frame_rate = mywin.getActualFrameRate()

# create some stimuli

grating = visual.GratingStim(win=mywin, mask='circle', size=(2 * circle_radius), sf=0.05, ori=45)
target = visual.Circle(win=mywin, radius=circle_radius, edges=100, lineWidth=20)
target.lineColor = [0, 1, 0]

win_statement = visual.TextStim(win=mywin, text='You win!')
lose_statement = visual.TextStim(win=mywin, text='You lose')
# target parameters

# draw the stimuli and update the window

timer = core.Clock()
correct = []
for t in range(5):
    # Initialize
    timer.reset()
    grating.pos = (random.choice([-start_distance, start_distance]), 0)
    in_game = True

    while in_game and timer.getTime() < timeout:
        is_correct = False
        # Have the grating move
        phase_advance = grating.phase + (2 / frame_rate)
        grating.phase = phase_advance
        # Draw textures
        grating.draw()
        target.draw()
        # Flip to screen
        mywin.flip()

        # Move the thing
        if keyboard.is_pressed('right'):
            grating.pos += (mov_amt, 0)
        if keyboard.is_pressed('left'):
            grating.pos -= (mov_amt, 0)

        # Check for end conditions
        if abs(grating.pos[0] - target.pos[0]) < circle_radius: # Win condition
            grating.pos = target.pos
            is_correct = True
            in_game = False
        if abs(grating.pos[0]) > 400 - circle_radius:
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




