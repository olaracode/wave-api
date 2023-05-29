set -o errexit
pipenv install
ls
pipenv run upgrade
