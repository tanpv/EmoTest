from numpy import * 
from scipy.linalg import norm
from scipy.stats.stats import pearsonr
from pytest import *

from os import listdir, path
import json
import os


scenes='./scenes/' #EDF source input files by sessionId
output='./output/' #target expected  emostate results
report='./report/' #comparison resport files
results = []

# groups = { #mat
  # 'fac_all': arange(3,13),
  # 'fac_upp': [0]+arange(3,7),
  # 'fac_low': [0]+arange(7,9),
  # 'fac_eye': [0]+arange(9,11),
  # 'fac_lid': [0]+arange(11,13),
  # 'cog_all': [0]+arange(13,34), 
  # 'cog_exc': [0]+arange(15,19),
  # 'cog_rel': [0]+arange(19,23),
  # 'cog_fru': [0]+arange(23,27),
  # 'cog_eng': [0]+arange(27,31),
  # 'cog_int': [0]+arange(31,35),
  # 'cog_foc': [0]+arange(35,38),
  # 'pow_all': [0]+arange(39,106)
# }

# groups = { #mat
  # 'fac_all': arange(3,13),
  # 'fac_upp': [0]+arange(3,7),
  # 'fac_low': [0]+arange(7,9),
  # 'fac_eye': [0]+arange(9,11),
  # 'fac_lid': [0]+arange(11,13),
  # 'cog_all': [0]+arange(13,34), 
  # 'cog_exc': [0]+arange(15,19),
  # 'cog_rel': [0]+arange(19,23),
  # 'cog_fru': [0]+arange(23,27),
  # 'cog_eng': [0]+arange(27,31),
  # 'cog_int': [0]+arange(31,35),
  # 'cog_foc': [0]+arange(35,38),
  # 'pow_all': [0]+arange(39,63)
# }


groups = {  #tung 
  'fac_all': arange(3,13),
  'fac_upp': [0]+arange(3,7),
  'fac_low': [0]+arange(8,9),
  'fac_eye': [0]+arange(10,11),
  'fac_lid': [0]+arange(12,13),
  'cog_all': [0]+arange(14,34), 
  'cog_exc': [0]+arange(14,18),
  'cog_rel': [0]+arange(19,22),
  'cog_fru': [0]+arange(23,26),
  'cog_eng': [0]+arange(27,30),
  'cog_int': [0]+arange(31,34),
  'cog_foc': [0]+arange(35,38),
  'pow_all': [0]+arange(39,63) #only for 5 channels to use for both insight and epoc+
}

def getData (esFile) : 
  print 'esFile is  ', esFile
  head = open(esFile).readline().rstrip().split(',') 
  #for (i, col) in enumerate(head) : print(i, col)
  data = genfromtxt(esFile, delimiter=',', skip_header=1)
  data = delete(data, -1, 1)
  return data  

def summary (data, result = {}) : 
  #result = {'dim_row' :  data.shape[0], 'dim_col': data.shape[1] }
  for k,v in groups.iteritems() : result[k] = rounder(norm(data[:, v]))
  return result

def rounder(num): 
  return float("{0:.4f}".format(num))
 
def compare(build = 'latest') :
  for scene in listdir(scenes) :
    target = getData(path.abspath(path.join(scenes, scene, 'target.csv')))
    actual = getData(path.abspath(path.join(output, scene, build+'.csv')))
    t_stat = summary(target)
    # print 't_stat', t_stat
    a_stat = summary(actual)
    # print 'a_stat', a_stat
    deltas = {}
    errors = {}
    for k, v in t_stat.iteritems() : deltas[k] = rounder(abs(v - a_stat[k])/ (v if v != 0 else 1))
    for k,v in groups.iteritems() :  
        print 'target ',target[:, v]
        print 'actual ',actual[:, v]
        errors[k] = rounder(((target[:, v] - actual[:, v]) ** 2).mean())
        print 'error ', k, ': ', errors[k]
    for k, v in deltas.iteritems() : results.append((scene, k, v, errors[k]))
    print json.dumps({'target': t_stat, 'actual':a_stat, 'deltas': deltas, 'errors': errors}, indent=2)
    
    if not path.exists(report + scene):
        os.makedirs(report + scene)
    with open(report+scene+'/'+build+'.json', 'w') as outfile: 
      json.dump({'target': t_stat, 'actual':a_stat, 'deltas': deltas, 'errors': errors}, outfile, indent=2)

@mark.parametrize("scene,group,delta, error", results)
def test_deltas(scene, group, delta, error) :
  assert delta < 0.01, group +" delta non zero in scene "+scene
  assert error < 0.01, group +" error non zero in scene "+scene

compare()