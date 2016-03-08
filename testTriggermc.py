#!/bin/python
# 3.8.2016 by Fan Xia
# to check the HLT distribution 

import os
import sys
import ROOT
from ROOT import *

f=TFile.Open("root://eoscms///eos/cms/store/group/phys_smp/ggNtuples/13TeV/mc/job_spring15_ggNtuple_WJetsToLNu_amcatnlo_pythia8_25ns_miniAOD.root")
#f=TFile.Open("data/SingleElectron_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD__data_example.root")

tree=f.Get("ggNtuplizer/EventTree")
n_events = tree.GetEntries()
print"Total events number: ",n_events

Hhlt=ROOT.TH1F("HLT hist","HLT hist",60,0,60)

for i in range(1000):
    tree.GetEntry(i)
    hlt=tree.HLTEleMuX
    for hh in range(len(bin(hlt))-2):
        if hlt>>hh&1:
            Hhlt.Fill(hh)
c=ROOT.TCanvas("c","c",600,600)
c.cd()
Hhlt.Draw()
c.Print("Hhlt.pdf","pdf")
