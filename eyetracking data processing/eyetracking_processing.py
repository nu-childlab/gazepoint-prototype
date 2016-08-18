import csv
import re

#GOALS: Look through all the files in a chosen data directory, and use re's to separate which to process
#Produce individual files and aggregate files

with open('testdata/calibration_results.txt') as f:
    calibration_results = f.readlines()

calibfile = open('calibration_results.csv', 'wb')
calibfields = ['data type', 'point', 'x calibration', 'y calibration', 'average error', 'valid points']
calibwriter = csv.DictWriter(calibfile, calibfields)
calibwriter.writeheader()
for line in calibration_results:
    if re.search("CALIB_(START|RESULT)_PT", line):
        startresult = re.search(r"(?<=CALIB_)(START|RESULT)", line).group(0)
        #startresult = startresult.split("_")[1]
        point = re.search(r"(?<=PT=\")[0-9]", line).group(0)
        #point = point[4]
        calx = re.search(r"(?<=CALX=\")[0-9\.]+", line).group(0)
        #calx = calx.split('"')[1]
        caly = re.search(r"(?<=CALY=\")[0-9\.]+", line).group(0)
        #caly = caly.split('"')[1]
        calibwriter.writerow({"data type":startresult, "point":point, "x calibration":calx, "y calibration":caly})
    elif re.search("CALIBRATE_RESULT", line):
        ave_error = re.search(r"(?<=AVE_ERROR=\")[0-9\.]+", line).group(0)
        #ave_error = ave_error.split('"')[1]
        valid_points = re.search(r"(?<=VALID_POINTS=\")[0-9\.]+\"", line).group(0)
        #valid_points = valid_points.split('"')[1]
        calibwriter.writerow({"data type":"SUMMARY", "average error":ave_error, "valid points":valid_points})

calibfile.close()

with open('testdata/trackingdata.csv') as f:
    trackingfile_write = open('trackingdata_results.csv', 'wb')
    trackingfields = ['trial', 'image', 'time', 'Fixation POG X', 'Fixation POG Y', 'Fixation POG time since calibration', 'Fixation POG duration', 'Fixation POG ID', 'Valid POG fixation?', 'Best POG X', 'Best POG Y', 'Valid Best POG fixation?']
    trackingwriter = csv.DictWriter(trackingfile_write, trackingfields)
    trackingwriter.writeheader()
    reader = csv.DictReader(f)
    for line in reader:
        trial = line['trial']
        image = line['image']
        data = line['tracking data']
        if re.search("\<REC ", data):
            TIME = re.search(r"(?<=TIME=\")[0-9\.]+", data).group(0)
            FPOGX = re.search(r"(?<=FPOGX=\")[0-9\.]+", data).group(0)
            FPOGY = re.search(r"(?<=FPOGY=\")[0-9\.]+", data).group(0)
            FPOGS = re.search(r"(?<=FPOGS=\")[0-9\.]+", data).group(0)
            FPOGD = re.search(r"(?<=FPOGD=\")[0-9\.]+", data).group(0)
            FPOGID = re.search(r"(?<=FPOGID=\")[0-9\.]+", data).group(0)
            FPOGV = re.search(r"(?<=FPOGV=\")[0-9\.]+", data).group(0)
            BPOGX = re.search(r"(?<=BPOGX=\")[0-9\.]+", data).group(0)
            BPOGY = re.search(r"(?<=BPOGY=\")[0-9\.]+", data).group(0)
            BPOGV = re.search(r"(?<=BPOGV=\")[0-9\.]+", data).group(0)
            trackingwriter.writerow({'trial':trial, 'image':image, 'time':TIME, 'Fixation POG X':FPOGX, 'Fixation POG Y':FPOGY, 'Fixation POG time since calibration':FPOGS, 'Fixation POG duration':FPOGD, 'Fixation POG ID':FPOGID, 'Valid POG fixation?':FPOGV, 'Best POG X':BPOGX, 'Best POG Y':BPOGY, 'Valid Best POG fixation?':BPOGV})
