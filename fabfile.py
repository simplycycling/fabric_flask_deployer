# fabric deployment script
# Written by Roger Sherman and Perry Boyko

from fabric.api import *
from fabric.contrib.console import confirm
import os
import urllib
from fabric.colors import green, cyan

# List of hosts to push to 
# Run with env.hosts unchecked will do all four nodes sequentially. For now, we'll do them 
# individually.
# env.hosts = ['10.20.0.x', '10.20.0.x', '10.20.0.x', '10.20.0.x']

@hosts('10.70.x.x')
def deploy_api0():

    # create target and temp dir 
    sudo("mkdir -p /path/to/apps/<current_version>/MAIN_APP")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number    
    sudo("chown -R rsherman:rsherman /home/rsherman")
    # TODO:  Replace the next 'put()' with a system `scp` command instead for upload progress.
    #os.system("scp " + srcfile + " " + destination)
    put("/Users/rsherman/viddler/fabric/MAIN_APP.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /path/to/apps/<current_version>/MAIN_APP/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Not in all environments) set permissions, and clean up user home dir
    with cd("/path/to/apps/<current_version>/MAIN_APP"):
        sudo("unzip /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    sudo("chown -R deploy:deploy /path/to/apps/<current_version>")
    sudo("rm -f /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    
    # confirm/execute stopping mod_jk    
    if confirm("Stop mod_jk now?", default=False):
    	# stop mod_jk (e.g., "web0 - viddler_a")
    	# STP, "&wa=2&vwa=2"
        urllib.urlopen("http://_generic_REST_command_")
        urllib.urlopen("http://_generic_REST_command_")
    
    # confirm/execute stopping tomcats
    if confirm("Stop tomcat instance(s) now?", default=False):
    	# stop tomcat
    	sudo("service tomcat_1 stop")
    	sudo("service tomcat_2 stop")

    # clear catalina logs
    sudo("> /path/to/tomcat_1/logs/catalina.out")
    sudo("> /path/to/tomcat_2/logs/catalina.out")

    # switch link to new app
    sudo("rm -f /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("rm -f /path/to/tomcat_2/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_2/webapps/MAIN_APP")


    # confirm switch
    sudo("ls -l /path/to/tomcat_1/webapps")
    sudo("ls -l /path/to/tomcat_2/webapps")
    if confirm("Has the app been switched to the proper version? If so, start tomcat.", default=False):
        # start tomcat
        sudo("set -m; /etc/init.d/tomcat_1 start")
        sudo("set -m; /etc/init.d/tomcat_2 start")

    # start mod_jk (e.g., "web0 - viddler_a")
    # ACT, "&wa=0&vwa=0"    
    urllib.urlopen("http://_generic_REST_command_")
    urllib.urlopen("http://_generic_REST_command_")
    print(green("Thank you for the new package, sir!"))

@hosts('10.70.x.x')
def deploy_api1():

    # create target and temp dir 
    sudo("mkdir -p /path/to/apps/<current_version>/MAIN_APP")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/viddler/fabric/MAIN_APP.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /path/to/apps/<current_version>/MAIN_APP/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Not in all environments)
    with cd("/path/to/apps/<current_version>/MAIN_APP"):
        sudo("unzip /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    sudo("chown -R deploy:deploy /path/to/apps/<current_version>")
    sudo("rm -f /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    
    # confirm/execute stopping mod_jk
    if confirm("Stop mod_jk now?", default=False):
        # stop mod_jk (e.g., "web0 - viddler_a")
        # STP, "&wa=2&vwa=2"
        urllib.urlopen("http://_generic_REST_command_")
        urllib.urlopen("http://_generic_REST_command_")
    
    # confirm/execute stopping tomcats
    if confirm("Stop tomcat instance(s) now?", default=False):
        # stop tomcat
        sudo("service tomcat_1 stop")
        sudo("service tomcat_2 stop")

    # clear catalina logs
    sudo("> /path/to/tomcat_1/logs/catalina.out")
    sudo("> /path/to/tomcat_2/logs/catalina.out")

    # switch link to new app
    sudo("rm -f /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("rm -f /path/to/tomcat_2/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_2/webapps/MAIN_APP")


    # confirm switch
    sudo("ls -l /path/to/tomcat_1/webapps")
    sudo("ls -l /path/to/tomcat_2/webapps")
    if confirm("Has the app been switched to the proper version? If so, start tomcat.", default=False):
        # start tomcat
        sudo("set -m; /etc/init.d/tomcat_1 start")
        sudo("set -m; /etc/init.d/tomcat_2 start")

    # start mod_jk (e.g., "web0 - viddler_a")
    # ACT, "&wa=0&vwa=0"
    urllib.urlopen("http://_generic_REST_command_")
    urllib.urlopen("http://_generic_REST_command_")

@hosts('10.70.0.43')
def deploy_web0():

    # create target and temp dir 
    sudo("mkdir -p /path/to/apps/<current_version>/MAIN_APP")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/viddler/fabric/MAIN_APP.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /path/to/apps/<current_version>/MAIN_APP/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Not in all environments)
    with cd("/path/to/apps/<current_version>/MAIN_APP"):
        sudo("unzip /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    sudo("chown -R deploy:deploy /path/to/apps/<current_version>")
    sudo("rm -f /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    
    # confirm/execute stopping mod_jk
    if confirm("Stop mod_jk now?", default=False):
        # stop mod_jk (e.g., "web0 - viddler_a")
        # STP, "&wa=2&vwa=2"
        urllib.urlopen("http://_generic_REST_command_")
        urllib.urlopen("http://_generic_REST_command_")
    
    # confirm/execute stopping tomcats
    if confirm("Stop tomcat instance(s) now?", default=False):
        # stop tomcat
        sudo("service tomcat_1 stop")
        sudo("service tomcat_2 stop")

    # clear catalina logs
    sudo("> /path/to/tomcat_1/logs/catalina.out")
    sudo("> /path/to/tomcat_2/logs/catalina.out")

    # switch link to new app
    sudo("rm -f /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("rm -f /path/to/tomcat_2/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_2/webapps/MAIN_APP")

    # confirm switch
    sudo("ls -l /path/to/tomcat_1/webapps")
    sudo("ls -l /path/to/tomcat_2/webapps")
    if confirm("Has the app been switched to the proper version? If so, start tomcat.", default=False):
        # start tomcat
        sudo("set -m; /etc/init.d/tomcat_1 start")
        sudo("set -m; /etc/init.d/tomcat_2 start")

    # start mod_jk (e.g., "web0 - viddler_a")
    # ACT, "&wa=0&vwa=0"
    urllib.urlopen("http://_generic_REST_command_")
    urllib.urlopen("http://_generic_REST_command_")

@hosts("10.70.0.40")
def deploy_web3():

    # First, we update MAIN_APP
    sudo("mkdir -p /path/to/apps/<current_version>/MAIN_APP")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/viddler/fabric/MAIN_APP.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /path/to/apps/<current_version>/MAIN_APP/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Not in all environments)
    with cd("/path/to/apps/<current_version>/MAIN_APP"):
        sudo("unzip /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")
    sudo("chown -R deploy:deploy /path/to/apps/<current_version>")
    sudo("rm -f /path/to/apps/<current_version>/MAIN_APP/MAIN_APP.war")

    # Stop mod_jk
    if confirm("Stop mod_jk now?", default=False):
        urllib.urlopen("http://_generic_REST_command_")
        urllib.urlopen("http://_generic_REST_command_")
    
    # stop tomcat
    if confirm("Stop tomcat instance(s) now?", default=False):
        sudo("service tomcat_1 stop")

    # clear catalina logs
    sudo("> /path/to/tomcat_1/logs/catalina.out")

    # switch link to new app
    sudo("rm -f /path/to/tomcat_1/webapps/MAIN_APP")
    sudo("ln -s /path/to/apps/<current_version>/MAIN_APP /path/to/tomcat_1/webapps/MAIN_APP")


    # confirm switch
    sudo("ls -l /path/to/tomcat_1/webapps")

    # Now update admin
    sudo("mkdir -p /path/to/apps/<current_version>/secondary_app")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/viddler/fabric/secondary_app.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /path/to/apps/<current_version>/secondary_app/")
    sudo("rm -Rf /home/rsherman/tmp")
    with cd("/path/to/apps/<current_version>/secondary_app"):
        sudo("unzip /path/to/apps/<current_version>/secondary_app/secondary_app.war")
    sudo("chown -R deploy:deploy /path/to/apps/<current_version>")
    sudo("rm -f /path/to/apps/<current_version>/secondary_app/secondary_app.war")
    if confirm("Stop tomcat instance(s) now?", default=False):
        sudo("service tomcat_2 stop")
    sudo("> /path/to/tomcat_2/logs/catalina.out")
    sudo("rm -f /path/to/tomcat_2/webapps/secondary_app")
    sudo("ln -s /path/to/apps/<current_version>/secondary_app /path/to/tomcat_2/webapps/secondary_app")
    sudo("ls -l /path/to/tomcat_2/webapps")
    # confirm switch
    sudo("ls -l /path/to/tomcat_1/webapps")
    sudo("ls -l /path/to/tomcat_2/webapps")
    if confirm("Has the app been switched to the proper version? If so, start tomcat.", default=False):
        sudo("set -m; /etc/init.d/tomcat_1 start")
        sudo("set -m; /etc/init.d/tomcat_2 start")

    # Start mod_jk
    urllib.urlopen("http://_generic_REST_command_")
    urllib.urlopen("http://_generic_REST_command_")

    
def start_tomcat():
    sudo("set -m; /etc/init.d/tomcat_1 start")
    sudo("set -m; /etc/init.d/tomcat_2 start")

def stop_tomcat():
    sudo("service tomcat_1 stop")
    sudo("service tomcat_2 stop")

