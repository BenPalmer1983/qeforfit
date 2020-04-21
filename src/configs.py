from units import units

class configs:
  
  @staticmethod
  def make(id=0):
    return {
           'id': id,
           'type': None,
           'size': 1,
           'alat': 0.0,
           'alat_units': 'bohr',
           'cp': numpy.array([1.0,1.0,1.0,0.0,0.0,0.0], dtype=numpy.float64),
           'rand_seed': 0,
           'coord_var': numpy.array([0.0,0.0], dtype=numpy.float64),
           'alat_var': numpy.array([0.0,0.0], dtype=numpy.float64),
           'count': 1,
           'tetra': 0,
           'octa': 0,
           'vac': [],
           'vac_list': [],
           }
           
  @staticmethod
  def load_from_inp():     
    #print("loading")
    
    # Loop through configs
    i = 0
    for c in g.inp['config']:
      for k in c.keys():
        g.log_fh.write(str(k) + ': ' + str(c[k]) + '\n')
      g.log_fh.write('\n')
      
      #print()
      conf = configs.make(i)
      for k in conf.keys():
        if(k in c.keys()):
          if(k == 'cp' or k == 'coord_var' or k == 'alat_var'):
            try:
              #print(c[k])
              for i in range(len(c[k])):
                conf[k][i] = c[k][i]
            except:
              pass
          elif(k == 'vac'):
            try:
              if(type(c['vac'][0]) == list):
                for v in c['vac']:
                  if(len(v) == 2):
                    varr = numpy.array([v[0],v[1]])
                    conf[k].append(varr)
              else:
                if(len(c['vac']) == 2):
                  varr = numpy.array([c['vac'][0],c['vac'][1]])
                  conf[k].append(varr)
            except:
              pass
          else:
            conf[k] = c[k]      
      for v in conf['vac']:
        for i in range(v[1]):
          conf['vac_list'].append(v[0])
      g.configs.append(conf)
      i = i + 1
            
  
  @staticmethod
  def to_file(template, dir):  
    runfiles = []
  
    n = 0
    for c in g.configs:
      random.seed(c['rand_seed'])
    
      n = n + 1
      vac = 0
      tetra = 0
      octa = 0
            
      g.log_fh.write('Save Config ' + str(n) + '\n')            
      g.log_fh.write('======================\n')
      g.log_fh.write('\n')
                  
      for i in range(c['count']):
        seed = random.randint(0,1000000)
        g.log_fh.write('config ' + str(n) + ' ' + str(i+1) + ' \n')
        g.log_fh.write('seed ' + str(seed) + ' \n')
      
        i_str = str(i+1)
        while(len(i_str)<4):
          i_str = '0'+i_str
          
        f = pwscf_input()
        f.load(template)
        f.set_dirs()
        f.set_seed(seed)
        f.set_prefix()    
        # SETTINGS
        f.set_ecutwfc(g.ffd['ecutwfc'])
        f.set_ecutrho(g.ffd['ecutrho'])
        f.set_k_points(g.ffd['kpointstype'], g.ffd['kpoints'])
        f.set_degauss(g.ffd['degauss'])
        
        v = 0
        t = []
        o = []
        if(vac < len(c['vac_list'])):
          v = c['vac_list'][vac]
          vac = vac + 1
        elif(tetra < c['tetra']):
          t.append(f.get_random_atom_label())
          tetra = tetra + 1
        elif(octa < c['octa']):
          o.append(f.get_random_atom_label())
          octa = octa + 1
        
        # CREATE CONFIG
        labels = f.get_atom_labels()
        s = {
            'type': c['type'],
            'labels': None,
            'size_x': c['size'],
            'size_y': c['size'],
            'size_z': c['size'],
            'vac': v,
            'tetra': t,
            'octa': o,
            }    
            
        alat = round(units.convert(c['alat_units'], 'bohr', c['alat']),7)    
        f.set_alat(alat)
        f.set_cp_arr(c['cp']) 
        s_conf = f.set_config(s)
        
        f.rand_vary_alat(c['alat_var'][0], c['alat_var'][1])
        f.rand_vary_positions(c['coord_var'][0], c['coord_var'][1])
        
        f.save("config_" + i_str +".in", g.dirs['configs']+'/'+str(n))    
        runfiles.append(g.dirs['configs']+'/'+str(n)+'/'+'config_' + i_str + '.in')
        
        g.log_fh.write('alat: ' + str(f.get_alat()) + '  [in: ' + str(s_conf['alat_in']) + ' out: ' + str(s_conf['alat_out']) + ']\n')
        g.log_fh.write('type: ' + str(c['type']) + '\n')
        g.log_fh.write('size: ' + str(c['size']) + '\n')
        for l in s_conf['log']:
          g.log_fh.write('   ' + str(l) + '\n')
          
        
        g.log_fh.write('saved to: ' + g.dirs['configs']+'/'+str(n) + '/' + str("config_" + i_str +".in") + '\n')
        g.log_fh.write('\n')
        
      g.log_fh.write('\n')
    # Return file list
    return runfiles
  