from IPython.core.debugger import Tracer
import yaml
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'data/'


def is_usable_data(data):
  if data['info']['gender'] == 'female':
    return False
  return True

def process_match(data):
  runs = [0]
  wickets = [0]
  for ball in data['innings'][0]['1st innings']['deliveries']:
    balld = ball[ball.keys()[0]]
    if balld['runs']['extras'] > 0 and ('wides' in balld['extras'] or 'noballs' in balld['extras']):
      runs[-1] += balld['runs']['total']
      if 'wicket' in balld:
        wickets[-1] += 1
    else:
      runs.append(runs[-1] + balld['runs']['total'])
      if 'wicket' in balld:
        wickets.append(wickets[-1] + 1)
      else:
        wickets.append(wickets[-1])
  return runs, wickets

if __name__ == '__main__':
  input_files = os.listdir(DATA_DIR)
  yaml_files = [f for f in input_files if f[-4:] == 'yaml']
  data = []
  i = 0
  for filename in yaml_files[:20]:
    filepath = DATA_DIR + os.sep + filename
    f = open(filepath, 'r')
    doc = f.read()
    filedata = yaml.load(doc)
    if is_usable_data(filedata):
      i += 1
      print "Importing file {0}".format(i)
      data.append(filedata)
  runs = [ process_match(d)[0] for d in data]
  wickets = [ process_match(d)[1] for d in data]
  [plt.plot(r) for r in runs]
  plt.show()
  # (balls left, wickets left  -> runs)
  # predict = curr_runs + runs
  # http://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_regression.html#example-ensemble-plot-gradient-boosting-regression-py
  Tracer()()
