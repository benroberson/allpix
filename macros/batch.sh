#!/bin/bash
#Note: must run within macros folder!
source /cvmfs/clicdp.cern.ch/software/allpix-squared/3.2.0/x86_64-el9-gcc12-opt/setup.sh

mkdir -p charge_maps
mkdir -p hits_txt
mkdir -p hits_txt_long
mkdir -p plots          

# Loop from 1 to 10
for i in {1..1}
do
    # Clean up simulation output
    rm -rf /afs/cern.ch/user/b/broberso/pixelsim/cmsp1/output/

    echo "--- Starting Iteration: $i ---"
    allpix -c neuro.conf
    
    # Run the first macro to save the TH2D to a ROOT file
    root -l -b -q "save_histogram.C(\"/afs/cern.ch/user/b/broberso/pixelsim/cmsp1/output/modules.root\",\"charge_maps/charge_map_$i.root\")"
    
    # --- NEW: Run the image extraction macro ---
    # This takes the root file we just made and exports it to a PNG
    root -l -b -q "extract_images.C(\"charge_maps/charge_map_$i.root\",\"plots/charge_map_$i.png\")"
    
    # Copy the text output from simulation (TextWriter module now saves directly)
    cp /afs/cern.ch/user/b/broberso/pixelsim/cmsp1/output/pixel_charges.txt hits_txt_long/hits_$i.txt

    # Run the second macro to convert to text format
    root -l -b -q "hist_data.C(\"charge_maps/charge_map_$i.root\",\"hits_txt/hits_$i.txt\")"

    echo "--- Iteration $i Finished ---"
    echo ""
done
