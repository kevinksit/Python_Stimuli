from psychopy import visual, core, monitors  # import some libraries from PsychoPy
from psychopy.tools import monitorunittools as mt
import numpy as np

# Set stimulus parameters
spatial_frequency = 0.12
temporal_frequency = 2
orientations = range(0, 360, 30)
repeats = 2

on_time = 2
off_time = 2

ori_time = on_time + off_time
rep_time = ori_time * len(orientations)

print('Total stimulus time: {}s'.format(rep_time * repeats))
# Getting window information
my_mon = monitors.Monitor('leftMonitor')
mywin = visual.Window([800, 600], fullscr=False, monitor=my_mon, units="degFlat")
screen_sz = (mt.pix2deg(800, monitor=my_mon), mt.pix2deg(600, monitor=my_mon))
frame_rate = mywin.getActualFrameRate()

# Converting to frames
on_frames = int(on_time * frame_rate)
off_frames = int(off_time * frame_rate)

# create some stimuli
grating = visual.GratingStim(win=mywin, tex='sin', size=[2*x for x in screen_sz], sf=spatial_frequency)  # full field

# draw the stimuli and update the window
session_timer = core.Clock()
start = session_timer.getTime()
for rep in range(repeats):

    for ori in range(len(orientations)):
        print(session_timer.getTime())
        blank_off = start + ori * ori_time + rep * rep_time + off_time
        while session_timer.getTime() < blank_off:
            mywin.flip()

        print(session_timer.getTime())
        stim_off = start + ori * ori_time + rep * rep_time + off_time + on_time
        while session_timer.getTime() < stim_off:
            phase_advance = grating.phase + (2 / frame_rate)
            grating.phase = phase_advance
            grating.ori = orientations[ori]
            grating.draw()
            mywin.flip()

mywin.close()
core.quit()
