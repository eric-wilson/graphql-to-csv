
## Dev Environment Setup


### MacOS / Linux
```sh
python3 -m venv .venv
source ./.venv/bin/activate
# is source doesn't work
#. ./.venv/bin/activate
touch ./.venv/pip.conf

pip install -r ./requirements.txt
pip install -r ./requirements.dev.txt
pip install -e .
```


### Windows

