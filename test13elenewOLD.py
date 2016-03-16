#!/bin/python
# 2.15.2016 by Fan Xia
# susy single electron to diphoton


import os
import sys
import ROOT
from ROOT import *
from array import array
from ana_mu import muPFRelCombIso

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

#os.mkdir("Output_SingleEle_v315",0755)
os.system('mkdir -p Output_SingleEle_v315')
os.chdir("Output_SingleEle_v315")


#------------

pre_SingleElePt = ROOT.TH1F("pre_SingleElePt","pre_SingleElePt",100,0,1000)
pre_SingleEleEta = ROOT.TH1F("pre_SingleEleEta","pre_SingleEleEta",60,-3,3)
pre_nPho = ROOT.TH1F("pre_nPho","pre_nPho",5,0,5)
pre_nJet = ROOT.TH1F("pre_nJet","pre_nJet",15,0,15)
preMET = ROOT.TH1F("preMET","preMET",100,0,1000)
pre_LeadBjetPt = ROOT.TH1F("pre_LeadBjetPt","pre_LeadBjetPt",100,0,1000)
pre_nJet_nbJet = ROOT.TH2F("pre_nJet_nbJet","pre_nJet_nbJet",20,0,20,10,0,10)


SR1_SingleElePt = ROOT.TH1F("SR1_SingleElePt","SR1_SingleElePt",100,0,1000)
SinglePhoEt = ROOT.TH1F("SinglePhoEt","SinglePhoEt",100,0,1000)
SinglePhoEta = ROOT.TH1F("SinglePhoEta","SinglePhoEta",60,-3,3)
SinglePhoR9 = ROOT.TH1F("SinglePhoR9","SinglePhoR9",60,0,1.2)
SinglePhoSigmaIEtaIEta = ROOT.TH1F("SinglePhoSigmaIEtaIEta","SinglePhoSigmaIEtaIEta",100,0,0.05)
SinglePhoSigmaIPhiIPhi = ROOT.TH1F("SinglePhoSigmaIPhiIPhi","SinglePhoSigmaIPhiIPhi",100,0,0.1)
SR1MET = ROOT.TH1F("SR1MET","SR1MET",100,0,1000)
SR1_LeadBjetPt = ROOT.TH1F("SR1_LeadBjetPt","SR1_LeadBjetPt",100,0,1000)
SR1_nJet_nbJet = ROOT.TH2F("SR1_nJet_nbJet","SR1_nJet_nbJet",15,0,15,10,0,10)
SR1invelepho = ROOT.TH1F("SR1invelepho","SR1invelepho",100,0,1000)
#SR1_nJet_nbJet_ratio = ROOT.TH2F("SR1_nJet_nbJet_ratio","SR1_nJet_nbJet_ratio",15,0,15,10,0,10)



SR2_SingleElePt = ROOT.TH1F("SR2_SingleElePt","SR2_SingleElePt",100,0,1000)
diPhotonM = ROOT.TH1F("diPhotonM","diPhotonM",100,0,1000)
SR2MET = ROOT.TH1F("SR2MET","SR2MET",100,0,1000)
SR2nPho = ROOT.TH1F("SR2nPho","SR2nPho",5,0,5)
diPhotonM_MET = ROOT.TH2F("diPhotonM_MET","diPhotonM_MET",100,0,1000,100,0,1000)
SR2_LeadBjetPt = ROOT.TH1F("SR2_LeadBjetPt","SR2_LeadBjetPt",100,0,1000)
LeadPhoEt = ROOT.TH1F("LeadPhoEt","LeadPhoEt",100,0,1000)
TrailPhoEt = ROOT.TH1F("TrailPhoEt","TrailPhoEt",100,0,1000)
SR2_nJet_nbJet = ROOT.TH2F("SR2_nJet_nbJet","SR2_nJet_nbJet",15,0,15,10,0,10)
#SR2_nJet_nbJet_ratio = ROOT.TH2F("SR2_nJet_nbJet_ratio","SR2_nJet_nbJet_ratio",15,0,15,10,0,10)
#------------

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

