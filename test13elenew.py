#!/bin/python
# 2.15.2016 by Fan Xia
# susy single electron to diphoton


import os
import sys
import ROOT
from ROOT import *
from array import array

sw = ROOT.TStopwatch()
sw.Start()
print "start"
chain_in = ROOT.TChain("ggNtuplizer/EventTree_pre")
#chain_in.Add("root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/SilverJSON/job_data_ggNtuple_SingleElectron_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD.root")
#chain_in.Add("data/SingleElectron_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD__data_example.root")
chain_in.Add("SingleEle_pre/reduced_singleEle.root")
#chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()
print"Total events for processing: ",n_events

os.mkdir("SingleEle_v3",0755)
os.chdir("SingleEle_v3")


#------------
sr1bins = array('d',[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000])
SR1_SingleElePt = ROOT.TH1F("SR1_SingleElePt","SR1_SingleElePt",17,sr1bins)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",17,sr1bins)
sr1metxbins =array('d',[0,10,20,30,40,50,75,100,150,300,800])
SR1MET = ROOT.TH1F("SR1MET","SR1MET",10,sr1metxbins)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","SR1_LeadBjetPt",17,sr1bins)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",15,0,15,10,0,10)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)


sr2bins = array('d',[0,25,50,100,150,200,400,600,1000])
SR2_SingleElePt = ROOT.TH1F("SR2_SingleElePt","SR2_SingleElePt",8,sr2bins)
diPhotonM = ROOT.TH1F("diPhotonM","diPhotonM",8,sr2bins)
sr2metxbins=array('d',[0,20,50,100,800])
SR2MET = ROOT.TH1F("SR2MET","SR2MET",4,sr2metxbins)
SR2nPho = ROOT.TH1F("SR2nPho","SR2nPho",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","diPhotonM_MET",100,0,1000,100,0,1000)
SR2_LeadBjetPt = ROOT.TH1F("SR2_LeadBjetPt","SR2_LeadBjetPt",8,sr2bins)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","LeadPhoEt",8,sr2bins)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","TrailPhoEt",8,sr2bins)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","SR2_nJet_nbJet",15,0,15,10,0,10)
#SR2_nJet_nbJet_ratio = ROOT.TH2F("SR2_nJet_nbJet_ratio","SR2_nJet_nbJet_ratio",15,0,15,10,0,10)
#------------

