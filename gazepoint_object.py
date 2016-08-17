import socket
from psychopy import core
import time

class gazepoint_object():
    def __init__(self,host='127.0.0.1',port=4242):
        self.host = host
        self.port = port
        self.address = (host, port)
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.connect(self.address)
        # print "Connection established"
        return

    def calibrate(self, duration=15):
        #Make another socket do it doesn't interfere with data reception
        calib_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        calib_socket.connect(self.address)
        #Putting the calibration on screen and starting it
        calib_socket.send(str.encode('<SET ID="CALIBRATE_SHOW" STATE="1" />\r\n'))
        calib_socket.send(str.encode('<SET ID="CALIBRATE_START" STATE="1" />\r\n'))
        #Wait for the process, and some extra time to see the calibration screen afterwards
        time.sleep(duration)
        #Take it off screen
        calib_socket.send(str.encode('<SET ID="CALIBRATE_SHOW" STATE="0" />\r\n'))
        calib_socket.send(str.encode('<SET ID="CALIBRATE_START" STATE="0" />\r\n'))
        calib_socket.send(str.encode('<GET ID="CALIBRATE_RESULT_SUMMARY" />\r\n'))
        calib_socket.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
        bytes_available = 2048
        data = []
        while bytes_available > 0:
            scan = calib_socket.recv(128)
            if scan != "<REC />\r\n":
                data.append(scan)
            bytes_available -= len(scan)
        #print data
        calib_socket.close()

        return ''.join(data)

    def init_data(self):
        """Run this function before using get_data to read eye tracking data"""
        #connect to socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.address)
        print "Connection established"
        #tell the server what data to track
        self.s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n'))
        self.s.send(str.encode('<SET ID="ENABLE_SEND_POG_BEST" STATE="1" />\r\n'))
        self.s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))
        self.s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
        #Flush some irrelevant data from the receiving buffer
        rxdat = self.s.recv(1024)
        rxdat = self.s.recv(1024)
        return

    def get_data(self, duration=0):
        """Retrieves tracking data. If no duration is given, it will get just
        one point. If a duration is given, it will track for that duration."""
        results = []
        if not duration:
            rxdat = self.s.recv(1024)
            results += [bytes.decode(rxdat)]
        timer = core.CountdownTimer(duration)
        while timer.getTime() > 0:
            rxdat = self.s.recv(1024)
            results += [bytes.decode(rxdat)]
            #print(bytes.decode(rxdat))
        return results

    def end_data(self):
        self.s.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="0" />\r\n'))
        self.s.send(str.encode('<SET ID="ENABLE_SEND_CURSOR" STATE="0" />\r\n'))
        self.s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="0" />\r\n'))
        self.s.close()