SR2pho1=ROOT.TLorentzVector()
SR2pho2=ROOT.TLorentzVector()
SR1pho=ROOT.TLorentzVector()
Trigele=ROOT.TLorentzVector()

n_hlt=0
n_singleEle=0
n_pre=0
n_SR1=0
n_SR2=0

#for i in range(1000):
for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i

##----------------0.5Vertex clean

#    if abs(chain_in.vtz)>24 or abs(chain_in.rho)>2: continue     //error here since the rho is not the "rho"


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
        muPFIso=muPFRelCombIso(chain_in.muPt[m],chain_in.muPFChIso[m],chain_in.muPFNeuIso[m],chain_in.muPFPhoIso[m],chain_in.muPFPUIso[m])
#        print "iso",i,"---",muPFIso
        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5 and chain_in.muIsLooseID[m] and muPFIso<0.25:
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
        if chain_in.jetPt[j]>30 and abs(chain_in.jetEta[j])<2.4 and chain_in.jetPFLooseId[j]:
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
        if chain_in.phoEt[p]>=20 and abs(chain_in.phoEta[p])<=1.4442 and (chain_in.phoIDbit[p]>>0&1)==1 and (chain_in.phoEleVeto[p])==1:
# and chain_in.phoR9[p]<1.0 and chain_in.phoSigmaIPhiIPhi[p]>0.001 and chain_in.phoSigmaIEtaIEta[p]>0.001  and chain_in.phoSigmaIEtaIEta[p]<0.012:
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

    Trigele.SetPtEtaPhiM(chain_in.elePt[ele_ind],chain_in.eleEta[ele_ind],chain_in.elePhi[ele_ind],0.000511)
#-----------------------below for pre plots
    pre_nPho.Fill(len(pholist))
    pre_SingleElePt.Fill(chain_in.elePt[ele_ind])
    pre_SingleEleEta.Fill(chain_in.eleEta[ele_ind])
    pre_nJet_nbJet.Fill(n_jet,n_bjet)
    pre_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
    preMET.Fill(chain_in.pfMET)
    pre_nJet.Fill(n_jet)


#-------------------------below for signal region1 &2
    if len(pholist)==1:
        singlepho_ind=pholist[0]
        (n_SR1)+=1
        SR1pho.SetPtEtaPhiM(chain_in.phoEt[singlepho_ind],chain_in.phoEta[singlepho_ind],chain_in.phoPhi[singlepho_ind],0.0)
        tree1_out.Fill()
        SR1MET.Fill(chain_in.pfMET)
        SinglePhoEt.Fill(chain_in.phoEt[singlepho_ind])
        SinglePhoEta.Fill(chain_in.phoEta[singlepho_ind])
        SinglePhoR9.Fill(chain_in.phoR9[singlepho_ind])
        SinglePhoSigmaIPhiIPhi.Fill(chain_in.phoSigmaIPhiIPhi[singlepho_ind])
        SinglePhoSigmaIEtaIEta.Fill(chain_in.phoSigmaIEtaIEta[singlepho_ind])
        SR1invelepho.Fill((Trigele+SR1pho).M())

        SR1_nJet_nbJet.Fill(n_jet,n_bjet)
#        SR1_nJet_nbJet_ratio.Fill(n_jet,n_bjet)
        SR1_SingleElePt.Fill(chain_in.elePt[ele_ind])
        SR1_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])

    elif len(pholist)>=2:    
        leadpho_ind=max(pholist,key=lambda x: chain_in.phoEt[x])
        trailpho_ind=max([pp for pp in pholist if pp!=leadpho_ind],key=lambda x: chain_in.phoEt[x])
        SR2pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
        SR2pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
#        phodR=pho1.DeltaR(pho2)
#        if phodR<0.5:
#            continue
        (n_SR2)+=1
        tree2_out.Fill()
        SR2nPho.Fill(len(pholist))
        diPhotonM.Fill((SR2pho1+SR2pho2).M())
        SR2MET.Fill(chain_in.pfMET)
        SR2_SingleElePt.Fill(chain_in.elePt[ele_ind])
        diPhotonM_MET.Fill((SR2pho1+SR2pho2).M(),chain_in.pfMET)
        LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind])
        TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind])
        SR2_LeadBjetPt.Fill(chain_in.jetPt[leadbjet_ind])
        SR2_nJet_nbJet.Fill(n_jet,n_bjet)