SR18vs13= ROOT.TH1F("SR18-13","SR18-13",10,sr1metxbins)
fl=TFile.Open("../8vs13/histograms_ele_bjj_SR1.root")
SR1met=fl.Get("pfMET_t01_gg_ele_bjj")
file_out = ROOT.TFile("reduced_singleEle.root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
#dir2_out = file_out.mkdir("ggNtuplizer_SR2")
dir_out.cd()
tree_out = chain_in.CloneTree(0)
tree_out.SetName("EventTree_pre")
tree1_out = chain_in.CloneTree(0)
tree1_out.SetName("EventTree_SR1")
tree2_out = chain_in.CloneTree(0)
tree2_out.SetName("EventTree_SR2")

pho1=ROOT.TLorentzVector()
pho2=ROOT.TLorentzVector()

n_hlt=0
n_singleEle=0
n_pre=0
n_SR1=0
n_SR2=0

for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i
# -----------------1.HLT selection(HLT_Ele23_WPLoose_Gsf_v)

    hltele = chain_in.HLTEleMuX>>6&1
    if hltele!=1:
        continue
    n_hlt+=1


#-------------------1+2. only one tight ele
    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if chain_in.elePt[e]>30 and (chain_in.eleIDbit[e]>>3&1)==1 and abs(chain_in.eleEta[e])<2.5:
            n_tightEle+=1
            ele_ind=e
        if chain_in.elePt[e]>10 and (chain_in.eleIDbit[e]>>1&1)==1 and abs(chain_in.eleEta[e])<2.5:
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5 and chain_in.muIsLooseID[m]==1:
            n_looseMu+=1
    if n_looseMu !=0:
        continue

    n_singleEle+=1     


#--------------------1+2+3.at least 3 jets and 1 bjet
    n_jet=0
    n_bjet=0
    jetlist =[]
    bjetlist=[]
    for j in range(chain_in.nJet):
        if chain_in.jetPt[j]>30 and abs(chain_in.jetEta[j])<2.4:
            n_jet+=1
            jetlist.append(j)
            if chain_in.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
                bjetlist.append(j)
    if n_jet<3 or n_bjet<1:
        continue
    n_pre+=1
    leadbjet_ind=max(bjetlist,key=lambda x: chain_in.jetPt[x])
    tree_out.Fill()
#---------------------above for pre-selection---------------------


#---------------------1+2+3+4.loose photon: singlepho  or diphoton
    pholist1 = [] 
    for p in range(chain_in.nPho):
        if chain_in.phoEt[p]>=20 and abs(chain_in.phoEta[p])<=1.4442 and (chain_in.phoIDbit[p]>>0&1)==1 and (chain_in.phoEleVeto[p])==1 and chain_in.phoR9[p]<1.0 and chain_in.phoSigmaIPhiIPhi[p]>0.001 and chain_in.phoSigmaIEtaIEta[p]>0.001  and chain_in.phoSigmaIEtaIEta[p]<0.012:
            pholist1.append(p)

#---------------------photon dR loop----
    pholist2=[]
    for p1 in pholist1:
        dRphoton_ele = ((chain_in.phoEta[p1]-chain_in.eleEta[ele_ind])**2+(chain_in.phoPhi[p1]-chain_in.elePhi[ele_ind])**2)**0.5
        if dRphoton_ele<=0.7:
            continue
        pholist2.append(p1)
        
    pholist3=[]
    for p2 in pholist2:
        w = 1
        for j in jetlist:
            dRphoton_jet = ((chain_in.phoEta[p2]-chain_in.jetEta[j])**2+(chain_in.phoPhi[p2]-chain_in.jetPhi[j])**2)**0.5
#            if dRphoton_jet<=0.7:
#                w=0
#                break
        if w==1:
            pholist3.append(p2)

    pholist=[]
    for p3 in pholist3:
        w = 1
        for p4 in pholist3:
            dRphoton_photon = ((chain_in.phoEta[p3]-chain_in.phoEta[p4])**2+(chain_in.phoPhi[p3]-chain_in.phoPhi[p4])**2)**0.5
            if dRphoton_photon<=0.5 and p4!=p3:
                w=0
                break
        if w==1:
            pholist.append(p3)


#-------------------------below for signal region1 &2
    if len(pholist)==1:
        singlepho_ind=pholist[0]
        (n_SR1)+=1
        tree1_out.Fill()
        SR1MET.Fill(chain_in.pfMET)
        SinglePhoEt.Fill(chain_in.phoEt[singlepho_ind])
        SR1_nJet_nbJet.Fill(n_jet,n_bjet)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet)
        SR1_SingleElePt.Fill(chain_in.elePt[ele_ind])
        SR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])

    elif len(pholist)>=2:    
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
#        phodR=pho1.DeltaR(pho2)
#        if phodR<0.5:
#            continue
        (n_SR2)+=1
        tree2_out.Fill()
        SR2nPho.Fill(len(pholist))
        diPhotonM.Fill((pho1+pho2).M())
        SR2MET.Fill(chain_in.pfMET)
        SR2_SingleElePt.Fill(chain_in.elePt[ele_ind])
        diPhotonM_MET.Fill((pho1+pho2).M(),chain_in.pfMET)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind])
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind])
        SR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
        SR2_nJet_nbJet.Fill(n_jet,n_bjet)



file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_hlt pass = ", n_hlt
print "n_singleEle pass = ", n_singleEle
print "n_pre selection = ",n_pre
print "n_SR1 = ", n_SR1
print "n_SR2 = ", n_SR2
print "----------------------"

c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
for i in range(1,11):
    SR1MET.SetBinContent(i,SR1MET.GetBinContent(i)/SR1MET.GetBinWidth(i))
SR1MET.Draw("e")
SR1MET.SetTitle("EleChannel SR1:MET;MET (GeV); Event Number/GeV")
gStyle.SetOptStat(0)
gPad.SetLogy()
gPad.Update()
c.Print("SR1MET.pdf","pdf")

