from psychopy import visual, core, monitors  # import some libraries from PsychoPy
from psychopy.tools import monitorunittools

import numpy as np
# Set stimulus parameters
spatial_frequency = 0.12
temporal_frequency = 2
orientations = [0, 45, 90]
repeats = 2

on_time = 5
off_time = 0

ori_time = on_time + off_time
rep_time = ori_time * len(orientations)
# Getting window information

mon = monitors.Monitor('leftMonitor')
mywin = visual.Window([800, 600], fullscr=False, monitor="leftMonitor", units="deg")
screen_sz = (monitorunittools.pix2deg(800, monitor=mon), monitorunittools.pix2deg(600, monitor=mon))

frame_rate = mywin.getActualFrameRate()
# Converting to frames
on_frames = int(on_time * frame_rate)
off_frames = int(off_time * frame_rate)
#create a window

mytex = np.array([[1, -1, 1],
         [-1, 1, -1],
         [1, -1, 1]])
#create some stimuli
grating = visual.GratingStim(win=mywin, tex='sqrXsqr', size=screen_sz, sf=1)  # full field

#draw the stimuli and update the window
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
          #  grating.phase = phase_advance
          #  grating.ori = orientations[ori]
            grating.draw()
            mywin.flip()

    # if len(event.getKeys()) > 0:
    #     break
    # event.clearEvents()
mywin.close()
core.quit()