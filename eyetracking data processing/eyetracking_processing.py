import csv
import re

with open('calibration_results.txt') as f:
    calibration_results = f.readlines()

calibfile = open('calibration_results.csv', 'wb')
calibfields = ['data type', 'point', 'x calibration', 'y calibration', 'average error', 'valid points']
calibwriter = csv.DictWriter(calibfile, calibfields)
calibwriter.writeheader()
for line in calibration_results:
    if re.search("CALIB_", line):
        startresult = re.search(r"CALIB_(START|RESULT)", line).group(0)
        startresult = startresult.split("_")[1]
        point = re.search(r"PT=\"[0-9]\"", line).group(0)
        point = point[4]
        calx = re.search(r"CALX=\"[0-9\.]+\"", line).group(0)
        calx = calx.split('"')[1]
        caly = re.search(r"CALY=\"[0-9\.]+\"", line).group(0)
        caly = caly.split('"')[1]
        calibwriter.writerow({"data type":startresult, "point":point, "x calibration":calx, "y calibration":caly})
    elif re.search("CALIBRATE_RESULT", line):
        ave_error = re.search(r"AVE_ERROR=\"[0-9\.]+\"", line).group(0)
        ave_error = ave_error.split('"')[1]
        valid_points = re.search(r"VALID_POINTS=\"[0-9\.]+\"", line).group(0)
        valid_points = valid_points.split('"')[1]
        calibwriter.writerow({"data type":"SUMMARY", "average error":ave_error, "valid points":valid_points})

calib_file.close()

trackingfile_read = open('trackingdata.csv', 'wb')
trackingreader = csv.DictReader(trackingfile_read)
trackingfile_write = open('calibration_results.csv', 'wb')
trackingfields = ['data type', 'point', 'x calibration', 'y calibration', 'average error', 'valid points']
calibwriter = csv.DictWriter(calib_file, calibfields)
calibwriter.writeheader()
