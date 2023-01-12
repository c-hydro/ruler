"""
Library Features:

Name:          ruler_process
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20211208'
Version:       '1.0.0'
"""
#######################################################################################
# Libraries
import time
from datetime import datetime
#######################################################################################

# -------------------------------------------------------------------------------------
# Algorithm information
project_name = 'RULER'
alg_name = 'APP EXAMPLE'
alg_type = 'Package'
alg_version = '1.0.0'
alg_release = '2022-12-27'

time_format = '%Y-%m-%d %H:%M'
memory_test = False
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# process to execute process in a while loop
time_sleep = 10
memory_eat = []
while True:

    # define time now - start
    time_now = datetime.now()
    time_run = time_now.strftime(time_format)
    print(' ---> Time ' + time_run + ' ... ')

    # define time start
    time_start = time.time()

    # simulate memory consumption
    if memory_test:
        memory_eat.append(' ' * 2)
        print(' ----> Memory eat ... "' + str(len(memory_eat)) + ' LENGTH"')

    print(' ----> Sleep time ... "' + str(time_sleep) + ' SECONDS"')
    time.sleep(time_sleep)

    # define time elapsed
    time_elapsed = round(time.time() - time_start, 1)
    print(' ----> Elapsed time ... "' + str(time_elapsed) + ' SECONDS"')

    # define time now - end
    print(' ---> Time ' + time_run + ' ... DONE')
# -------------------------------------------------------------------------------------
