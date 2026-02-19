#include <iostream>
#include "TROOT.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1F.h"
#include "TBrowser.h"
#include "TFrame.h"
#include "TApplication.h"
#include "stdbool.h"

void save_histogram(const char* inputPath, const char* outputPath ){
  TFile *results = TFile::Open(inputPath);
  const char* parentDir = "DetectorHistogrammer/project_detector/charge";
  results->cd(parentDir);
  TH1F::AddDirectory(false);

  TCanvas *canvas_n2;
  TKey *key_n2 = results->FindKeyAny("charge_map;1");
  if(key_n2 != NULL){
    //gDirectory->GetObject("charge_map;1", canvas_n2);
    TH2D* n2 = new TH2D("name","title", 100, 0, 100,0,100);
    gDirectory->GetObject("charge_map;1", n2);
    // results->ls();
    //n2->Write();
    TFile *outFile = TFile::Open(outputPath, "RECREATE");
    if (!outFile || outFile->IsZombie()) {
      std::cerr << "Error: Could not open output file for writing." << std::endl;
      // Clean up input file before returning
      
      outFile->Close();                                                                                                               return;                                                                                                                      }                                                                                                                                                                                                                                                             // Change the current directory to the output file so the object is written there
    outFile->cd();                                                                                                                 // Write the histogram to the output file
    n2->Write();                                                                                                                   // Close the output file. This is crucial to ensure data is saved correctly.
    outFile->Close();                                                                                                                                                                                                                                             std::cout << "Histogram saved to"<<outputPath << std::endl;                                                          }

}
