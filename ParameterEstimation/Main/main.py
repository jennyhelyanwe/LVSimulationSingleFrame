__author__ = 'zwan145'

import os
import sys
from setup import *
from geom_setup import *
from bc_setup import *
from mech_setup import *
from optimise import *


def main_program(study_id, study_frame, debug_toggle, forward_solve_toggle, a_p_toggle):
    # This function does the following:
    # 1. Program set-up: - set up directories for current study
    #                    - set up log text file if needed.
    # 2. Geometric set-up: - set up reference model and cavity models of LV.
    #                      - transfer reference, cavity models and DS, ED and ES surface data files to study folder.
    # 3. Mechanics simulation set-up: - get pressure array
    #                                 - get data index for prescribing basal displacement boundary conditions.
    #                                 - transfer mechanical simulation template files into study folder.
    # 4. Run estimation: - passive parameter estimation
    #                    - active parameter estimation.
    ####################################################################################################################

    ## 1. Program set-up:
    # Set up directories for current study.
    setup_dir(study_id)

    # Set up log text file if needed.
    if debug_toggle == 1:
        if a_p_toggle == 1:
            # Set up log file
            setup_log_file(study_id, 'Output_Passive.log')
        elif a_p_toggle == 2:
            setup_log_file(study_id, 'Output_Active.log')
        else:
            setup_log_file(study_id, 'Output_P_A.log')

    ## 2. Geometric set-up:
    # Set up reference model and cavity model of LV.
    geom_setup_ref_cavity(study_id, study_frame)

    # Initialise mechanics problem with reference model and endpoint surface data.
    geom_setup_data(study_id, study_frame)

    ## 3. Mechanics simulation set-up:
    # Get pressure array.
    pressure = bc_pressure_get(study_id, study_frame)

    # Get data indices for applying BC.
    data_idx = bc_displacement_get(study_id)

    # Transfer mechanics template files into study folder.
    mech_template_setup(study_id)

    optimise_passive_main(study_id, study_frame, pressure, data_idx, forward_solve_toggle)

def main():
    # Main commands begin here.
    os.system('rm *.*~')  # Remove all temporary files in Main folder.

    # Top level control of the entire simulation:
    # Command line inputs:
    idx = int(sys.argv[1])  # Study number
    debug_toggle = int(sys.argv[2])  # Debug toggle: 1 - write output to text file Output.log, 0 - write output to terminal.
    forward_toggle = int(sys.argv[3])  # Forward solve toggle: 1 - do passive initial solve, 0 - don't do it.
    a_p_toggle = int(sys.argv[4])  # Run: 1. Passive only, 2. Active only, 3. Passive & active.

    # Extract the important frame numbers for all studies
    [study_id, study_frame] = setup_get_frames(idx)

    # Output to screen
    print ''
    print '********************************************************'
    print '          Analysing study ' + study_id
    print '********************************************************'
    print ''

    # Run main program.
    main_program(study_id, study_frame, debug_toggle, forward_toggle, a_p_toggle)

if __name__ == '__main__':
    main()
