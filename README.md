# API-Galore

LLM Driven website creation. We aim to use guided prompts and API driven cloud infrastructure instantiation to build websites for those that are not too tech-savvy. Our users are expected to provide admin keys to DB and endpoint hosting services, and we will spin up entire websites on their behalf. 


## Installation
Observed issues installing and using autogen locally. It's suggested to use conda virtual env setup (or pip venv):

```bash
conda create -n pyautogen python=3.10  # python 3.10 is recommended as it's stable and not too old
conda activate pyautogen
```

AutoGen requires **Python version >= 3.8**. It can be installed from pip:

```bash
pip install pyautogen
```

The SME are RetrieveAssitantAgents which need to be installed seperately

```bash
pip install "pyautogen[retrievechat]"
```

=======
Automated website creation. We aim to use guided prompts and API driven cloud infrastructure instantiation to build websites for those that are not too tech-savvy. Our users are expected to provide admin keys to DB and endpoint hosting services, and we will spin up entire websites on their behalf. 