#file_out.Write()
#file_out.Close()

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
pre_nPho.Draw()
gPad.SetLogy()
gPad.Update()
c.Print("pre_nPho.pdf","pdf")

c.Clear()
pre_nJet.Draw()
c.Print("pre_nJet.pdf","pdf")


c.Clear()
preMET.Draw("e")
preMET.SetTitle("Elehannel pre:MET;MET (GeV);")
c.Print("preMET.pdf","pdf")


c.Clear()
pre_SingleElePt.Draw()
pre_SingleElePt.SetTitle("EleChannel pre;ele_Pt (GeV/c);")
c.Print("pre_SingleEle.pdf","pdf")

c.Clear()
pre_SingleEleEta.Draw()
pre_SingleEleEta.SetTitle("EleChannel pre;ele_Eta;")
c.Print("pre_SingleEleEta.pdf","pdf")


c.Clear()
pre_LeadBjetPt.Draw()
pre_LeadBjetPt.SetTitle("pre;Lead bjet_Pt (GeV/c);")
c.Print("pre_LeadBjetPt.pdf","pdf")

c.Clear()
SR1MET.Draw("e")
SR1MET.SetTitle("EleChannel SR1:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("SR1MET.pdf","pdf")


c.Clear()
SR1_SingleElePt.Draw()
SR1_SingleElePt.SetTitle("EleChannel SR1;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SingleEle.pdf","pdf")


c.Clear()
SinglePhoR9.Draw()
SinglePhoR9.SetTitle("SR1:;#gamma_R9;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoR9.pdf","pdf")

c.Clear()
SinglePhoSigmaIEtaIEta.Draw()
SinglePhoSigmaIEtaIEta.SetTitle("SR1:;#gamma_i#etai#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoSigmaIEtaIEta.pdf","pdf")

c.Clear()
SinglePhoSigmaIPhiIPhi.Draw()
SinglePhoSigmaIPhiIPhi.SetTitle("SR1:;#gamma_i#phii#phi;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoSigmaIPhiIPhi.pdf","pdf")

c.Clear()
SinglePhoEt.Draw()
SinglePhoEt.SetTitle("SR1: #gamma;#gamma_{Et} (GeV);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEt.pdf","pdf")

c.Clear()
SinglePhoEta.Draw()
SinglePhoEta.SetTitle("SR1: #gamma;#gamma_#eta;")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR1_SinglePhoEta.pdf","pdf")


c.Clear()
SR1_LeadBjetPt.Draw()
SR1_LeadBjetPt.SetTitle("SR1;Lead bjet_Pt (GeV/c);")
c.Print("SR1_LeadBjetPt.pdf","pdf")


c.Clear()
SR1invelepho.SetTitle("SR1;invmass_e#gamma;")
SR1invelepho.Draw()
c.Print("SR1invelepho.pdf","pdf")

c.Clear()
SR2_SingleElePt.Draw()
SR2_SingleElePt.SetTitle("EleChannel SR2;ele_Pt (GeV/c);")
#gPad.SetLogy()
#gPad.Update()
c.Print("SR2_SingleElePt.pdf","pdf")

c.Clear()
SR2MET.Draw("e")
SR2MET.SetTitle("EleChannel SR2:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
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
c.Print("SR2nPho.pdf","pdf")

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
SR2_LeadBjetPt.Draw()
SR2_LeadBjetPt.SetTitle("SR2;Lead bjet_Pt (GeV/c);")
c.Print("SR2_LeadBjetPt.pdf","pdf")

c.Clear()
c.SetRightMargin(0.14)
pre_nJet_nbJet.Draw("colz")
pre_nJet_nbJet.SetTitle("pre;n_Jet;nbJet")
gStyle.SetOptStat(0)
#gPad.SetLogy(0)
#gPad.SetLogz()                                                
#gPad.Update()
c.Print("pre_nJet_nbJet.pdf","pdf")

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


file_out.Write()
file_out.Close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


