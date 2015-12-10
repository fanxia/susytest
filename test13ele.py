#!/bin/python
# 11.23.2015 Fan Xia
# Try to using 2015 data:single muon ntuples to look at some hists 
# need to using grid, then run this script

import ROOT
from ROOT import *

fl=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/GoldenJSON/job_data_ggNtuple_SingleElectron_Run2015D_05Oct2015_25ns_JSON_Golden_1560pb_miniAOD.root')


eventTree=fl.Get('ggNtuplizer/EventTree')

v1=ROOT.TLorentzVector()
v2=ROOT.TLorentzVector()
SingleElePt=ROOT.TH1F("SingleElePt","SingleElePt",100,0,1000)
SingleEleEta=ROOT.TH1F("SingleEleEta","SingleEleEta",100,-5,5)
PhotonNum=ROOT.TH1F("PhotonNum","Photon Number",5,0,5)
Leading1PhotonPt=ROOT.TH1F("Leading1PhotonPt","LeadingPhoton_Pt",100,0,1000)
Leading2PhotonPt=ROOT.TH1F("Leading2PhotonPt","LeadingPhoton_Pt",100,0,1000)
Trailing2PhotonPt=ROOT.TH1F("Trailing2PhotonPt","TrailingPhoton_Pt",100,0,1000)
Inv2Photon=ROOT.TH1F("Inv2Photon","Inv2Photon",100,0,500)
METSR1=ROOT.TH1F("METSR1","SR1:MET",100,0,1000)
METSR2=ROOT.TH1F("METSR2","SR2:MET",100,0,1000)
nEvent=eventTree.GetEntriesFast()
print "nEvent=",nEvent
n=0
for i in range(0,100000):
    eventTree.GetEntry(i)
#    print "i=",i
#    for a in range(0,eventTree.eleFiredTrgs.size()): print "eleFiredTrgs.size()",eventTree.eleFiredTrgs.size(),"---",eventTree.eleFiredTrgs[a],"elept",eventTree.elePt[a]
# select exact one tight ele, no other lepton events
    if eventTree.nEle==1 and eventTree.elePt[0]>30 and abs(eventTree.eleEta[0])<2.5 and abs(eventTree.eleD0[0])<0.02 and abs(eventTree.eleDz[0])<1.0  and eventTree.nMu==0 and eventTree.nJet>2:
        SingleElePt.Fill(eventTree.elePt[0])
        SingleEleEta.Fill(eventTree.eleEta[0])
        PhotonNum.Fill(eventTree.nPho)
#        print"---jetJetProbabilityBJetTags:",eventTree.jetJetProbabilityBJetTags[0],"--",eventTree.jetJetProbabilityBJetTags[1],"---jetpfCombinedMVABJetTags:",eventTree.jetpfCombinedMVABJetTags[0],"--",eventTree.jetpfCombinedMVABJetTags[1]
#        for j in range(0,eventTree.eleFiredTrgs.size()): print "eleFiredTrgs.size()",eventTree.eleFiredTrgs.size(),"---",eventTree.eleFiredTrgs[j],"elept",eventTree.elePt[0]
        if eventTree.nPho==1:
            Leading1PhotonPt.Fill(eventTree.phoEt[0])
            n+=1
            METSR1.Fill(eventTree.pfMET)
        elif eventTree.nPho>1:
            #find the max two phoEt
            a1=0
            a2=0
            phoEt=eventTree.phoEt[0]
            for k in range(eventTree.nPho):
                if eventTree.phoEt[k]>phoEt: 
                    a1=k
                    phoEt=eventTree.phoEt[k]
            phoEt=eventTree.phoEt[0]
            for k in range(eventTree.nPho):
                if eventTree.phoEt[k]>phoEt and k != a1: 
                    a2=k
                    phoEt=eventTree.phoEt[k]


#            a2=max([i for i in eventTree.phoEt if i!= a1])
            Leading2PhotonPt.Fill(eventTree.phoEt[a1])
            Trailing2PhotonPt.Fill(eventTree.phoEt[a2])
            v1.SetPtEtaPhiM(eventTree.phoEt[a1],eventTree.phoEta[a1],eventTree.phoPhi[a1],0.0)
            v2.SetPtEtaPhiM(eventTree.phoEt[a2],eventTree.phoEta[a2],eventTree.phoPhi[a2],0.0)
            Inv2Photon.Fill((v1+v2).M())
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
Inv2Photon.Draw()
c.Print("Elechannel/InvmassSR2photon.pdf","pdf")


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

