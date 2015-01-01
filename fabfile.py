from fabric.api import *
import urllib

# List of hosts to push to
# Run with env.hosts unchecked will do all four nodes sequentially. For now, we'll do them 
# individually.
# env.hosts = ['10.70.0.40', '10.70.0.43', '10.70.0.96', '10.70.0.95']

# The command to stop mod_jk doesn't currently work, so please go to 
# http://10.70.0.94/modjk.php?r=10
# and control it manually (solution is in progress)


def deploy_ROOT():

    # create target and temp dir 

    sudo("mkdir -p /var/opt/apps/<current_version>/ROOT")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/<sanitized>/fabric/ROOT.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /var/opt/apps/<current_version>/ROOT/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Yes it is!)
    
    with cd("/var/opt/apps/<current_version>/ROOT"):
        sudo("unzip /var/opt/apps/<current_version>/ROOT/ROOT.war")

    sudo("chown -R deploy:deploy /var/opt/apps/<current_version>")
    sudo("rm -f /var/opt/apps/<current_version>/ROOT/ROOT.war")
    
    # confirm/execute stopping mod_jk
    
    if confirm("Stop mod_jk now?", default=False):
    	# stop mod_jk (e.g., "web0 - <sanitized>_a")
    	# STP, "&wa=2&vwa=2"
    	urllib.urlopen("http://10.70.0.94/modjk.php?cmd=update&w=<sanitized>&sw=viddler_a&wf=300&wn=viddler_a&wr=&wc=&wd=0&vwn=viddler_a&vwr=&vwc=&vwd=0&wa=2&vwa=2")
    
    # confirm/execute stopping tomcats
    if confirm("Stop tomcat instance(s) now?", default=False):
    	# stop tomcat
    	sudo("service tomcat_1 stop")
    	sudo("service tomcat_2 stop")

    # clear catalina logs

    sudo("> /var/opt/tomcat_1/logs/catalina.out")
    sudo("> /var/opt/tomcat_2/logs/catalina.out")

    # switch link to new app

    sudo("rm -f /var/opt/tomcat_1/webapps/ROOT")
    sudo("ln -s /var/opt/apps/<current_version>ROOT /var/opt/tomcat_1/webapps/ROOT")

    sudo("rm -f /var/opt/tomcat_2/webapps/ROOT")
    sudo("ln -s /var/opt/apps/<current_version>/ROOT /var/opt/tomcat_2/webapps/ROOT")


    # confirm switch

    sudo("ls -l /var/opt/tomcat_1/webapps")
    sudo("ls -l /var/opt/tomcat_2/webapps")

    # start tomcat

    sudo("set -m; /etc/init.d/tomcat_1 start")
    sudo("set -m; /etc/init.d/tomcat_2 start")

    # start mod_jk (e.g., "web0 - <sanitized>_a")
    # ACT, "&wa=0&vwa=0"
    
    urllib.urlopen("http://10.70.0.94/modjk.php?cmd=update&w=<sanitized>&sw=viddler_a&wf=300&wn=viddler_a&wr=&wc=&wd=0&vwn=viddler_a&vwr=&vwc=&vwd=0&wa=0&vwa=0")


@hosts("root@10.70.0.40")
def deploy_admin():

    # First, we update ROOT

    sudo("mkdir -p /var/opt/apps/<current_version>/ROOT")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/<sanitized>/fabric/ROOT.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /var/opt/apps/<current_version>/ROOT/")
    sudo("rm -Rf /home/rsherman/tmp")
    
    # Expand war file (is this necessary? Yes it is!)
    
    with cd("/var/opt/apps/<current_version>/ROOT"):
        sudo("unzip /var/opt/apps/<current_version>/ROOT/ROOT.war")

    sudo("chown -R deploy:deploy /var/opt/apps/<current_version>")
    sudo("rm -f /var/opt/apps/<current_version>/ROOT/ROOT.war")
    
    # stop tomcat

    sudo("service tomcat_1 stop")

    # clear catalina logs

    sudo("> /var/opt/tomcat_1/logs/catalina.out")

    # switch link to new app

    sudo("rm -f /var/opt/tomcat_1/webapps/ROOT")
    sudo("ln -s /var/opt/apps/<current_version>ROOT /var/opt/tomcat_1/webapps/ROOT")


    # confirm switch

    sudo("ls -l /var/opt/tomcat_1/webapps")

    # start tomcat

    sudo("set -m; /etc/init.d/tomcat_1 start")
    

    # Now update admin

    sudo("mkdir -p /var/opt/apps/<current_version>/<sanitized>_admin")
    sudo("mkdir -p /home/rsherman/tmp/<current_version>")

    # push app to host - remember to update target dir version number
    
    sudo("chown -R rsherman:rsherman /home/rsherman")
    put("/Users/rsherman/<sanitized>/fabric/viddler_admin.war", "/home/rsherman/tmp/<current_version>/")
    sudo("mv /home/rsherman/tmp/<current_version>/* /var/opt/apps/<current_version>/<sanitized>_admin/")
    sudo("rm -Rf /home/rsherman/tmp")

    with cd("/var/opt/apps/<current_version>/<sanitized>_admin"):
        sudo("unzip /var/opt/apps/<current_version>/<sanitized>_admin/viddler_admin.war")

    sudo("chown -R deploy:deploy /var/opt/apps/<current_version>")
    sudo("rm -f /var/opt/apps/<current_version>/<sanitized>_admin/viddler_admin.war")
    sudo("service tomcat_2 stop")
    sudo("> /var/opt/tomcat_2/logs/catalina.out")
    sudo("rm -f /var/opt/tomcat_2/webapps/<sanitized>_admin")
    sudo("ln -s /var/opt/apps/<current_version>/<sanitized>_admin /var/opt/tomcat_2/webapps/viddler_admin")
    sudo("ls -l /var/opt/tomcat_2/webapps")
    sudo("set -m; /etc/init.d/tomcat_2 start")

    # Remember to stop mod_jk
    

def start_tomcat():
    sudo("set -m; /etc/init.d/tomcat_1 start")
    sudo("set -m; /etc/init.d/tomcat_2 start")

def stop_tomcat():
    sudo("service tomcat_1 stop")
    sudo("service tomcat_2 stop")

def test_mod_jk():
    urllib.urlopen("http://10.70.0.94/modjk.php?cmd=update&w=<sanitized>-search&sw=viddler-search_g&wf=100&wn=viddler_g&wr=&wc=&wd=0&vwn=viddler_g&vwr=&vwc=&vwd=0&wa=2&vwa=2")
