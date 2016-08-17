import Tkinter as tk
import tkFileDialog
import re
import csv

print "Hi, welcome to the experiment conditions generator!"
print "This will help you create a csv file full of parameters for the Gazepoint experiment frame!"
print "If you have a problem and need to stop, press control+c to force the program to end."
raw_input("Press Enter to start!")

raw_input("First you'll select the directory containing your stimuli. Press Enter when you're ready.")
while True:
    root=tk.Tk()
    root.withdraw()
    stim_directory = tkFileDialog.askdirectory()
    print "This is the path to the directory you've chosen:"
    print stim_directory
    response = raw_input("Does that look right? y/[n]: ")
    if re.search("^y", response, re.IGNORECASE):
        break
print ""

while True:
    calibration_input = raw_input("Enter a duration for calibration. 11 will only show the calibration"
    + " window. More than 11 will show the results and their tracked gaze for a little while: ")
    try:
        calibration_time = float(calibration_input)
        break
    except ValueError:
        print "There was a problem! Your input here should be a number! Please try again!"

print ""

while True:
    display_input = raw_input("Enter a duration for image display. The image will be shown and "
    + "gaze will be tracked for this duration: ")
    try:
        display_time = float(display_input)
        break
    except ValueError:
        print "There was a problem! Your input here should be a number! Please try again!"

print ""

while True:
    repetitions_input = raw_input("Enter the number of times you want to repeat each image. if you only want to see each image once, just enter 1: ")
    try:
        repetitions = int(repetitions_input)
        break
    except ValueError:
        print "There was a problem! Your input here should be an integer! Please try again!"

print ""

while True:
    question_input = raw_input("Enter the question you want to ask participants. (The prompt for what key to press is defined later.) This question will be displayed on the response screen: ")
    try:
        question = str(question_input)
        print "Your question is: "
        print ""
        print question
        print ""
        response = raw_input("Does that look right? y/[n]: ")
        if re.search("^y", response, re.IGNORECASE):
            break
    except ValueError:
        print "There was a problem! Your input here should be able to become a string! Please try again!"

print ""

print "Next you'll define the set of keys that are acceptable responses for your question."
while True:
    print "For f and j, enter fj. For any key, enter all. To define another set, just press enter."
    response = raw_input("Choose your key set: ")
    if re.search("^fj", response, re.IGNORECASE):
        keylist = ['f', 'j']
        print "Your key list contains f and j."
        response = raw_input("Is this right? y/[n]")
        if re.search("^y", response, re.IGNORECASE):
            break
    elif re.search("^all", response, re.IGNORECASE):
        keylist = None
        print "Your key list includes all keys."
        response = raw_input("Is this right? y/[n]")
        if re.search("^y", response, re.IGNORECASE):
            break
    else:
        print "Ok, please type your list of keys! Each key should be one (lowercase) letter or number, and they should be separated by a comma"
        key_input = raw_input("Please enter all of your keys, separated by commas!: ")
        key_input = key_input.replace(" ","")
        key_input = key_input.split(",")
        keylist = []
        for key in key_input:
            key = key[0]
            if re.search("^[a-zA-Z]$", key):
                keylist.append(key.lower())
            elif re.search("^[0-9]$", key):
                keylist.append(key)
        print "Your finalized list is: "
        print keylist
        response = raw_input("Is this right? y/[n]")
        if re.search("^y", response, re.IGNORECASE):
            break

print ""

while True:
    prompt_input = raw_input("Enter the prompt you would like to appear below the question on the response screen. This is usually helpful for telling participants what to press. This will be displayed on the response screen: ")
    try:
        prompt = str(prompt_input)
        print "Your prompt is: "
        print ""
        print prompt
        print ""
        response = raw_input("Does that look right? y/[n]: ")
        if re.search("^y", response, re.IGNORECASE):
            break
    except ValueError:
        print "There was a problem! Your input here should be able to become a string! Please try again!"

condfile = open('experimentconditions.csv', 'wb')
condfields = ['calibration_time', 'display_time', 'stim_directory', 'repetitions', 'question', 'keylist', 'prompt']
condwriter = csv.DictWriter(condfile, condfields)
condwriter.writeheader()
condwriter.writerow({'calibration_time':calibration_time, 'display_time':display_time, 'stim_directory':stim_directory, 'repetitions':repetitions, 'question':question, 'keylist':keylist, 'prompt':prompt})

print ""
print "You're done! Please check the folder containing this script for your experimentconditions.csv file! If it looks right, put the csv in the same folder as the experiment code!"
