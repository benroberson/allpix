#include <iostream>
#include "TROOT.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1F.h"
#include "TBrowser.h"
#include "TFrame.h"
#include "TApplication.h"
#include "stdbool.h"

void hist_data(const char* inputPath, const char* outputPath){
  TFile *results = TFile::Open(inputPath);
  //const char* parentDir = "DetectorHistogrammer/project_detector/charge";
  //results->cd(parentDir);
  TH1F::AddDirectory(false);

  TCanvas *canvas_n2;
  TKey *key_n2 = results->FindKeyAny("charge_map;1");
  if(key_n2 != NULL){
    //gDirectory->GetObject("charge_map;1", canvas_n2);
    TH2D* n2 = new TH2D("name","title", 100, 0, 100,0,100);
    gDirectory->GetObject("charge_map;1", n2);                                                                                

    ofstream myfile;
    myfile.open(outputPath);

    for (int i = 1; i <= n2->GetNbinsX(); ++i) {
      for (int j = 1; j <= n2->GetNbinsY(); ++j) {
	double x = n2->GetXaxis()->GetBinCenter(i);
	double y = n2->GetYaxis()->GetBinCenter(j);
	double content = n2->GetBinContent(i, j);
	if( content != 0)	
	  myfile << x << " " << y << " " << content << endl;
        // Save X, Y, and Content (Z)
      }
    }
    myfile.close();

  }

}
