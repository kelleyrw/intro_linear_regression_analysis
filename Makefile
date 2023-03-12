PHONY: help, setup, install

# ---------------------------------------------------------------------------- #

python_version = 3.11.1
python_env = tr_linreg3111
dsc_version=$$(python -c "import dsc; print(dsc.get_version())")

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------- #
# devoloper python setup
# ---------------------------------------------------------------------------- #

setup:   ## setup python virtual environment
	pyenv install --skip-existing $(python_version) &&\
	pyenv uninstall -f $(python_env) &&\
	pyenv virtualenv --force $(python_version) $(python_env) &&\
	pyenv local $(python_env) &&\
	pip install --upgrade pip &&\
	pip install -r requirements.txt 

install:   ## install/reinstall python requirements into virtual env
	pip install --upgrade pip &&\
	pip install -r requirements.txt 
