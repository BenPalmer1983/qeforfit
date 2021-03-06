################################################################
#    Main Program
#
#
#
#
################################################################

import os
import time
import datetime
import re
import sys
import shutil
from globals import g
from std import std
from read_config import read_config
from for_fit import for_fit


def main():
  
  # RECORD START TIME
  g.times['start'] = time.time()
  
  # MAKE DIRS
  for d in g.dirs.keys():
    dir = g.dirs[d]
    std.make_dir(dir)
  
  # OPEN LOG
  g.log_fh = open(g.dirs['log'] + '/main.log', 'w')
  g.log_fh.write('###########################################################################\n')
  g.log_fh.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + '\n')
  g.log_fh.write('###########################################################################\n')
  g.log_fh.write('\n')
  g.log_fh.write('Script: ' + str(sys.argv[0]) + '\n')
  if(len(sys.argv)>1):
    shutil.copyfile(sys.argv[1], g.dirs['log'] + '/input.log')
    run_program = False
    try:
      g.inp = read_config.read_file(sys.argv[1])
      g.log_fh.write('Loaded: ' + str(sys.argv[1]) + '\n')
      run_program = True
    except:
      g.log_fh.write('Unable to load, exiting\n')
      
      
#######################################################################
#######################################################################
# RUN
    if(run_program):
      g.log_fh.write('\n')
      for_fit.run()
#######################################################################
#######################################################################
    

  # CLOSE LOG
  g.times['end'] = time.time()
  g.log_fh.write('\n')
  g.log_fh.write('###########################################################################\n')
  g.log_fh.write('Duration: ' + str(g.times['end'] - g.times['start']) + '\n')
  g.log_fh.write('###########################################################################\n')
  g.log_fh.close()



# Run
main()
