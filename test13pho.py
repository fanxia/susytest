#!/bin/python
# 11.23.2015 Fan Xia
# Try to using 2015 data:single muon ntuples to look at some hists 
# need to using grid, then run this script

import ROOT
from ROOT import *

sw=ROOT.TStopwatch()
sw.Start()


fl=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/SilverJSON/job_data_ggNtuple_DoubleEG_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD.root')
eventTree=fl.Get('ggNtuplizer/EventTree')

v1=ROOT.TLorentzVector()
v2=ROOT.TLorentzVector()
PhotonNum=ROOT.TH1F("PhotonNum","Photon Number",5,0,5)
deltaR=ROOT.TH1F("","",50,0,5)

diPhotonM=ROOT.TH1F("diPhotonM","diPhotonM",100,0,1000)
diPhotonMET=ROOT.TH1F("diPhotonMET","diPhotonMET",100,0,1000)
diPhotonLeadPt=ROOT.TH1F("diPhotonLeadPt","diPhotonLeadPt",100,0,1000)
diPhotonTrailPt=ROOT.TH1F("diPhotonTrailPt","diPhotonTrailPt",100,0,1000)
Leading1PhotonPt=ROOT.TH1F("Leading1PhotonPt","LeadingPhoton_Pt",100,0,1000)
Leading2PhotonPt=ROOT.TH1F("Leading2PhotonPt","LeadingPhoton_Pt",100,0,1000)
Trailing2PhotonPt=ROOT.TH1F("Trailing2PhotonPt","TrailingPhoton_Pt",100,0,1000)
Inv2Photon=ROOT.TH1F("Inv2Photon","Inv2Photon",100,0,1000)
#METSR1=ROOT.TH1F("METSR1","SR1:MET",100,0,1000)
#METSR2=ROOT.TH1F("METSR2","SR2:MET",100,0,1000)
nEvent=eventTree.GetEntriesFast()
print "nEvent=",nEvent
n=0
nhltpass=0
for i in range(0,100000):
  eventTree.GetEntry(i)
  PhotonNum.Fill(eventTree.nPho)
# -----------------HLT selection
  hlt=((eventTree.HLTPho)%2**18)//2**14

  if hlt>= 1:
    nhltpass+=1


    if eventTree.nPho==1:
        Leading1PhotonPt.Fill(eventTree.phoEt[0])
        n+=1
#                METSR1.Fill(eventTree.pfMET)
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
                    
        v1.SetPtEtaPhiM(eventTree.phoEt[a1],eventTree.phoEta[a1],eventTree.phoPhi[a1],0.0)
        v2.SetPtEtaPhiM(eventTree.phoEt[a2],eventTree.phoEta[a2],eventTree.phoPhi[a2],0.0)
        dR=v1.DeltaR(v2)

        #---------with only hlt selection-------------------
 
        Leading2PhotonPt.Fill(eventTree.phoEt[a1])
        Trailing2PhotonPt.Fill(eventTree.phoEt[a2])
        deltaR.Fill(dR)
        Inv2Photon.Fill((v1+v2).M())
        #------------ +make detail selection to fill diPhoton plots-----------------
        if abs(eventTree.phoEta[a1])<1.4442 and abs(eventTree.phoEta[a2])<1.4442 and eventTree.phoEt[a1]>35 and eventTree.phoEt[a2]>25 and eventTree.phoIDbit[a1]>2 and eventTree.phoIDbit[a2]>2 and  dR>0.3:
          diPhotonM.Fill((v1+v2).M())
          diPhotonMET.Fill(eventTree.pfMET)
          diPhotonLeadPt.Fill(eventTree.phoEt[a1])
          diPhotonTrailPt.Fill(eventTree.phoEt[a2])


print "---------------------------------------"
print "EventNumber = ",i
print "nhltpass = ",nhltpass


c=ROOT.TCanvas("c","Plots",800,800)

c.cd()
Inv2Photon.Draw("e")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/Invmass2photon_hlt.pdf","pdf")


c.Clear()
diPhotonM.Draw("e")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/diPhotonM_hlt.pdf","pdf")

c.Clear()
diPhotonMET.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Photon/diPhotonMET_hlt.pdf","pdf")

c.Clear()
diPhotonLeadPt.Draw()
diPhotonLeadPt.SetTitle("diPhoton:LeadingPhoton;Et;")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/diPhotonLeadPt_hlt.pdf","pdf")


c.Clear()
diPhotonTrailPt.Draw()
diPhotonTrailPt.SetTitle("diPhoton:TrailingPhoton;Et;")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/diPhotonTrailPt_hlt.pdf","pdf")

c.Clear()
PhotonNum.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("Photon/PhotonNum_hlt.pdf","pdf")

c.Clear()
deltaR.Draw()
deltaR.SetTitle("gammagamma-dR;dR;")
c.Print("Photon/deltaR_hlt.pdf","pdf")


c.Clear()
Leading1PhotonPt.Draw()
Leading1PhotonPt.SetTitle("SR1:LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/Leading1PhotonPt_hlt.pdf","pdf")

c.Clear()
Leading2PhotonPt.Draw()
Leading2PhotonPt.SetTitle("SR2: LeadingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/Leading2PhotonPt_hlt.pdf","pdf")

c.Clear()
Trailing2PhotonPt.Draw()
Trailing2PhotonPt.SetTitle("SR2: TrailingPhoton; Et; Events")
gPad.SetLogy()
gPad.Update()
c.Print("Photon/Trailing2PhotonPt_hlt.pdf","pdf")

sw.Stop()
print "Real Time:"+ str(sw.RealTime()/60.0) +"min"
print "CPU Time:"+ str(sw.CpuTime()/60.0) +"min"


