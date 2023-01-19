# SpheroScan

## Prerequisite. 
  - To install SpheroScan, you will need to have a compatible operating system (Mac, Linux, or Windows).  
  - Conda installed. You can follow the official Conda documentation (https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html) to install Conda. Once installed, run the command ```conda list``` in your terminal to test your installation. You could follow this tutorial to learn more about conda.

## Installation. 
  - #### Download sourcecode and model weights. 
    1. Download the SpheroScan GitHub repository from https://github.com/FunctionalUrology/SpheroScan.
    2. Download the model weights from the provided link ------ . Unzip and copy the model weights to the previously downloaded SpheroScan directory.
    
- #### Install dependencies.  
    1. Open your terminal and change the directory to the SpheroScan directory (e.g. ```cd path/to/SpheroScan/dir```). 
    2. Run following commands one by one:    
  
    ```
    conda create -n my_env                          #create a new Conda environment
    conda activate my_env                           #activate Conda environment
    conda install python=3.10.6                     #Install Python
    conda install -c conda-forge detectron2         #Install detectron2
    pip install -r requirements.txt                 #Install other dependencies for SpheroScan
    python main.py                                  #It will open a web window and launch SpheroScan
 
- #### Re-run SpheroScan
    1. Open your terminal and change the directory to the SpheroScan directory (e.g. ```cd path/to/SpheroScan/dir```). 
    2. Run following commands one by one:  
   
    ```
    conda activate my_env                           #activate Conda environment
    python main.py                                   #It will open a web window and launch SpheroScan
    ```


## Errors you may encountered. 
- ``` ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts. detectron2 0.6 requires black==21.4b2, which is not installed.```.  
  - Possible solution: You can simply ignore this error.
  
- ``` Address already in use
Port 4549 is in use by another program. Either identify and stop that program, or start the server with a different port.```.  
  - Possible solution: Before relaunching, please verify if you have a server already running for SpheroScan by checking your terminal and browser windows. If a server is already running, kindly close it.
