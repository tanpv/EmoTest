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
minError =  0.001
groups = { 
  'fac_all': [0]+list(arange(3,13)),
  'fac_upp': [0, 3, 4, 5, 6],
  'fac_low': [0, 7, 8],
  'fac_eye': [0, 9, 10],
  'fac_lid': [0, 11, 12],
  'cog_all': [0]+list(arange(13,34)), 
  'cog_exc': [0, 15, 16, 17, 18],
  'cog_rel': [0, 19, 20, 21, 22],
  'cog_fru': [0, 23, 24, 25, 26],
  'cog_eng': [0, 27, 28, 29, 30],
  'cog_int': [0, 31, 32, 33, 34],
  'cog_foc': [0, 35, 36, 37, 38],
  'pow_all': [0]+list(arange(39,63))
}

def getData (esFile) : 
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
    a_stat = summary(actual)
    deltas = {}
    errors = {}
    for k, v in t_stat.iteritems() : deltas[k] = rounder(abs(v - a_stat[k])/ (v if v != 0 else 1))
    for k,v in groups.iteritems() :  errors[k] = rounder(((target[:, v] - actual[:, v]) ** 2).mean())
    for k, v in deltas.iteritems() : results.append((scene, k, v, errors[k]))
    print json.dumps({'target': t_stat, 'actual':a_stat, 'deltas': deltas, 'errors': errors}, indent=2)
    if not path.exists(report + scene):
        os.makedirs(report + scene)
    with open(report+scene+'/'+build+'.json', 'w') as outfile: 
      json.dump({'target': t_stat, 'actual':a_stat, 'deltas': deltas, 'errors': errors}, outfile, indent=2)

#@mark.parametrize("scene, eRow, aRow", allRows)
#def test_approx() : 
#  assert error < minError, group +" error non zero in scene "+scene

@mark.parametrize("scene,group,delta, error", results)
def test_errors(scene, group, delta, error) :
  assert error < minError, group +" error non zero in scene "+scene

@mark.parametrize("scene,group,delta, error", results)
def test_norms(scene, group, delta, error) : 
  assert delta < minError, group +" delta non zero in scene "+scene

compare()