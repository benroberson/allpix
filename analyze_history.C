
R__ADD_INCLUDE_PATH(/cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/include/)
R__LOAD_LIBRARY(/cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/lib/libAllpixObjects.so)

#include "objects/PixelHit.hpp"
#include "objects/PixelCharge.hpp"
#include "objects/MCParticle.hpp"

void analyze_history() {
    // Open the output file
    TFile* file = new TFile("output/allpix_squared_outputs.root", "READ");
    TTree* tree = (TTree*)file->Get("PixelHit");

    // Link the branch
    std::vector<allpix::PixelHit*> hits;
    tree->SetBranchAddress("dut", &hits);

    for (int i = 0; i < tree->GetEntries(); ++i) {
        tree->GetEntry(i);
        for (auto& hit : hits) {
            std::cout << "--- New Hit Found ---" << std::endl;
            std::cout << "Final Hit: Pix (" << hit->getIndex().x() << "," << hit->getIndex().y() << ")" << std::endl;

            // 1. Trace back to PixelCharge (The digitization input)
            auto pixel_charges = hit->getPixelCharge();
            std::cout << "  Derived from " << pixel_charges->size() << " charge clusters." << std::endl;

            // 2. Trace back to MCParticles (The Truth information)
            auto mc_particles = hit->getMCParticles();
            for (auto& mc_p : mc_particles) {
                std::cout << "  Originating MC Particle PDG: " << mc_p->getParticleID() << std::endl;
                std::cout << "  Initial Energy: " << mc_p->getInitialKineticEnergy() << " MeV" << std::endl;
            }
        }
    }
}