# osio-chatbot

## Design
![Diagram](https://raw.github.com/ravsa/osio-chatbot/master/diagram.jpeg)

## Create a virtualenv
```bash
    virtualenv -p python3 --no-site-packages --clear venv
```

## Install the requirements
```bash
    pip install spacy
    python -m spacy download en_core_web_md
    python -m spacy link en_core_web_md en
    python -m spacy download en
```

```bash
    pip install -r requirements.txt
```


## tool for generate training data

```bash
    npm i -g rasa-nlu-trainer
    rasa-nlu-trainer -v <path to the training data file>
```
