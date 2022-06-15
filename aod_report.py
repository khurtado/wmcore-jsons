#! /bin/env python3

import  subprocess
from optparse import OptionParser
import json
import sys

def countLumis(inputFile):
    cmd = ["edmFileUtil",
           "--eventsInLumis",
           "%s" % inputFile 
          ]
    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err  = p.communicate()
    out = str(out)
    out = out.split('\\n')
    out = out[4:]
    runs = []
    for line in out:
        line = line.lstrip()
        line = line.rstrip()
        line = line.split()
        if len(line) == 3:
            runs.append(line)
    jsonind = {}
    for run, lumi, event in runs:
        if run not in jsonind:
            jsonind[run] = [[lumi, event]]
        else:
            jsonind[run].append([lumi, event])
    # Reformat
    for run in jsonind:
        # jsonind[run] = list(set(jsonind[run]))
        lumis = {}
        for lumi, event in jsonind[run]:
            if lumi not in lumis:
                lumis[lumi] = [event]
            else:
                lumis[lumi].append(event)
        #  Get event count per lumi
        for l in lumis:
            if l == 0:
                # Shouldn't happen
                lumis.pop(l)
            lumis[l] = len(lumis[l])
        jsonind[run] = lumis

    return jsonind

if __name__ == '__main__':
    parser = OptionParser(usage='%prog [options] aod-file',
                          description='Return Run/Lumis/Event count')
    parser.add_option("-o", "--output", dest="outputFile",
                      default="lumiSummary.json", help="Name of the output file")
    (options, arg) = parser.parse_args()
    if len(arg) > 1:
        print("Only 1 file at a time is allowed")
    jsondic = countLumis(arg[0])
    if jsondic:
        json.dump(jsondic, open(options.outputFile, 'w'))
        print("Saved %s" % (options.outputFile))
        sys.exit(0)
    sys.exit(1)
