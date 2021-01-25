# pypsa-in-prime

# Running PyPSA-Eur-Sec in PRIME

This repository includes instructions and tricks to run PyPSA-Eur-Sec in the cluster PRIME.

Its main purpose is to help master and PhD students install the packages and run the simulations. 

If you encounter a problem (and hopefully also a solution). Please, edit this README file with the solution so that other students can also benefit.

***GENERAL INSTRUCTIONS FOR PYPSA-EUR-SEC***

PyPSA-Eur-Sec allows the optimization of the sector-coupled European energy system and includes as a subpackage PyPSA-Eur (which includes only the power sector). PyPSA-Eur can be run independently or it can be called from PyPSA-Eur-Sec by selecting in the configuration file
only the power sector. Technology-Data is a repository including costs, efficiencies, lifetimes, etc for different technologies.

There is a [distribution list](https://groups.google.com/g/pypsa) where PyPSA-related problems (and solutions) are discussed.

There is also documentation for [PyPSA](https://pypsa.readthedocs.io/en/latest/), [PyPSA-Eur](https://pypsa-eur.readthedocs.io/en/latest/) and [PyPSA-Eur-Sec](https://pypsa-eur-sec.readthedocs.io/en/latest/)

This repository does not substitute any of the previous information and it only focuses on issues related to running PyPSA-Eur-Sec in PRIME.

NOTE: In order to set up anaconda, python, and pypsa, [these instructions](https://github.com/martavp/RES_project/blob/master/Instructions_RES_project.pdf) and the [tutorial for the course project in RES](https://github.com/martavp/RES_project/blob/master/RES_project.ipynb) could be useful. 

This [video](https://www.youtube.com/watch?v=ty47YU1_eeQ) provides a nice introduction to PyPSA-Eur. 



### USING SNAKEMAKE IN THE CLUSTER ###

1. Tu use the [PRIME cluster](https://mpe.au.dk/en/research/facilities/prime/), first you need to get a user. 

2. You can connect to the cluster through the terminal, e.g.
> ssh marta@prime.eng.au.dk

3. Some useful commands to use in the cluster are described in the [labbook](https://labbook.au.dk/display/COM/3.+Convenient+commands)

4. If you are using Windows, [WinSCP](https://winscp.net/eng/download.php) can be useful to copy folders to/from the cluster

5. To connect to the cluster you need to be connected to the university network, so if you are at home you need to use the VPN

6. You will need to have installed anaconda/miniconda in your home directory at the cluster

7. You can install PyPSA-Eur-Sec following the [instructions](https://pypsa-eur-sec.readthedocs.io/en/latest/installation.html) 

8. You will need to have an environment with all the necessary packages, including [snakemake](https://snakemake.readthedocs.io/en/stable/)
which is a very useful way of dealing with parallelized jobs in the cluster. One easy way to install all the packages that you need is to create
the environment using the 'environment.yaml' file provided in pypsa-eur

> .../pypsa-eur % conda env create -f envs/environment.yaml

> .../pypsa-eur % conda activate pypsa-eur


9. Install gurobi in the environment
> conda isntall -c gurobi gurobi

10. In the folder '/PRIME_cluster' of this repository, there are two additional files needed to use snakemake in the PRIME. 

Copy the files 'cluster.yaml' and 'snakemake_cluster' to the directory '.../pypsa-eur-sec/'  in your folders in the cluster

Then, to run snakemake, you only need to write the following instruction in the command line (jobs identify the number of jobs that you want to parallelize if you send more that one job simultaneously). 

> ./snakemake_cluster --jobs 5

11. It is possible that you need to give rights to snakemake_cluster, you can do it typing in the terminal.

> chmod u+x snakemake_cluster

12. Create a directory 'logs/cluster", as indicated in the file 'cluster.yaml'. This is where the logs and error files will be saved.

13. Check that the variable names in 'snakemake_cluster' comply with the variable names in your Snakefile. In particular, check that the memory attribution 
(mem_mb) is the same in both files or correct if necessary. 


14. Setting up Gurobi in the cluster  

On the PRIME-cluster, Gurobi needs to be pointed in the right direction as to where to look for packages and licenses. The first step is to add the following lines to the end of the file '.bashrc' located in /home/(AU-ID), as indicated in the [Gurobi guide](https://www.gurobi.com/documentation/6.5/quickstart_linux/software_installation_guid.html):

> export GUROBI_HOME="/home/com/meenergy/gurobi651/linux64"

> export PATH="${PATH}:${GUROBI_HOME}/bin"

> export LD_LIBRARY_PATH="${GUROBI_HOME}/lib"

Additionally, the following line should be added at the end of the file '.bashrc':

> export GRB_LICENSE_FILE="$GUROBI_HOME/gurobi.lic"

This points Gurobi to the cluster-license. Note that an academic license used locally on a computer is unsuitable for use on the cluster, and will result in a failed simulation.


15. Solution to "Solver (gurobi) returned non-zero return code (127)"
A change needs to be made to the file 'gurobi.sh' located in /home/(AU-ID)/anaconda3/envs/(pypsa-eur_environment_name)/bin/gurobi.sh . The last line of this shell script needs to point to 'python2.7', 
regardless of what Python version is used in the pypsa-eur environment in your local folder. Thus, the last line of 'gurobi.sh' needs to be:
 
> $PYTHONHOME/bin/python2.7 "$@"

Make sure to restart the terminal for these modifications to take effect.


16. Solution to "memory error". 
The config file should include a path to a folder where the temporal files during the solving of the network are saved.

> tmpdir: "/home/marta/tmp"

If this path is not specified, the [default is to use the directory where the script is being executed]
(https://github.com/PyPSA/pypsa-eur/blob/2e70e8d15b722e818efb57cf72b35a9536340365/scripts/solve_network.py#L281) which can cause errors due to not enough space in PRIME.  


17. Solution to "memory error".

Indicate that temporary files for the solver must the saved in the temporary directory specified in the config file by changing the script 'solve_network.py' and including the attribute
> n.lopf(pyomo=False, solver_name=solver_name, solver_dir=tmpdir,

18. I (Marta) have manually increased the resources in rule build_renewable_profiles to speed up that rule in the cluster.

> resources: mem=ATLITE_NPROCESSES * 50000

19. If you are using pypsa-eur independently of pypsa-eur-sec, to make sure that pypsa-eur gets to the final networks (with the solution), a rule all needs to be added to the Snakefile. 
In practice, this means adding the following text: 

>rule all:

>    input:
    
>        expand("results/networks/elec_s_{simpl}_{clusters}_ec_l{ll}_{opts}.nc",
>                **config['scenario'])


20. Terminal multiplexer (optional, but useful)  
ATTENTION: The execution of the workflow in a tmux-window defined in the Snakefile may result in the 'solve_network' rule to fail. This is different from system to system, but if it occurs, it can be solved by executing the rule 'solve_network' outside tmux.  
When

> ./snakemake_cluster --jobs 1

is executed in the cluster, the workflow in the 'Snakefile' starts. The DAG of jobs will be built, and depending on how many jobs have been allowed to run in parallel with the execution command above, one or more jobs will be submitted to the cluster with their own unique job-ID. If one chooses to close the terminal window in which the cluster is accessed, only the submitted jobs will be executed. For example if the rule 'cluster_network' is the last job to be submitted, this job will finish, but the subsequent rules will not. Because of this, one must wait until the final rule, 'solve_network', has been submitted if one wants to for instance log off the cluster.  
A solution for this, that allows for inputting the executing command and immediately logging off the cluster, is a terminal multiplexer called 'tmux'. This allows for having multiple windows in the same terminal window. To install it, make sure to have an Anaconda environment active in the cluster terminal window, and execute the following:

> conda install -c conda-forge tmux

Next, a new tmux-session can be created by executing:

> tmux new -s type_session_name_here

In this session, 'snakemake_cluster' can then be executed. When the workflow is running, the tmux-session can then be detached from, i.e. return to the normal PRIME-cluster window, by typing 'Ctrl+B', to get the attention of tmux, relatively quickly followed by typing 'd'. To reattach, execute the following in the terminal:

> tmux a -t type_session_name_here

If one has forgotten the name of the session when trying to reattach, simply execute:

> tmux

To get a list of the created sessions. The tmux commands described here, as well as many other neat ones, can be found  in this [article](https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/).
