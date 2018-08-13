# osio-chatbot

## Design
![Diagram](https://raw.github.com/ravsa/osio-chatbot/master/diagram.png)

## Create a virtualenv
```bash
    virtualenv -p python3 --no-site-packages --clear venv
```

## Install the requirements
```bash
    pip install spacy
    python -m spacy download en
    python -m spacy download en_core_web_md
    python -m spacy link en_core_web_md en
```

```bash
    pip install -r requirements.txt
```

## Training:
#### NLU:
```bash
	python main.py train nlu
```
	
#### Dialogue:
```bash
	python main.py train dialogue
```	

#### Interactive:
```bash
	python main.py train online
```

## RUN:

#### Console:
```bash
	python main.py run console
```
#### Mattermost:
```bash
	export MATTERMOST_LOGIN_ID=<USERNAME>
	export MATTERMOST_PASSWORD=<BOT PASSWD>

	python main.py run mattermost
```
  

## http-server:
```bash
	python main.py run http-server
```
  
> [GET] ‘api/v1’ 
##### [Response]
```json
{
    "paths": [
        "/api/v1",
        "/api/v1/query"
    ]
}
```


> [POST] ‘api/v1/query’

##### [Request]

```json
HEADER =  {"Authorization ": "Bearer Token"}
```

```json
PAYLOAD = { "query": "<english sentence>",  
			"Timestamp": "<timestamp>"}
```

##### [Response]
```json
RESPONSE = {"response": "<english sentence>",  
			"Timestamp": "<timestamp>"}
```
