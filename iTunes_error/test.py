import time

while True:
    hh, mm, ss = time.localtime()[3:6]
    print('\r', f'{hh}:{mm}:{ss}', end="")
    time.sleep(1)