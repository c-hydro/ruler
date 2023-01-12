#!/bin/bash -e

# ----------------------------------------------------------------------------------------
# Script information
script_name='RULER - APP - HMC WRAPPER'
script_version='1.0.0'
script_date='2022/12/27'

# Argument(s) default definition(s)
file_app_main='ruler_main.py'
file_app_configuration='ruler_configuration_hmc_wrapper.json'

# Virtualenv default definition(s)
virtualenv_folder='/home/gabellani/DTE-EVO/library/fp_system_env_conda/'
virtualenv_name='fp_system_conda_python3_hmc_libraries'
                 
# Default script folder
script_folder='/home/gabellani/DTE-EVO/library/fp_package_ruler/'
configuration_folder='/home/gabellani/DTE-EVO/utils/'
package_folder='/home/gabellani/DTE-EVO/library/fp_package_ruler/'

# Get information (-u to get gmt time)
time_app=$(date -u +"%Y-%m-%d %H:00")
#time_app='2020-12-21 13:21' # DEBUG 
#-----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Activate virtualenv
echo " ===> SET APP ENVIRONMENTAL LIBRARIES ... "
export PATH=$virtualenv_folder/bin:$PATH
source activate $virtualenv_name

# Add path to pythonpath script and package folder(s)
export PYTHONPATH="${PYTHONPATH}:$script_folder"
export PYTHONPATH="${PYTHONPATH}:$package_folder"

echo " ===> SET APP ENVIRONMENTAL LIBRARIES ... DONE"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Define app option(s)
path_app_main=$script_folder/$file_app_main
path_app_configuration=$configuration_folder/$file_app_configuration

echo " ===> SET APP SETTINGS ... "
echo " ====> App main: ${path_app_main} "
echo " ====> App configuration: ${path_app_configuration} "
echo " ====> App time: ${time_app} "
echo " ===> SET APP SETTINGS ... DONE"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Check entrypoint option(s) 
echo " ===> CHECK APP ... "
echo " ====> Check app main [$path_app_main] ... "
if [ -f $path_app_main ] ; then
	echo " ====> Check app main ... DONE"
else
	echo " ====> Check app main ... FAILED. FILE DOES NOT EXIST" 
	exit 1
fi
echo " ====> Check app configuration [$path_app_configuration] ... "
if [ -f $path_app_configuration ] ; then
	echo " ====> Check app configuration ... OK"
else
	echo " ====> Check app configuration ... FAILED. FILE DOES NOT EXIST" 
	exit 2
fi
echo " ===> CHECK APP ... DONE"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Execute app
echo " ===> EXECUTE APP ... "
echo " ====> Command Line: python $path_app_main -settings_file $path_app_configuration -time $time_app"

# Run command-line
python $path_app_main -settings_file $path_app_configuration -time "$time_app"

echo " ===> EXECUTE APP ... DONE"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------
