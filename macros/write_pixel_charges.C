#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include "TFile.h"
#include "TKey.h"
#include "TObjArray.h"
#include "TBranch.h"
#include "TTree.h"
#include "TH2D.h"
using namespace std;

// Heuristic ROOT macro to extract x y charge rows.
// Tries to find a TTree containing pixel/charge branches (PixelCharge-like).
// Falls back to reading a TH2D named "charge_map;1" if no tree is found.
void write_pixel_charges(const char* inputPath, const char* outputPath){
  TFile *file = TFile::Open(inputPath);
  if(!file || file->IsZombie()){
    cerr << "Error: cannot open " << inputPath << endl;
    return;
  }

  ofstream out(outputPath);
  if(!out.is_open()){
    cerr << "Error: cannot open output file " << outputPath << endl;
    file->Close();
    return;
  }

  // Search keys for TTrees that might contain pixel charge info
  TIter next(file->GetListOfKeys());
  TKey *key;
  bool wrote = false;

  const set<string> xCandidates = {"x","X","pixelX","pixel_x","col","column","pixelColumn","pixel_column","ix","iX"};
  const set<string> yCandidates = {"y","Y","pixelY","pixel_y","row","pixelRow","pixel_row","iy","iY"};
  const set<string> chargeCandidates = {"charge","Charge","amplitude","Amplitude","value","weight","signal"};

  while((key=(TKey*)next())){
    TObject *obj = key->ReadObj();
    if(!obj) continue;
    if(obj->InheritsFrom("TTree")){
      TTree *tree = (TTree*)obj;
      TObjArray *branches = tree->GetListOfBranches();
      string bx,by,bq;
      for(int bi=0; bi<branches->GetEntries(); ++bi){
        TBranch *br = (TBranch*)branches->At(bi);
        string name = br->GetName();
        if(bx.empty()){
          for(auto &c: xCandidates) if(name==c) { bx=name; break; }
        }
        if(by.empty()){
          for(auto &c: yCandidates) if(name==c) { by=name; break; }
        }
        if(bq.empty()){
          for(auto &c: chargeCandidates) if(name==c) { bq=name; break; }
        }
      }

      if(!bx.empty() && !by.empty() && !bq.empty()){
        // Try to read numeric branches
        double x=0, y=0, q=0;
        tree->SetBranchStatus("*",0);
        tree->SetBranchStatus(bx.c_str(),1);
        tree->SetBranchStatus(by.c_str(),1);
        tree->SetBranchStatus(bq.c_str(),1);
        if(tree->SetBranchAddress(bx.c_str(), &x) == 0) {
          // continue: SetBranchAddress returns 0 on failure for some ROOT versions, ignore
        }
        tree->SetBranchAddress(by.c_str(), &y);
        tree->SetBranchAddress(bq.c_str(), &q);

        Long64_t n = tree->GetEntries();
        for(Long64_t i=0;i<n;++i){
          tree->GetEntry(i);
          out << x << " " << y << " " << q << "\n";
        }
        wrote = true;
        break; // done
      }
    }
    // If object is a directory, try to find a TH2D inside
    if(obj->InheritsFrom("TDirectory")){
      TDirectory *dir = (TDirectory*)obj;
      // look for TH2D named charge_map;1
      TH2D *h = (TH2D*)dir->Get("charge_map;1");
      if(h){
        for (int i = 1; i <= h->GetNbinsX(); ++i) {
          for (int j = 1; j <= h->GetNbinsY(); ++j) {
            double x = h->GetXaxis()->GetBinCenter(i);
            double y = h->GetYaxis()->GetBinCenter(j);
            double content = h->GetBinContent(i, j);
            if(content != 0) out << x << " " << y << " " << content << "\n";
          }
        }
        wrote = true;
        break;
      }
    }
  }

  // Fallback: try to get TH2D at top-level
  if(!wrote){
    TH2D *h = (TH2D*)file->Get("charge_map;1");
    if(h){
      for (int i = 1; i <= h->GetNbinsX(); ++i) {
        for (int j = 1; j <= h->GetNbinsY(); ++j) {
          double x = h->GetXaxis()->GetBinCenter(i);
          double y = h->GetYaxis()->GetBinCenter(j);
          double content = h->GetBinContent(i, j);
          if(content != 0) out << x << " " << y << " " << content << "\n";
        }
      }
      wrote = true;
    }
  }

  if(!wrote) cerr << "Warning: no pixel-charge tree or histogram found in " << inputPath << endl;

  out.close();
  file->Close();
}
