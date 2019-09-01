Set up Environment
Install GIT
Install vagrant and VirtualBox
Fork this directory and copy the newly forked repository path with clone 

Terminal: bash-3.2$ git clone (Paste repo link here) fullstack
Download the following: 
application.py
database_populate.py
database_setup.py
static
templates

Copy files to the fullstack/catalog directory

Start the Program
In the terminal change directory to cloned fullstack directory

bash-3.2$ cd FULL_PATH_TO_NEWLY_CLONED_DIRECTORY

bash-3.2$ ls
CODEOWNERS    README.md     vagrant
bash-3.2$ cd vagrant/catalog

Launch the VM

bash-3.2$ vagrant up
Log in VM

bash-3.2$ vagrant ssh
vagrant@vagrant:~$

Change directory to the correct folder
vagrant@vagrant:~$ cd ../../vagrant/catalog

Install external python library
vagrant@vagrant:~$ sudo pip install flask_oauth

Setup & populate database
vagrant@vagrant:~$ python database_setup.py
vagrant@vagrant:~$ python database_populate.py

Run the program
vagrant@vagrant:~$ python application.py