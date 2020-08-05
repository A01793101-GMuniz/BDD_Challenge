# BDD_Challenge
BDD-Selenium Framework

This is a project for Behavior Driven Development which needs some pre-installed pre-requisites to be run on your environment:


  	A) Install necessary packages by running command: pip install -r requirements.txt
  	B) You need to have WebDriver on PATH already configured or modified the path in Features\environment.py and add the Path to the file in your computer
		Driver for Mozilla, Chrome and Edge are provided on ROOT_FOLDER\bin\
	B) In case of wanting an html report generated: Install allure-commandline (provided under venv folder as zip) 
  
  
Once the pre-requisites are met user can run Framework by:


  1.- Running behave command on command line under project root folder run: 
  
  	behave \PATH\TO\FEATURES_FOLDER\<feature_file_to_run.feature> -D browser=<Firefox|Chrome|Edge|Safari>
        ** Safari browser was not tested as no MAC computer available
	    
  
  2.- Running run_behave.py file which is located on:
  
  	"<PROJECT_PATH>\Features\Common\bin\run_behave.py"
        This file will display a small and simple UI prompting the user to select the feature file and a browser, 
        Once user clicks start button the feature will start to run.
	

To generate allure report file run below command

	A)	allure serve <PATH_TO_PROJECT>\Reports\results
