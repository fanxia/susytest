#!/bin/python
# 11.23.2015 Fan Xia
# Try to using 2015 data:single muon ntuples to look at some hists 
# need to using grid, then run this script

import ROOT
from ROOT import *
fl=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/GoldenJSON/job_data_ggNtuple_SingleMuon_Run2015D_PromptReco-v4_25ns_JSON_Golden_1560pb_miniAOD.root')
eventTree=fl.Get('ggNtuplizer/EventTree')

nEvent=eventTree.GetEntriesFast()
print "nEvent=",nEvent
n=0
trg=[]
a=2**53-1
for i in range(0,1000):
    eventTree.GetEntry(i)
    a&=eventTree.HLTEleMuX
#    print "---xxxx---",eventTree.HLTEleMuX
#    a=bin(eventTree.HLTEleMuX)[2:][::-1]
#    for j in range(len(a)):
#        if a[j]=='1':
#            trg.append(j)
#    trg=list(set(trg))
        
print "---------------------------------------"
print "EventNumber = ",i
#print trg
print bin(a)
'''
c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
SingleMuPt.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("SingleMuPt.pdf","pdf")    

c.Clear()
PhotonNum.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("PhotonNum","pdf")


c.Clear()
Leading1PhotonPt.Draw()
Leading1PhotonPt.SetTitle("SR1: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Leading1PhotonPt.pdf","pdf")

c.Clear()
Leading2PhotonPt.Draw()
Leading2PhotonPt.SetTitle("SR2: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Leading2PhotonPt.pdf","pdf")

c.Clear()
Trailing2PhotonPt.Draw()
Trailing2PhotonPt.SetTitle("SR2: TrailingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Trailing2PhotonPt.pdf","pdf")

c.Clear()
METSR1.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("METSR1.pdf","pdf")

c.Clear()
METSR2.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("METSR2.pdf","pdf")
'''
