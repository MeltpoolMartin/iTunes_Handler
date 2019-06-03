import time
import sys

def move_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))


while True:
    hh, mm, ss = time.localtime()[3:6]
    move_cursor(0, 0)
    print(f'{hh}:{mm}:{ss}')
    time.sleep(1)