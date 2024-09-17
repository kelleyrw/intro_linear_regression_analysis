# intro_linear_regression_analysis

Walkthrough of [Introduction to Linear Regressions Analysis, 5th Edition](https://www.oreilly.com/library/view/introduction-to-linear/9780470542811/).

## setup

### prereqs
___

Install [pyenv](https://github.com/pyenv/pyenv)

```
brew install pyenv
```

### setup python virtual env
___

```
make pyenv-setup
```

Use the makefile via the following CLI calls:

**fresh install** (idempotent):

Build python virtual environment for project and pip install the requirements

```
make pyenv-setup
```

**install packages** (from `requirements.txt`)

```
make pyenv-install
```

**upgrade installed packages** (from `requirements.txt`)

```
make pyenv-upgrade
```

#### IDE
___
Install [Black](https://black.readthedocs.io/en/stable/editor_integration.html)

```
brew install black
```

To setup with Intellij/Pycharm, follow instructions [here](https://black.readthedocs.io/en/stable/integrations/editors.html).


```
brew install isort
```

To setup with Intellij/Pycharm, follow instructions [here](https://github.com/pycqa/isort/wiki/isort-Plugins).


