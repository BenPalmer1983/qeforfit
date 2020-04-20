######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################

from configs import configs
from pwscf_input import pwscf_input
from atom_config import atom_config
from pwscf_exec import pwscf_exec

class for_fit:
  
  @staticmethod
  def run():
    print("run")
    
    # Template file    
    g.ffd['template'] = g.inp['template']['file']
    
    # Load settings
    for k in g.inp['settings'].keys():
      if(k in g.ffd.keys()):
        g.ffd[k] = g.inp['settings'][k]
    
    
    # Load configs
    configs.load_from_inp()

    # Load Template
    template = pwscf_input()
    template.load(g.ffd['template'])
    template.set_dirs()
    template.save("input_template.in", g.dirs['templates'])    
    

    
    runfiles = configs.to_file(g.dirs['templates'] + '/' + "input_template.in", g.dirs['configs'])
    
    run_pw = True
    if('run' in g.inp.keys()):
      if('option' in g.inp['run'].keys()):
        run_pw = std.option(g.inp['run']['option'])
        
    if(run_pw):
      log, files_out, run_list = pwscf_exec.execute(runfiles)
    
    
    #print(runfiles)
    
    
    
    
    
    
    