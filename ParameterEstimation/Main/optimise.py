__author__ = 'zwan145'

import os, sys
from passive_mechanics import *
from scipy.optimize import leastsq, fmin, fminbound, fmin_slsqp, fmin_l_bfgs_b
#from pykalman import UnscentedKalmanFilter
from scipy import array

from bc_setup import *
from results import *
from datetime import datetime
import time
import math

def optimise_passive_main(study_id, study_frame, pressure, node_idx, forward_solve_toggle):
    # This function estimates a bulk myocardial stiffness parameter (C1) by fitting LV model predictions to
    # subject-specific image-derived geometries.
    # 1. Initial forward solve, simulating inflation from DS to ED. The model predictions at each frame is saved in
    # ipinit format.
    # 2. Generate results text file after initial solve.
    # 3. Optimise C1 to minimise summed fitting error for all frames from DS to ED.
    # 4. Evaluate final optimised solution and fitting errors.
    ####################################################################################################################

    os.chdir(os.environ['STUDIES']+study_id+'/LVMechanics'+study_id+'/PassiveMechanics')

    ## 1. Initial forward solve, simulating inflation from DS to ED. The model predictions at each frame is saved in
    # ipinit format.
    if forward_solve_toggle == 1:
        # Initialise passive parameter
        material_create_ipmate(3.0, 'LV_CubicGuc_TEMPLATE.ipmate', 'LV_CubicGuc.ipmate')
        # Do initial solve
        passive_initial_solve(study_id, study_frame, pressure, node_idx)
        ## 2. Generate results files containing pressure, volume, endocardial and epicardial fitting errors at each frame
        # from DS+1 to ED.
        results_passive_generate(study_id, study_frame, 'ForwardSolve', 'ForwardSolve')

    ## 3. Optimise C1 to minimise summed fitting error for all frames from DS to ED.
    # Control bounds for C1 parameter.
    l_bound = 0.6
    u_bound = 20.0
    # Set initial guess for C1.
    C1_init = [3.0]
    # Copy over forward solve solutions to current warm solve solution folder.
    os.system('cp ForwardSolveSolution/*.* WarmStartSolution/.')
    # Use built-in python optimiser to estimate C1.
    C1_opt = fmin_l_bfgs_b(optimise_passive_obj_function, C1_init, approx_grad=1, bounds=[(l_bound, u_bound)],
                           epsilon=1e-2, args=[study_id, study_frame], factr=1e12)
    print C1_opt
    # Final solve using optimised C1 value.
    C1 = float(C1_opt[0][0])
    mse = optimise_passive_obj_function(C1, study_id, study_frame)

    results_passive_generate(study_id, study_frame, 'Optimised', 'Optimised')

    # Output to log file.
    print 'LOG: Final Optimised Passive Parameter: ' + str(C1)
    print 'LOG: With total MSE of '+str(mse)

#
#=======================================================================================================================
#

def optimise_passive_obj_function(C1, study_id, study_frame):
    # This function is the objective function which interfaces with the python optimiser for passive parameter
    # estimation. It updates the C1 parameter and evaluates the overall fitting error objective function at all frames
    # between DS to ED.
    # 1. Update current C1 estimate in ipmate file.
    # 2. Re-run simulation using current C1 estimate and get new model predictions for each frame from DS+1 to ED.
    # 3. Evaluate MSE of fitting and sum for all frames from DS+1 to ED.
    # 4. Generate results text files.
    ####################################################################################################################

    print 'LOG: Evaluating C1 = '+str(C1)+'\n'

    ## 1. Update current C1 estimate in ipmate file.
    copy('LV_CubicGuc.ipmate', 'LV_CubicGuc_previous.ipmate')
    material_create_ipmate(C1, 'LV_CubicGuc_TEMPLATE.ipmate', 'LV_CubicGuc.ipmate')

    ## 2. Re-run simulation using current C1 estimate and get new model predictions for each frame from DS+1 to ED.
    # Solve warm start using new C1 guess
    passive_warm_solve(study_id, 'ED', reg_toggle=1)

    ## 3. Evaluate MSE of fitting and sum for all frames from DS+1 to ED.
    toggle = 1  # Scalar objective value.
    mse = optimise_passive_obj_evaluate(['ED'], toggle)

    ## 4. Generate results text files containing pressure, volume, endocardial and epicardial fitting errors.
    results_name = datetime.now().strftime('%H:%M')
    results_passive_generate(study_id, study_frame, results_name, 'Optimised')

    print 'LOG: Finished updating solutions with current C1 = '+str(C1)
    return mse

#
#=======================================================================================================================
#

def optimise_passive_obj_evaluate(idx, toggle):
    # This function extracts the MSE of fitting for both endocardial and epicardial surfaces for all frames from DS+1 to
    # ED and sums them up.
    mse = []
    for i in range(0, len(idx)):
        # Vector error value
        info = open('OptimisedError/EpiError_'+str(idx[i])+'.opdata').read()
        array = re.split(r'[\n\\]', info)
        temp = array[3].split()
        num_epi = float(temp[len(temp)-1])
        temp = array[7].split()
        epi_rmse = float(temp[len(temp)-1])
        print epi_rmse

        info = open('OptimisedError/EndoError_'+str(idx[i])+'.opdata').read()
        array = re.split(r'[\n\\]', info)
        temp = array[3].split()
        num_endo = float(temp[len(temp)-1])
        temp = array[7].split()
        endo_rmse = float(temp[len(temp)-1])
        print endo_rmse
        mse.append((epi_rmse**2*num_epi + endo_rmse**2*num_endo)/(num_endo+num_epi))
        print mse
        print '\033[0;30;45m LOG: Current MSE for ED = '+str(mse[i])+'\033[0m\n'

    if toggle == 1:
        mse_tot = 0
        mse_tot = mse[0]
        print 'LOG: Current total MSE for diastole = '+str(mse_tot)+'\n'
        return mse_tot
    elif toggle == 2:
        mse = array(mse)
        return mse
#
