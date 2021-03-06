#!/bin/python
# 2.15.2016 by Fan Xia
# susy single Muon channel


import os
import sys
import ROOT
from ROOT import *

sw = ROOT.TStopwatch()
sw.Start()

chain_in = ROOT.TChain("ggNtuplizer/EventTree")
#chain_in.Add("root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/SilverJSON/job_data_ggNtuple_SingleMuon_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD.root")
chain_in.Add("data/SingleMuon_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD__data_example.root")
chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

os.mkdir("SingleMu_v1",0755)
os.chdir("SingleMu_v1")


#------------
SR1_SingleMuPt = ROOT.TH1F("SR1_SingleMuPt","SR1_SingleMuPt",100,0,1000)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",100,0,1000)
SR1MET = ROOT.TH1F("SR1MET","SR1MET",100,0,1000)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",40,0,40,40,0,40)

SR2_SingleMuPt = ROOT.TH1F("SR2_SingleMuPt","SR2_SingleMuPt",100,0,1000)
diPhotonM = ROOT.TH1F("diPhotonM","diPhotonM",100,0,1000)
SR2MET = ROOT.TH1F("SR2MET","SR2MET",100,0,1000)
SR2nPho = ROOT.TH1F("SR2nPho","SR2nPho",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","diPhotonM_MET",100,0,1000,100,0,1000)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","LeadPhoEt",100,0,1000)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","TrailPhoEt",100,0,1000)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","SR2_nJet_nbJet",40,0,40,40,0,40)
#------------


file_out = ROOT.TFile("reduced_singleMu.root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
#dir2_out = file_out.mkdir("ggNtuplizer_SR2")
dir_out.cd()
tree1_out = chain_in.CloneTree(0)
tree1_out.SetName("EventTree_SR1")
tree2_out = chain_in.CloneTree(0)
tree2_out.SetName("EventTree_SR2")

pho1=ROOT.TLorentzVector()
pho2=ROOT.TLorentzVector()

n_hlt=0
n_singleMu=0
n_SR1=0
n_SR2=0

for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i
# -----------------1.HLT selection(HLT_IsoMu24_eta2p1_v)  ID=24

    hltmu = chain_in.HLTEleMuX>>24&1
    if hltmu!=1:
        continue
    n_hlt+=1


#-------------------1+2. only one tight muon
    n_tightMu=0
    n_looseMu=0
    for m in range(chain_in.nMu):
        if chain_in.muPt[m]>30 and (chain_in.muIsTightID[m])==1 and abs(chain_in.muEta[m])<2.1:
            n_tightMu+=1
            mu_ind=m
        if chain_in.muPt[m]>10 and (chain_in.muIsLooseID[m])==1 and abs(chain_in.muEta[m])<2.5:
            n_looseMu+=1
    if n_tightMu !=1 or n_looseMu !=1:
        continue

    n_looseEle=0
    for e in range(chain_in.nEle):
        if chain_in.elePt[m]>10 and abs(chain_in.eleIDbit[e]>>1&1)==1:
            n_looseEle+=1
    if n_looseEle !=0:
        continue

    n_singleMu+=1     


#--------------------1+2+3.at least 3 jets and 1 bjet
    n_jet=0
    n_bjet=0
    for j in range(chain_in.nJet):
        if chain_in.jetPt[j]>30 and abs(chain_in.jetEta[j])<2.4:
            n_jet+=1
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
    if n_jet<3 or n_bjet<1:
        continue


#---------------------1+2+3+4.loose photon: singlepho  or diphoton
    pholist = [] 
    for p in range(chain_in.nPho):
        if chain_in.phoEt[p]>=20 and abs(chain_in.phoEta[p])<=1.4442 and (chain_in.phoIDbit[p]>>0&1)==1:
            pholist.append(p)

    if len(pholist)==1:
        singlepho_ind=pholist[0]
        (n_SR1)+=1
        SR1MET.Fill(chain_in.pfMET)
        SinglePhoEt.Fill(chain_in.phoEt[singlepho_ind])
        SR1_nJet_nbJet.Fill(n_jet,n_bjet)
        SR1_SingleMuPt.Fill(chain_in.muPt[mu_ind])
        tree1_out.Fill()
    elif len(pholist)>=2:    
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
        phodR=pho1.DeltaR(pho2)
        if phodR<0.5:
            continue
        (n_SR2)+=1
        SR2nPho.Fill(len(pholist))
        diPhotonM.Fill((pho1+pho2).M())
        SR2MET.Fill(chain_in.pfMET)
        SR2_SingleMuPt.Fill(chain_in.muPt[mu_ind])
        diPhotonM_MET.Fill((pho1+pho2).M(),chain_in.pfMET)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind])
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind])
        SR2_nJet_nbJet.Fill(n_jet,n_bjet)
        tree2_out.Fill()


file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_hlt pass = ", n_hlt
print "n_singleMu pass = ", n_singleMu
print "n_SR1 = ", n_SR1
print "n_SR2 = ", n_SR2
print "----------------------"

c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
SR1MET.Draw()
SR1MET.SetTitle("Muon Channel SR1:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("SR1MET.pdf","pdf")


c.Clear()
SR1_SingleMuPt.Draw()
SR1_SingleMuPt.SetTitle("Muon Channel SR1;mu_Pt (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SingleMu.pdf","pdf")


c.Clear()
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Pt} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEt.pdf","pdf")


c.Clear()
SR2_SingleMuPt.Draw()
SR2_SingleMuPt.SetTitle("MuonChannel SR2;mu_Pt (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_SingleMu.pdf","pdf")

c.Clear()
SR2MET.Draw()
SR2MET.SetTitle("MuonChannel SR2:MET;MET (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2MET.pdf","pdf")

c.Clear()
diPhotonM.Draw("e")
diPhotonM.SetTitle("SR2: #gamma#gamma;m_{#gamma#gamma} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_diPhotonM.pdf","pdf")

c.Clear()
SR2nPho.Draw()
SR2nPho.SetTitle("SR2;n_Photon;")
c.Print("SR2nPho","pdf")

c.Clear()
LeadPhoEt.Draw()
LeadPhoEt.SetTitle("SR2:Lead #gamma;Lead #gamma_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_LeadPhoEt.pdf","pdf")

c.Clear()
TrailPhoEt.Draw()
TrailPhoEt.SetTitle("SR2:Trail #gamma;Trail #gamma_Et(GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_TrailPhoEt.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR1_nJet_nbJet.Draw("colz")
SR1_nJet_nbJet.SetTitle("SR1;n_Jet;nbJet")
gStyle.SetOptStat(0)
gPad.SetLogy(0)
gPad.SetLogz()                                                                                                
gPad.Update()
c.Print("SR1_nJet_nbJet.pdf","pdf")


c.Clear()
c.SetRightMargin(0.14)
SR2_nJet_nbJet.Draw("colz")
SR2_nJet_nbJet.SetTitle("SR2;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                                                                
#gPad.Update()
c.Print("SR2_nJet_nbJet.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
c.SetLeftMargin(0.12)
diPhotonM_MET.Draw("colz")
diPhotonM_MET.SetTitle("SR2: diPhotonMass vs MET;m_{#gamma#gamma} (GeV); MET")
diPhotonM_MET.GetYaxis().SetTitleOffset(1.5)
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()
#gPad.Update()
c.Print("SR2_diPhotonM_MET.pdf","pdf")

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


