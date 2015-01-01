This is a deployment system that leverages fabric and flask.

Currently, the fabfile.py is usable from the command line. To use, install fabric via pip:

pip install fabric

Modify the script to reflect the file paths that you'll need to use. Then invoke the class that reflects the action you want to perform:

fab deploy_api0

Currently, a flask frontend is being worked on that will allow you to enter the software version number that you're going to push. 

In the not too distant future, the ability to push from git (rather than local) will be added.
