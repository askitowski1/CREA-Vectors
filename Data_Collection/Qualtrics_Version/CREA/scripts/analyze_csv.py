# Simple script to parse the CSV output from Qualtrics and output the catch trial accuracy,
# correlation between responses, and individual CREA vectors for each subject
#
# Bill Gross, 7/27/23

import csv,re,sys
import numpy as np

fname = sys.argv[1]
catch_answers = [0,6,0,6,6]

def catch_acc(rr):
    try:
        return sum([float(rr[f'Catch{i+1}']==catch_answers[i]) for i in range(5)]) / 5.
    except:
        return 0.0

with open(fname) as f:
    all_rows = [r for r in csv.DictReader(f)]

column_map = {}
for k in all_rows[0].keys():
    m = re.match('^(\d+)_Rating$',k)
    if m:
        column_map[all_rows[0][k].split(" - ")[0]] = m[1]

derived_columns = ['WorkerID','Word','CatchAcc','Corr','Include?']

columns = derived_columns + list(column_map.keys())
rows = []
for r in all_rows[2:]:
    if r['word']=='Test':
        continue
    if r['Progress'] != '100':
        continue
    rr = {'WorkerID':r['WorkerID '],
         'Word':r['word']}
    for k in columns[len(derived_columns):]:
        val = r[f'{column_map[k]}_Rating'].strip().split()
        if len(val)>0:
            val = val[0]
            if val=='Not':
                val = 0
            val = int(val)
            rr[k] = val
    rr['CatchAcc'] = catch_acc(rr)
    rr['Include?'] = 'TRUE'
    rows.append(rr)

words = list(set([x['Word'] for x in rows]))

avg_vector = {}

for w in words:
    avg_vector[w] = []
    for c in columns[len(derived_columns):]:
        cc = []
        for r in filter(lambda x: x['Word']==w,rows):
            cc.append(r[c])
        avg_vector[w].append(sum(cc)/len(cc))

for r in rows:
    wordvec = [r[c] for c in columns[len(derived_columns):]]
    if np.mean(np.abs(np.subtract(wordvec,avg_vector[r['Word']]))) > 1:
        r['Corr'] = np.corrcoef(wordvec,avg_vector[r['Word']])[0,1]
    else:
        r['Corr'] = float('nan')


w = csv.DictWriter(sys.stdout,columns)
w.writeheader()
for rr in rows:
    w.writerow(rr)
