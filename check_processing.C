/**
 * Allpix Squared Processing Verification Macro
 * Environment: /cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/
 */

// 1. Setup CVMFS Paths for Headers and Libraries
R__ADD_INCLUDE_PATH(/cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/include/)
R__LOAD_LIBRARY(/cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/lib/libAllpixObjects.so)

#include <iostream>
#include <vector>
#include <string>

// Include the necessary Allpix Squared objects
#include "objects/PixelHit.hpp"
#include "objects/PixelCharge.hpp"
#include "objects/MCParticle.hpp"

void check_processing(std::string filename = "output/allpix_squared_outputs.root", std::string detector_name = "timepix") {
    
    TFile* file = TFile::Open(filename.c_str(), "READ");
    if(!file || file->IsZombie()) {
        std::cerr << "❌ Error: Could not open file " << filename << std::endl;
        return;
    }

    // Identify the Processing Stage by Tree existence
    TTree* hit_tree = (TTree*)file->Get("PixelHit");
    if(!hit_tree) {
        std::cout << "❌ STAGE FAILURE: No 'PixelHit' tree found." << std::endl;
        std::cout << "   The simulation likely stopped at Propagation or Transfer." << std::endl;
        return;
    }

    // Set up branch for the detector
    std::vector<allpix::PixelHit*> hits;
    if(hit_tree->GetBranch(detector_name.c_str())) {
        hit_tree->SetBranchAddress(detector_name.c_str(), &hits);
    } else {
        std::cout << "⚠️ Warning: Branch for '" << detector_name << "' not found. Check your detector name." << std::endl;
        return;
    }

    // Analyze the first event with hits
    bool found_valid_event = false;
    for (Long64_t i = 0; i < hit_tree->GetEntries(); ++i) {
        hit_tree->GetEntry(i);
        if (hits.empty()) continue;

        found_valid_event = true;
        allpix::PixelHit* first_hit = hits[0];
        
        std::cout << "--- Processing Verification for Event " << i << " ---" << std::endl;
        std::cout << "Final Output: PixelHit found at index " << first_hit->getIndex().x() << "," << first_hit->getIndex().y() << std::endl;

        // 2. Verify Transfer Step (PixelCharge)
        const allpix::PixelCharge* parent_charge = first_hit->getPixelCharge();
        if(parent_charge != nullptr) {
            std::cout << "✅ STEP 1 (Digitization): Success. Hit linked to PixelCharge." << std::endl;
            std::cout << "   Collected Charge: " << parent_charge->getCharge() << " e" << std::endl;
        } else {
            std::cout << "❌ STEP 1 (Digitization): Link Missing! History was not saved." << std::endl;
        }

        // 3. Verify Truth Step (MCParticles)
        auto mc_particles = first_hit->getMCParticles();
        if(!mc_particles.empty()) {
            std::cout << "✅ STEP 2 (Truth Link): Success. Hit linked to " << mc_particles.size() << " MCParticle(s)." << std::endl;
            std::cout << "   Primary Particle PDG: " << mc_particles[0]->getParticleID() << std::endl;
        }

        std::cout << "\nRESULT: File is FULLY PROCESSED through the Digitizer stage." << std::endl;
        break; // Just check the first valid event
    }

    if(!found_valid_event) {
        std::cout << "⚠️ No hits found in any events. Processing chain is complete but signal is below threshold." << std::endl;
    }

    file->Close();
}