# Verify Performance Scripts
Scripts for running the RP report

## Setup 

### Prerequisites

1. **Python 3** (3.6 or higher)

    There are a few different ways to install Python if it is not already installed:
    1. Using brew: `brew install python3`
    2. Using pyenv to manage multiple versions of Python on the same machine, or install a specific Python version:
        ```bash
        brew install pyenv
        eval "$(pyenv init -)"  # note this should go in your .bash_profile
        pyenv install 3.6.6
        pyenv global 3.6.6
        ```

1. **pre-commit** - for installing hooks that run final checks before allowing push to repositories
    ```bash
    brew install pre-commit
    ```

1. Clone the [verify-data-pipeline-config](https://github.com/alphagov/verify-data-pipeline-config) repo locally and [create a data directory](https://github.com/alphagov/verify-data-pipeline-config#the-data-folder) inside it.

1. **Setup AWS profile**
    Steps 1 to 5 in the [verify-event-infrastructure](https://github.com/alphagov/verify-event-infrastructure) repo README has good instructions on how to set up your AWS profile. It has also has instructions on how to assume and AWS admin role which is compatible with using Yubikeys for MFA.

### Installation
From the project root directory, run the following in terminal:
```
make requirements-dev
```
    
This will create a Python virtual environment (sometimes referred to as Virtualenv or venv) and install all the required dependencies into it.
    
## Using the Python Virtual Environment 
We are using an isolated Python environment to allow modules, dependencies, etc. used by this project to not affect another. 

In order to run scripts included in the project, run the following command to activate the virtual environment:

```
source ./verify-performance-scripts-venv/bin/activate
```

To exit or deactivate the virtual environment (e.g. in case you need to activate another project's virtual environment), run the following command:
```
deactivate
```

## Running tests
Running automated tests is a quick way to ensure that the code is in a good and reliable state, especially when you pull changes from upstream repository, change Python version, or install dependencies. 

The tests can be run by executing `make test`. Any test failing will indicate that there is likely a problem with the code or your local setup.

## Generating RP reports
RP reports can be generated by running the following command from inside the virtualenv:
```bash
export AWS_PROFILE=<aws-profile-name>  # No need to do this if you already have it set in a .env file
bin/generate_rp_report.py --report_start_date yyyy-mm-dd
```
To run the reports weekly, activate the virtual env then:
'''
bin/generate_rp_report.py --report_start_date yyyy-mm-dd
'''

`aws-profile-name` should correspond to your ~/.aws/credentials profile name, some of us have called this verify-audit-billing-dev because it's really the *integration* environment. You will be prompted to input an MFA token generated by an authentication app/key associated with your AWS account.

This will generate reports for all the RPs in the `output/` directory.

## Developer Setup
### Managing dependencies
Application and development dependencies are specified in `requirements-app.txt` and 
`requirements-dev.txt` respectively.

If you need to install dependencies for local development, execute `make requirements-dev`. This 
will install application as well as development dependencies. 

You can freeze your versions of 
application dependencies by running `make freeze-requirements`, which will generate 
`requirements.txt` containing the specific versions of application dependencies installed on your 
environment. Building reproducible environments then becomes easier by executing 
`make requirements`, which will only install dependencies specified in `requirements.txt`.

### Git hooks
We are using `pre-commit` to setup Git hooks automatically based on configurations defined within 
`.pre-commit-config.yaml`. 

In order to setup the hooks, you should execute the `./pre-commit` script provided with this 
repository. It will ask you to install `pre-commit` if it isn't already installed. It will use 
`pre-commit` to automatically install pre-push Git hooks in order to allow push only if all tests 
pass.

### Intellij IDE Setup (optional)
After creating the virtual environment (as outlined above):
- On the IntelliJ start page, select `Import Project`
- Choose the root folder of this project (`verify-performance-scripts`), then `Next`
- Select the option `Import project from existing sources`
- Continue until the `Select SDK` screen, where we will configure Intellij to use the Virtualenv
  - Click `+` on the top-left to add sdk 
  - choose `Virtualenv environment`, `Existing environment` 
  - set the `Python Interpreter` field to the file `verify-performance-scripts/venv/bin/python3`
- Continue until end of setup.

