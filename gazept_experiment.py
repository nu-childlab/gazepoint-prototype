from psychopy import visual, core, event
from gazepoint_object import gazepoint_object
from os import listdir
from os.path import isfile, join
import os.path
import csv
import re
import tkFileDialog
import time
import random
import ast

#############Parameters!!
if os.path.isfile('experimentconditions.csv'):
    #get conditions
    with open('experimentconditions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print "test"
            calibration_time = float(row["calibration_time"])
            display_time = float(row["display_time"])
            stim_directory = row["stim_directory"]
            repetitions = int(row["repetitions"])
            question = row["question"]
            keylist = ast.literal_eval(row["keylist"])
            prompt = row["prompt"]
else:
    #If you don't want to go through the condition generator, you can change these parameters directly.
    calibration_time = 11
    display_time = 2
    stim_directory = "C:/Users/expt102/Documents/gazepoint_code/gazepoint_psychopy/28px"
    repetitions = 0
    question = "check this out"
    keylist = ['f', 'j']
    prompt = "woah"


############File setup
calibrationfile = open("calibration_results.txt", 'wb')
responsefile = open("responses.csv", 'wb')
responsefields = ['trial', 'image', 'response', 'rt']
responsewriter = csv.DictWriter(responsefile,responsefields)
responsewriter.writeheader()
trackingfile = open("trackingdata.csv", 'wb')
trackingfields = ['trial', 'image', 'tracking data']
trackingwriter = csv.DictWriter(trackingfile,trackingfields)
trackingwriter.writeheader()

############calibration
gp = gazepoint_object()
while True:
    calibration_results = gp.calibrate(calibration_time)
    calibrationfile.write(calibration_results)
    response = raw_input("Experimenter: Was the calibration successful? y/[n]: ")
    if re.search("^y", response, re.IGNORECASE):
        break

#get all the images
tempfiles = [f for f in listdir(stim_directory) if isfile(join(stim_directory, f))]
images = []
for f in tempfiles:
    if re.search(".jpg$", f, re.IGNORECASE):
        images += [f]
    else:
        print f + " isn't a jpg image! It wasn't included."

#Preload the images into stimuli
stimuli_list = []
myWin = visual.Window((1000,1000), monitor='testMonitor',allowGUI=False, color=(-1,-1,-1))
for stim in images:
    stimuli_list.append(visual.ImageStim(myWin, image=stim_directory+"/"+stim, pos=(0,0), units='deg'))

background = visual.Rect(myWin, lineWidth=0, fillColor="black", size=[800,800], pos=[0,0])
instructions = visual.TextStim(myWin, text="Welcome to the experiment or whatever", height=60,color='white', pos=[0,0], units='pixels')
background.draw()
instructions.draw()
myWin.flip()
while True:
    event.waitKeys()
    break
#Prep response variables
question_stim = visual.TextStim(myWin, text=question, height=60,color='white', pos=[0,0], units='pixels')
prompt_stim = visual.TextStim(myWin, text=prompt, height=30, color='white', pos=[0,-60], units='pixels')

#prep other variables
trial=1
timer = core.Clock()

#Cycle thru each stim

for stim in stimuli_list:
    gp.init_data()
    stim.draw()
    myWin.flip()
    #time.sleep(2)
    tracking_results = gp.get_data(display_time)
    #Start response drawing
    background.draw()
    question_stim.draw()
    prompt_stim.draw()
    myWin.flip()
    #Start the response screen
    timer.reset()
    while True:
        response=event.waitKeys(keyList=keylist)[0]
        break
    rt = timer.getTime()
    responsewriter.writerow({'response':response, 'rt':rt, 'image':stim.image, 'trial':trial})
    for row in tracking_results:
        trackingwriter.writerow({'tracking data':row, 'image':stim.image, 'trial':trial})
    trial += 1


core.quit()
sys.exit()
