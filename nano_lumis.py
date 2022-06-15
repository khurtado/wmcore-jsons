#!/usr/bin/env python
# imported from https://github.com/CERN-PH-CMG/cmg-cmssw/blob/0c11a5a0a15c4c3e1a648c9707b06b08b747b0c0/PhysicsTools/Heppy/scripts/heppy_report.py
from optparse import OptionParser
import json
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys

def root2map(tree):
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("run", 1)
    tree.SetBranchStatus("luminosityBlock", 1)
    tree.SetBranchStatus("event", 1)
    jsonind = {}
    for e in range(tree.GetEntries()):
        tree.GetEntry(e)
        run, lumi, event = tree.run, tree.luminosityBlock, tree.event
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
    parser = OptionParser(usage='%prog [options] nanoAOD-files',
                          description='Check the output of the LuminosityBlocks and produce a json file of the processed runs and lumisections')
    parser.add_option("-t", "--tree", dest="treeName", default="Events",
                      help="Name of the TTree with the luminosity blocks")
    parser.add_option("-o", "--output", dest="outputFile",
                      default="lumiSummary.json", help="Name of the output file")
    (options, args) = parser.parse_args()
    if len(args) == 0:
        print('provide at least one input file in argument. Use -h to display help')
        exit()
    chain = ROOT.TChain(options.treeName)
    for a in args:
        chain.Add(a)
    jsondic = root2map(chain)
    if jsondic:
        json.dump(jsondic, open(options.outputFile, 'w'))
        print("Saved %s" % (options.outputFile))
        sys.exit(0)
    sys.exit(1)
