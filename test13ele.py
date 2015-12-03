#!/bin/python
# 11.23.2015 Fan Xia
# Try to using 2015 data:single muon ntuples to look at some hists 
# need to using grid, then run this script

import ROOT
from ROOT import *

fl=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/GoldenJSON/job_data_ggNtuple_SingleElectron_Run2015D_05Oct2015_25ns_JSON_Golden_1560pb_miniAOD.root')


eventTree=fl.Get('ggNtuplizer/EventTree')

SingleElePt=ROOT.TH1F("SingleElePt","SingleElePt",100,0,1000)
SingleEleEta=ROOT.TH1F("SingleEleEta","SingleEleEta",50,-5,5)
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
#    print "i=",i
#    for a in range(0,eventTree.eleFiredTrgs.size()): print "eleFiredTrgs.size()",eventTree.eleFiredTrgs.size(),"---",eventTree.eleFiredTrgs[a],"elept",eventTree.elePt[a]
    if eventTree.nEle==1 and eventTree.elePt[0]>30 and eventTree.nMu==0 and eventTree.nJet>2:
        SingleElePt.Fill(eventTree.elePt[0])
        SingleEleEta.Fill(eventTree.eleEta[0])
        PhotonNum.Fill(eventTree.nPho)

#        for j in range(0,eventTree.eleFiredTrgs.size()): print "eleFiredTrgs.size()",eventTree.eleFiredTrgs.size(),"---",eventTree.eleFiredTrgs[j],"elept",eventTree.elePt[0]
        if eventTree.nPho==1:
            Leading1PhotonPt.Fill(eventTree.phoEt[0])
            n+=1
            METSR1.Fill(eventTree.pfMET)
        elif eventTree.nPho>1:
            if eventTree.phoEt[0]>eventTree.phoEt[1]: 
                a1=eventTree.phoEt[0]
                a2=eventTree.phoEt[1]
            else:
                a1=eventTree.phoEt[1]
                a2=eventTree.phoEt[0]
            Leading2PhotonPt.Fill(a1)
            Trailing2PhotonPt.Fill(a2)
            METSR2.Fill(eventTree.pfMET)
print "---------------------------------------"
print "EventNumber = ",i
print "Single Ele EventNumber = ",n

c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
SingleElePt.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/SingleElePt.pdf","pdf")    

c.cd()
SingleEleEta.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/SingleEleEta.pdf","pdf")    

c.Clear()
PhotonNum.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/PhotonNum.pdf","pdf")


c.Clear()
Leading1PhotonPt.Draw()
Leading1PhotonPt.SetTitle("SR1: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/Leading1PhotonPt.pdf","pdf")

c.Clear()
Leading2PhotonPt.Draw()
Leading2PhotonPt.SetTitle("SR2: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/Leading2PhotonPt.pdf","pdf")

c.Clear()
Trailing2PhotonPt.Draw()
Trailing2PhotonPt.SetTitle("SR2: TrailingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/Trailing2PhotonPt.pdf","pdf")

c.Clear()
METSR1.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/METSR1.pdf","pdf")

c.Clear()
METSR2.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Elechannel/METSR2.pdf","pdf")
