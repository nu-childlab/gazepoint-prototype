import csv
import re
import Tkinter as tk
import tkFileDialog
from os import listdir
from os.path import isfile, join

print "Welcome to the eyetraking data processer!"
raw_input("First you'll need to select the directory containing all your data. Press enter to open the directory selector dialog box.")
root=tk.Tk()
root.withdraw()
directory = tkFileDialog.askdirectory()
tempfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
calib_filenames = []
tracking_filenames = []
for f in tempfiles:
    if re.search(r"s[0-9]+_calibration_results\.txt", f):
        calib_filenames += [f]
    elif re.search(r"s[0-9]+_tracking_data\.csv", f):
        tracking_filenames += [f]


calib_aggregatefile = open('calibration_aggregateResults.csv', 'wb')
calibfields = ['subject', 'data type', 'point', 'x calibration', 'y calibration', 'average error', 'valid points']
calib_aggregatewriter = csv.DictWriter(calib_aggregatefile, calibfields)
calib_aggregatewriter.writeheader()

for filename in calib_filenames:
    #Open the file and read the data into a list
    with open(directory+"/"+filename) as f:
        calibration_results = f.readlines()
    #Use re to get the subject number
    subject = re.search(r"s[0-9]+", filename).group(0)
    calib_writefile = open(subject + '_calibration_processedResults.csv', 'wb')
    calibwriter = csv.DictWriter(calib_writefile, calibfields)
    calibwriter.writeheader()
    for line in calibration_results:
        if re.search("CALIB_(START|RESULT)_PT", line):
            startresult = re.search(r"(?<=CALIB_)(START|RESULT)", line).group(0)
            point = re.search(r"(?<=PT=\")[0-9]", line).group(0)
            calx = re.search(r"(?<=CALX=\")-?[0-9\.]+", line).group(0)
            caly = re.search(r"(?<=CALY=\")-?[0-9\.]+", line).group(0)
            calibwriter.writerow({"data type":startresult, "point":point, "x calibration":calx, "y calibration":caly})
        elif re.search("CALIBRATE_RESULT", line):
            ave_error = re.search(r"(?<=AVE_ERROR=\")-?[0-9\.]+", line).group(0)
            valid_points = re.search(r"(?<=VALID_POINTS=\")-?[0-9\.]+\"", line).group(0)
            calibwriter.writerow({"subject":subject, "data type":"SUMMARY", "average error":ave_error, "valid points":valid_points})
            calib_aggregatewriter.writerow({"subject":subject, "data type":"SUMMARY", "average error":ave_error, "valid points":valid_points})

    calib_writefile.close()
calib_aggregatefile.close()

#####TRACKING PROCESSING
tracking_aggregatefile = open('tracking_aggregateResults.csv', 'wb')
trackingfields = ['subject', 'trial', 'image', 'time', 'Fixation POG X', 'Fixation POG Y', 'Fixation POG time since calibration', 'Fixation POG duration', 'Fixation POG ID', 'Valid POG fixation?', 'Best POG X', 'Best POG Y', 'Valid Best POG fixation?']
tracking_aggregatewriter = csv.DictWriter(tracking_aggregatefile, trackingfields)
tracking_aggregatewriter.writeheader()

for filename in tracking_filenames:
    with open(directory+"/"+filename) as f:
        #Use re to get the subject number
        subject = re.search(r"s[0-9]+", filename).group(0)
        tracking_writefile = open(subject + '_tracking_processedResults.csv', 'wb')
        trackingwriter = csv.DictWriter(tracking_writefile, trackingfields)
        trackingwriter.writeheader()
        reader = csv.DictReader(f)
        for line in reader:
            #subject = line['subject']
            trial = line['trial']
            image = line['image']
            data = line['tracking data']
            if re.search("\<REC ", data):
                TIME = re.search(r"(?<=TIME=\")-?[0-9\.]+", data).group(0)
                FPOGX = re.search(r"(?<=FPOGX=\")-?[0-9\.]+", data).group(0)
                FPOGY = re.search(r"(?<=FPOGY=\")-?[0-9\.]+", data).group(0)
                FPOGS = re.search(r"(?<=FPOGS=\")-?[0-9\.]+", data).group(0)
                FPOGD = re.search(r"(?<=FPOGD=\")-?[0-9\.]+", data).group(0)
                FPOGID = re.search(r"(?<=FPOGID=\")-?[0-9\.]+", data).group(0)
                FPOGV = re.search(r"(?<=FPOGV=\")-?[0-9\.]+", data).group(0)
                BPOGX = re.search(r"(?<=BPOGX=\")-?[0-9\.]+", data).group(0)
                BPOGY = re.search(r"(?<=BPOGY=\")-?[0-9\.]+", data).group(0)
                BPOGV = re.search(r"(?<=BPOGV=\")-?[0-9\.]+", data).group(0)
                trackingwriter.writerow({"subject":subject, 'trial':trial, 'image':image, 'time':TIME, 'Fixation POG X':FPOGX, 'Fixation POG Y':FPOGY, 'Fixation POG time since calibration':FPOGS, 'Fixation POG duration':FPOGD, 'Fixation POG ID':FPOGID, 'Valid POG fixation?':FPOGV, 'Best POG X':BPOGX, 'Best POG Y':BPOGY, 'Valid Best POG fixation?':BPOGV})
                tracking_aggregatewriter.writerow({"subject":subject, 'trial':trial, 'image':image, 'time':TIME, 'Fixation POG X':FPOGX, 'Fixation POG Y':FPOGY, 'Fixation POG time since calibration':FPOGS, 'Fixation POG duration':FPOGD, 'Fixation POG ID':FPOGID, 'Valid POG fixation?':FPOGV, 'Best POG X':BPOGX, 'Best POG Y':BPOGY, 'Valid Best POG fixation?':BPOGV})
    tracking_writefile.close()
tracking_aggregatefile.close()
