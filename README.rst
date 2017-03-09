Budgeting App!

This is a simple budgeting web app using bank credentials (chase, bank of america, wells fargo, citi, american express)

To set up the environment, let's first create a virtual environment in Python3:
Run the command 

``virtualenv _env35 --python=python3``

Then run ``source ./bin/activate`` to activate your environment

Change into the `_env35` directory and clone this repo ``git clone <git_url>``

After cloning, run ``pip install -e .``

The config files are not added to this info, so you will not be able to serve the webpage until you create them or I send them to you. After obtaining the configuration file, you can serve the webapp by calling ``pserve <config_file_name>``	