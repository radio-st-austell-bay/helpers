"""Helper to process RSPlayer logs for Programme Return.

Put RSPlayer logs into some folder, change to it, open a Python prompt and paste
in this code.  Be sure that the logs contain only the data you want (ie trim the
start and end to get rid of data outside of the reporting period).

XXX To do:
"""

import csv
import glob
import re
import sets

headings = ["Date", "Time", "Artist", "Title"]
pat = re.compile('(?P<D>[0-9]{2})/(?P<M>[0-9]{2})/(?P<Y>[0-9]{4}) (?P<h>[0-9]{2}):(?P<m>[0-9]{2}):(?P<s>[0-9]{2}) SONG "(?P<a>[^-"]+) - (?P<t>[^"]+)"')

def make_row(m):
    if m is None:
        return None
    d = m.groupdict()
    return [
        "%(Y)s-%(M)s-%(D)s" % d,
        "%(h)s:%(m)s:%(s)s" % d,
        d['a'],
        d['t'],
    ]

def fix(r):
    if re.match('[0-9]+$', r[2]):
        if ' _ ' in r[3]:
            a, t = r[3].split(' _ ', 1)
        else:
            no_title.add((r[2], r[3]))
            a, t = r[3], '?'
        r[2] = a
        r[3] = t
    return r

no_title = sets.Set()
all_data = []
for fname in glob.glob('log*.txt'):
    f = open(fname, 'r')
    for line in f:
        line = line.strip()
        if not line:
            continue
        match = pat.match(line)
        if not match:
            continue
        all_data.append(fix(make_row(match)))
    f.close()
    print 'Processed', fname

all_data.sort()
d1 = all_data[0][0].replace('-', '')
d2 = all_data[-1][0].replace('-', '')
g = open('log-%s-%s.csv' % (d1, d2), 'wb')
w = csv.writer(g, dialect='excel')
w.writerow(headings)
w.writerows(all_data)
g.close()

no_title = list(no_title)
no_title.sort()
if no_title:
    print 'Tracks with no title (%d)' % (len(no_title),)
    for tpl in no_title:
        print '%s - %s' % tpl
else:
    print 'No tracks found with no title.'


