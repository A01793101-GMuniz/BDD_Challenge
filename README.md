# BDD_Challenge
BDD-Selenium Framework

This is a project for Behavior Driven Development which needs some pre-installed pre-requisites to be run on your environment:


  	1.- Install behave module (pip install behave)
	2.- Install selenium module (pip install selenium)
	3.- Install Gherkin plugin for pycharm to improve editing of .feature file
	4.- Install allure package in python (pip install allure-behave)
  	5.- In case of wanting an html report generated: Install allure-commandline (provided under venv folder as zip) 
  
  
Once the pre-requisites are met user can run Framework by:


  1.- Running behave command on command line:
        Under project root folder run: behave \PATH\TO\FEATURES_FOLDER\<feature_file_to_run.feature> -D browser=<Firefox|Chrome|Edge|Safari>
            ** Safari browser was not tested as no MAC computer available
	    
  
  2.- Running run_behave.py file which is located on "<PROJECT_PATH>\Features\Common\bin\run_behave.py"
        This file will display a small and simple UI prompting the user to select the feature file and a browser, 
        Once user clicks start button the feature will start to run.
	

To generate allure report file run below command
	*	allure serve <PATH_TO_PROJECT>\Reports\results
