# cv-wifi-GT

## MESA-based SEIR Model

The original simulation framwork is borrowed from [Covid-19 Infection Model](https://github.com/metalcorebear/COVID-Agent-Based-Model) written by @metalcorebear.

The model is derived from the SEIR compartmental framework. Agents transits between the following states:
- Susceptible
- Exposed
- Asymptomatic
- Symptomatic
- Isolated
- Recovered
- Dead

Please refer to Agent-based Model&Simulation in the supplementary part of our paper [WiFi mobility models for COVID-19 enable less burdensome and more localized interventions for university
campuses](https://www.medrxiv.org/content/10.1101/2021.03.16.21253662v1.full.pdf) for all the definitions of our model dynamics and parameters (Table S2).

## Main files to run the model and reproduce the results in the paper

To protect the Georgia Tech commuity's privacy, we do not release the mobility networks to the followers of this paper. To run our simulation model, you must have your own 
mobility networks stored as pickle files for each day.

#### Data Processing files

- './calibration/usr_collection.py': file for collecting the population IDs list for every simulation.
- './calibration/data_shaping.py': file for attaching the network files based on the simulation category.

#### Model files

- './mesa_SIR/SEIR.py': file that contains functions for initialization and tranisitions between states.
- './calibration/agent.py'： file that create agents with all state state variables defined.
- './calibration/cal_model_t.py': file that defines the agent-based model by a class structure which inherits all functions and agents based on the above files. The class structure has 
three properties: (1) update the underline contact networks by days (2) update the state varibles for all agents by days (3) update the external infection rates based on 
the surrounding county's data by day, and (4) calculate all output metrics.
- './calibration/calibration_RMSE_t.py': file that runs the simulations of t days multiple times (15 by default) and store the result into a pickle file.
- './calibration/run_simulation.py': file that receives model parameters from the command line options to run the entire simulation pipeline

### Calibration

- './calibration/nelder_mead.py': file that define the rmse objective for calibrating the model to the ground truth by running the numerical algorithm, Nelder Mead. 
- './calibration/Nelder_mead_method.ipynb': the jupyter notebook for training the model.

## Example
For the non-intervention simulation for fall 2019 in Georgia Tech, from 2019/08/19 (yyyy/mm/dd) to 2020/12/21, please run the command
`python3 ./calibration/run_simulation.py -cat all -sp 7 -s 2019-08-19 -epoch 15 -days 118 -p 0.0293013 -y 0.01191042 -x  0.03175983`  
