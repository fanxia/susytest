import ROOT
import sys
import os

from ROOT import *
  #get old file, old tree and set top branch address
oldfile=TFile.Open('root://xrootd-cms.infn.it//store/group/phys_smp/ggNtuples/13TeV/data/V07_04_14_00/GoldenJSON/job_SinglePho_Run2015D_PR_v4_miniAOD.root')
oldtree=oldfile.Get('ggNtuplizer/EventTree')
oldtree.SetBranchStatus("*",1)
nEntries=oldtree.GetEntries()
#new file to store some entries
newfile=ROOT.TFile("photon_data_example.root","recreate")
newdir=newfile.mkdir("ggNtuplizer")
newdir.cd()
newtree=oldtree.CloneTree(100000)
newfile.Write()
newfile.Close()
