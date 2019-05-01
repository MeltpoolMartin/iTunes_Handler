import subprocess
import time
import sys_proc.get_proc_attrs as get_proc_attr
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(f'{__name__}.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
#yyyy-MM-dd HH:mm:ss,SSS

i = 0
logger.info("Initialization finished")

"""subprocess.call("open -a TextEdit")
logging.info("Program started via subprocess call")

while i < 5:
    print(i)
    time.sleep(1)
    i += 1
proc_info = get_proc_attr.get_proc_attrs("TexEdit")
"""