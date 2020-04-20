##########
# GLOBALS

import numpy

class g: 
  
  dirs = {
         'wd': 'wd',
         'log': 'wd/log',  
         'plots': 'wd/plots', 
         'templates': 'wd/templates',  
         'configs': 'wd/configs',  
         }
  
  times = {
          'start' : 0.0,
          'end' : 0.0,
          'duration' : 0.0,
          }
          
  inp = {}    
  
  
  
  ffd = {
         'template': '',
         'ecutwfc': 50,
         'ecutrho': 200,
         'kpoints': '5 5 5 1 1 1',
         'kpointstype': 'automatic',
         'degauss': 0.01,
         }
         
  configs = []
           
  
  log_fh = None
         
  file_counter = 0 
         
  def file_name():
    globals.file_counter = globals.file_counter + 1
    name = "file_"
    file_counter_str = str(globals.file_counter)
    while(len(file_counter_str) < 6):
      file_counter_str = '0' + file_counter_str
    name = name + file_counter_str    
    return name
         
         