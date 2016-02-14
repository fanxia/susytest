#!/bin/python
# 2.12.2016 by Fan Xia
# susy diphoton to single lepton


import os
import sys
import ROOT
from ROOT import *

sw = ROOT.TStopwatch()
sw.Start()

chain_in = ROOT.TChain("ggNtuplizer/EventTree")
chain_in.Add("root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/SilverJSON/job_data_ggNtuple_DoubleEG_Run2015D_PromptReco-v4_25ns_JSON_Silver_1915pb_miniAOD.root")
chain_in.SetBranchStatus("tau*",0)
n_events = chain_in.GetEntries()

os.mkdir("Diphoton_v1",0755)
os.chdir("Diphoton_v1")
file_out = ROOT.TFile("reduced_  .root","recreate")
dir_out = file_out.mkdir("ggNtuplizer")
dir_out.cd()
tree_out = chain_in.CloneTree(0)

#------------


#------------

pho1=ROOT.TLorentzVector()
pho2=ROOT.TLorentzVector()

n_hlt=0
n_dipho=0
n_selectevent=0

for i in range(n_events):
    chain_in.GetEntry(i)
    
    if i%100000 ==0:
        print "Processing entry ", i

    hlt1=chain_in.HLTPho >>14&1
    hlt2=chain_in.HLTPho >>15&1
    hlt3=chain_in.HLTPho >>16&1
    hlt4=chain_in.HLTPho >>17&1

    hltpho = hlt1&hlt2&hlt3&hlt4
    if hltpho!=1:
        continue
    n_hlt+=1
     
    pholist = [] 
    for p in range(chain_in.nPho):
        if chain_in.phoEt[p]>=20 and abs(chain_in.phoEta[p])<=1.4442 and (chain_in.phoIDbit[p]>>0&1)==1:
            pholist.append(p)
    if len(pholist)!=2:
        continue
    
    leadpho_ind=max(pholist,key=lambda x: phoEt[x])
    trailpho_ind=min(pholist,key=lambda x: phoEt[x])
    pho1.SetPtEtaPhiM(chain_in.phoEt[leadpho_ind],chain_in.phoEta[leadpho_ind],chain_in.phoPhi[leadpho_ind],0.0)
    pho2.SetPtEtaPhiM(chain_in.phoEt[trailpho_ind],chain_in.phoEta[trailpho_ind],chain_in.phoPhi[trailpho_ind],0.0)
    phodR=pho1.DeltaR(pho2)
    if phodR<0.5:
        continue
    n_dipho+=1

    n_tightEle=0
    n_looseEle=0
    for e in range(chain_in.nEle):
        if chain_in.elePt[e]>30 and (chain_in.eleIDbit[e]>>3&1)==1:
            n_tightEle+=1
            ele_ind=e
        if chain_in.elePt[e]>10 and (chain_in.eleIDbit[e]>>1&1)==1:
            n_looseEle+=1
    if n_tightEle !=1 or n_looseEle !=1:
        continue

    n_looseMu=0
    for m in range(chain_in.nMu):
        if chain_in.muPt[m]>10 and abs(chain_in.muEta[m])<2.5:
            n_looseMu+=1
    if n_looseMu !=0:
        continue

    n_jet=0
    n_bjet=0
    for j in range(chain_in.nJet):
        if chain_in.jetPt[j]>30 and abs(chain_in.jetEta[j])<2.4:
            n_jet+=1
            if chain_in.pfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.89:
                n_bjet+=1
    if n_jet<3 or n_bjet<1:
        continue

    n_selectevent+=1
    tree_out.Fill()

    diPhotonM.Fill((pho1+pho2).M())
    SR2MET.Fill(chain_in.pfMET)
    diPhotonM_MET.Fill((pho1+pho2).M(),chain_in.pfMET)
    LeadPhoEt.Fill(chain_in.phoEt[leadpho_ind])
    TrailPhoEt.Fill(chain_in.phoEt[trailpho_ind])
    nJet_nbJet.Fill(n_jet,n_bjet)

file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", n_events
print "n_hlt pass = ", n_hlt
print "n_diphoton pass = ", n_dipho 
print "n_selectevent = ", n_selectevent
print "----------------------"

c=ROOT.TCanvas("c","Plots",800,800)
c.cd()
diPhotonM.Draw("e")
diPhotonM.SetTitle("diPhoton_mass;m_{#gamma#gamma} (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("diPhotonM.pdf","pdf")

c.Clear()
SR2MET.Draw()
SR2MET.SetTitle("EleChannel SR2:MET;MET (GeV);")
gPad.SetLogy()
gPad.Update()
c.Print("SR2MET.pdf","pdf")

c.Clear()
diPhotonM_MET.Draw("colz")
diPhotonM_MET.SetTitle("diPhotonMass vs MET;m_{#gamma#gamma} (GeV); MET")
c.Print("diPhotonM_MET.pdf","pdf")

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"


