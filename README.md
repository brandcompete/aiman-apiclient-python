# AIMan API-Client by brandCompete
[![Package](https://img.shields.io/badge/package-latest-blue.svg)](https://test.pypi.org/project/aiman) [![brandCompete](https://img.shields.io/badge/brandcompete-home-darkred.svg)](https://www.brandcompete.com) [![AIMan](https://img.shields.io/badge/aiman_ui-dev-green.svg)](https://aiman-dev.brandcompete.com) [![AIMan](https://img.shields.io/badge/aiman_api-dev-green.svg)](https://aiman-api-dev.brandcompete.com/api/v1/spec-ext.html)

## Preconditions
Python version: >=3.8.1,<=3.12

## Installation

```
pip install aiman
```

## Getting started

### Instantiate the api client
IMPORTANT: Use only the base address of the api as the url, like in this example:
```
from brandcompete.client import AIManServiceClient

client = AIManServiceClient(
    host_url="https://aiman-api-test.brandcompete.com",
    user_name="john@doe.com",
    password="top_secret")
```

#### Autorefresh JWT-Token
The client takes care of updating the token during the client's runtime if it has expired.

### Fetching available AI-Models
This method returns a list of available models of type: AIModel (```List[AIModel]```)
The ```model_tag_id``` needs always be specified for a prompt. This specification is located in each AIModel object. Alternatively, you can also view available models [here](https://aiman-dev.brandcompete.com/help/models)
```
models = client.get_models()
for model in models:
    print(f"[default tag:{model.default_model_tag_id:4}] {model.name.upper():25} - {model.short_description}")
```

### Prompting a simple query to a specific model

In order to submit a query, the model must be passed as a parameter via ```model_tag```
```
response:str = client.prompt(
    model_tag_id=10,
    query="my question to AI-Model")
```

### Prompting a query and attach one or more files
```    
response:dict = client.prompt(
    model_tag_id=1, 
    query="My query ask something about the given file content...", 
    attachments=["file/path/file_1.pdf", "file/path/file_2.xlsx"])
   
```

## Raging with datasources and documents
### Datasource
Init a new datasource (minimum requirements - name and summary)
```
datasource_id = client.init_new_datasource(
    name="Test datasource", 
    summary="New datasource for uploading some documents")
```
Or init a new datasource with a list of tags and categories
```
datasource_id = client.init_new_datasource(
    name="Test datasource", 
    summary="New datasource for uploading documents", 
    tags=["tagA","tagB", "etc"], 
    categories=["catA","catB","etc"])
```
Fetch all datasources (associated to my account).
Possible status: 
- (2)ready
- (1)indexing
- (0)pending

```
datasources = client.fetch_all_datasources()
for source in datasources:
    print(f"{source.id}")
    print(f"{source.name}")
    print(f"{source.status}")
```
### Documents
Add multiple documents into a datasource (can be url or file)
```
client.add_documents(
    data_source_id=your_ds_id, 
    sources=["path/to_my_data/test.pdf", "https://www.brandcompete.com"] )
```
### Prompt on datasource context
Prompt in conjunction with a ```datasource_id```. You have to use the ```model_tag_id``` to specify the model to prompt.
NOTE: The datasource requires status == 2 and should be checked before prompting.
```    
client.prompt_on_datasource(
    datasource_id=datasource_id, 
    model_tag_id=200, 
    query="can you please summarize the content?", 
    prompt_options = None)
```