#-----------
c.Clear()
#SR18vs13=SR1MET.Divide(SR1met)
SR1MET.Divide(SR1met)
SR1MET.Draw()
c.Print("SR1metvs.pdf","pdf")

c.Clear()
for i in range(1,18):
    SR1_SingleElePt.SetBinContent(i,SR1_SingleElePt.GetBinContent(i)/SR1_SingleElePt.GetBinWidth(i))
SR1_SingleElePt.Draw()
SR1_SingleElePt.SetTitle("EleChannel SR1;ele_Pt (GeV/c); Event Number/GeV")
gStyle.SetOptStat(0)
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SingleEle.pdf","pdf")


c.Clear()
for i in range(1,18):
    SinglePhoEt.SetBinContent(i,SinglePhoEt.GetBinContent(i)/SinglePhoEt.GetBinWidth(i))
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Et} (GeV); Event Number/GeV")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEt.pdf","pdf")

c.Clear()
for i in range(1,18):
    SR1_LeadBjetPt.SetBinContent(i,SR1_LeadBjetPt.GetBinContent(i)/SR1_LeadBjetPt.GetBinWidth(i))
SR1_LeadBjetPt.Draw()
SR1_LeadBjetPt.SetTitle("SR1;Lead bjet_Pt (GeV/c); Event Number/GeV")
c.Print("SR1_LeadBjetPt.pdf","pdf")

c.Clear()
for i in range(1,9):
    SR2_SingleElePt.SetBinContent(i,SR2_SingleElePt.GetBinContent(i)/SR2_SingleElePt.GetBinWidth(i))
SR2_SingleElePt.Draw()
SR2_SingleElePt.SetTitle("EleChannel SR2;ele_Pt (GeV/c); Event Number/GeV")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_SingleElePt.pdf","pdf")

c.Clear()
for i in range(1,5):
    SR2MET.SetBinContent(i,SR2MET.GetBinContent(i)/SR2MET.GetBinWidth(i))
SR2MET.Draw("e")
SR2MET.SetTitle("EleChannel SR2:MET;MET (GeV);Event Number/GeV")
gPad.SetLogy()
gPad.Update()
c.Print("SR2MET.pdf","pdf")

c.Clear()
for i in range(1,9):
    diPhotonM.SetBinContent(i,diPhotonM.GetBinContent(i)/diPhotonM.GetBinWidth(i))
diPhotonM.Draw("e")
diPhotonM.SetTitle("SR2: #gamma#gamma;m_{#gamma#gamma} (GeV); Event Number/GeV")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_diPhotonM.pdf","pdf")

c.Clear()
SR2nPho.Draw()
SR2nPho.SetTitle("SR2;n_Photon;")
c.Print("SR2nPho.pdf","pdf")

c.Clear()
for i in range(1,9):
    LeadPhoEt.SetBinContent(i,LeadPhoEt.GetBinContent(i)/LeadPhoEt.GetBinWidth(i))
LeadPhoEt.Draw()
LeadPhoEt.SetTitle("SR2:Lead #gamma;Lead #gamma_Et(GeV); Event Number/GeV")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_LeadPhoEt.pdf","pdf")

c.Clear()
for i in range(1,9):
    TrailPhoEt.SetBinContent(i,TrailPhoEt.GetBinContent(i)/TrailPhoEt.GetBinWidth(i))
TrailPhoEt.Draw()
TrailPhoEt.SetTitle("SR2:Trail #gamma;Trail #gamma_Et(GeV); Event Number/GeV")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_TrailPhoEt.pdf","pdf")


c.Clear()
for i in range(1,9):
    SR2_LeadBjetPt.SetBinContent(i,SR2_LeadBjetPt.GetBinContent(i)/SR2_LeadBjetPt.GetBinWidth(i))
SR2_LeadBjetPt.Draw()
SR2_LeadBjetPt.SetTitle("SR2;Lead bjet_Pt (GeV/c); Event Number/GeV")
c.Print("SR2_LeadBjetPt.pdf","pdf")

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


