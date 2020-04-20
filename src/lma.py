import numpy as np

class lma:


  @staticmethod
  def optimise(f, p, x, y, settings_in=None):
    settings = {
               'fixed': None,
               'conv_threshold': 1.0E-10,
               'max_outer_loops': 100,
               'max_inner_loops': 10,     
               'ng_mode': False,
               }     
    if(settings_in != None):
      for k in settings_in.keys():
        settings[k] = settings_in[k]
            
    if(settings['ng_mode']):
      settings['max_inner_loops'] = 1
            
    converged = False
    p_best = np.copy(p)
    
    n = 0
    while(not converged and n < settings['max_outer_loops']):
      n = n + 1
      j, r = lma.make_j(f, p_best, x, y)
      jt = np.transpose(j)
      rss = sum(r[:]**2)
      
      if(n == 1):
        if(settings['ng_mode']):
          l = 0.0e0
        else:
          l = lma.l_cutoff(j)
          l_cutoff = l
  
      n_inner = 0
      while(not converged and n_inner < settings['max_inner_loops']):
        n_inner = n_inner + 1
        if(not settings['ng_mode']): 
          # LMA MODE
          p = np.copy(p_best)
          h = lma.make_h(j, jt, l)
                
          jtr = np.matmul(jt, r)
          dp = np.linalg.solve(h, jtr)         
          p = p + dp   

          rss_p = rss
          rss = lma.calc_rss(f, p, x, y)
        
          if(abs(rss - rss_p) < settings['conv_threshold']):
            converged = True
            p_best = np.copy(p)
          else:
            if(rss < rss_p):
              p_best = np.copy(p)
              l = 0.2 * l
            else:
              if(l < l_cutoff):
                l = 2.0 * l_cutoff
              l = 1.5 * l
        else:
          # NG MODE
          h = lma.make_h(j, jt, l)                
          jtr = np.matmul(jt, r)
          dp = np.linalg.solve(h, jtr)         
          p_best = p_best + dp   
        
    return p_best

  
  @staticmethod
  def make_j(f, p, x, y):
    j = np.zeros((len(x), len(p)),dtype=np.float64,)
    r = np.zeros((len(x),),dtype=np.float64,)
    pt = np.zeros((len(p),),dtype=np.float64,)
    h = (x[-1] - x[0]) / (1000 * len(x))
    
    for n in range(len(x)):
      fa = f(x[n], p)
      r[n] = y[n] - fa
      for m in range(len(p)):
        pt = np.copy(p)
        pt[m] = pt[m] + h
        fb = f(x[n], pt)
        j[n,m] = (fb - fa) / h
    return j, r  
    
  @staticmethod
  def make_h(j, jt, l):    
    h = np.matmul(jt, j)
    for i in range(len(h)):
      h[i,i] = h[i,i] + h[i,i] * l
    return h

    
  @staticmethod
  def l_cutoff(j):  
    jt = np.transpose(j)
    jtj = np.matmul(jt, j)
    jtj_inv = np.linalg.inv(jtj)
    t = np.trace(jtj_inv)
    l_cutoff = np.float64(1.0 / t)
    return l_cutoff


  @staticmethod
  def calc_rss(f, p, x, y):
    r = np.zeros((len(x),),dtype=np.float64,)    
    r[:] = (y[:] - f(x[:], p))  
    return sum(r[:]**2)  
    
