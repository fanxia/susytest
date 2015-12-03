#!/bin/python
# 11.23.2015 Fan Xia
# Try to using 2015 data:single muon ntuples to look at some hists 
# need to using grid, then run this script

import ROOT
from ROOT import *
fl=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/GoldenJSON/job_data_ggNtuple_SingleMuon_Run2015D_PromptReco-v4_25ns_JSON_Golden_1560pb_miniAOD.root')
eventTree=fl.Get('ggNtuplizer/EventTree')
SingleMuPt=ROOT.TH1F("SingleMuPt","SingleMuPt",100,0,1000)
SinglEMuEta=ROOT.TH1F("SingleMuEta","SingleMuEta",100,-5,5)
PhotonNum=ROOT.TH1F("PhotonNum","Photon Number",5,0,5)
Leading1PhotonPt=ROOT.TH1F("Leading1PhotonPt","LeadingPhoton_Pt",100,0,1000)
Leading2PhotonPt=ROOT.TH1F("Leading2PhotonPt","LeadingPhoton_Pt",100,0,1000)
Trailing2PhotonPt=ROOT.TH1F("Trailing2PhotonPt","TrailingPhoton_Pt",100,0,1000)
METSR1=ROOT.TH1F("METSR1","SR1:MET",100,0,1000)
METSR2=ROOT.TH1F("METSR2","SR2:MET",100,0,1000)
nEvent=eventTree.GetEntriesFast()
print "nEvent=",nEvent
n=0
for i in range(0,1000000):
    eventTree.GetEntry(i)
    if eventTree.nMu==1 and eventTree.muPt[0]>30 and eventTree.nEle==0 and eventTree.nJet>2:
        SingleMuPt.Fill(eventTree.muPt[0])
        SingleMuEta.Fill(eventTree.muEta[0])        
        PhotonNum.Fill(eventTree.nPho)

#        for j in range(0,eventTree.muFiredTrgs.size()): print "muFiredTrgs.size()",eventTree.muFiredTrgs.size(),"---",eventTree.muFiredTrgs[j]
        if eventTree.nPho==1:
            Leading1PhotonPt.Fill(eventTree.phoEt[0])
            n+=1
            METSR1.Fill(eventTree.pfMET)
        elif eventTree.nPho>1:
            Leading2PhotonPt.Fill(eventTree.phoEt[0])
            Trailing2PhotonPt.Fill(eventTree.phoEt[1])
            METSR2.Fill(eventTree.pfMET)
print "---------------------------------------"
print "EventNumber = ",i
print "Single Muon EventNumber = ",n

c=ROOT.TCanvas("c","Plots",800,800)

c.cd()
SingleMuPt.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/SingleMuPt.pdf","pdf")    

c.cd()
SingleMuEta.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/SingleMuEta.pdf","pdf")    

c.Clear()
PhotonNum.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/PhotonNum","pdf")


c.Clear()
Leading1PhotonPt.Draw()
Leading1PhotonPt.SetTitle("SR1: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/Leading1PhotonPt.pdf","pdf")

c.Clear()
Leading2PhotonPt.Draw()
Leading2PhotonPt.SetTitle("SR2: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/Leading2PhotonPt.pdf","pdf")

c.Clear()
Trailing2PhotonPt.Draw()
Trailing2PhotonPt.SetTitle("SR2: TrailingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/Trailing2PhotonPt.pdf","pdf")

c.Clear()
METSR1.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/METSR1.pdf","pdf")

c.Clear()
METSR2.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Muchannel/METSR2.pdf","pdf")
