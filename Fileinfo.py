import time
import datetime
import os


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileSize(filePath):
    #filePath = filePath.decode('utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

def get_FileAccessTime(filePath):
    #filePath = filePath.decode('utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)

def get_FileModifyTime(filePath):
    #filePath = filePath.decode('utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

filename = r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx'

size = get_FileSize(filename)
ModifyTime = get_FileModifyTime(filename)
LocalTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
print(ModifyTime-time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
