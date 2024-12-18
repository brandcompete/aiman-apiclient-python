# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=too-many-locals
# pylint: disable=too-many-return-statements
"""Module providing a aiman service client"""
import json
import base64
from typing import (
    List,
    Optional
)
import requests
from brandcompete.core.util import Util
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import (
    AIModel,
    Attachment,
    DataSource,
    PromptOptions,
    Route,
    Prompt,
    RequestType
)


class AIManServiceClient():
    """Represents the AI Manager Service Client"""

    def __init__(self, host_url:str = None, user_name:str = None, password:str = None, token_credential:TokenCredential = None ) -> None:
        """ Instantiate a new Client to communicate with an AIMan API
            NOTE: Use host, user and password or a TokenCredential Object

        Args:
            host_url (str, optional): _description_. Defaults to None.
            user_name (str, optional): _description_. Defaults to None.
            password (str, optional): _description_. Defaults to None.
            token_credential (TokenCredential, optional): _description_. Defaults to None.

        Raises:
            ValueError: Missing credential informations
        """
        if token_credential is None:
            if host_url is None:
                raise ValueError("Missing parameter: host_url. EXPLAIN")
            if password is None:
                raise ValueError("Missing parameter: password. ")
            if user_name is None:
                raise ValueError("Missing parameter: username. ")
            token_credential = TokenCredential(api_host_url=host_url, user_name=user_name,password=password)
        self.credential = token_credential
        self.request_timeout = 200

    def get_models(self) -> List[AIModel]:
        """Get all available models to prompt on

        Returns:
            List[AIModel]: List of available AIModel objects
        """
        results = self._perform_request(
            request_type=RequestType.GET, route=Route.GET_MODELS.value)
        models = []
        for model in results['Models']:
            models.append(AIModel.from_dict(model))

        return models

    def prompt(self, **kwargs) -> dict:
        """_summary_

        Args:
            model_tag (int): the model id
            query (str): Query to prompt
            loader (Optional[Loader], optional): Content loader. Defaults to None.
            attachments (Optional[str], optional): Absolute path to a file. Defaults to None.
            prompt_options (Optional[PromptOptions], optional): Prompt options. Defaults to None.

        Raises:
            ValueError: If any of the required parameters are missing

        Returns:
            dict: The API-Response as dict
        """
        if "model_tag" not in kwargs:
            raise ValueError(
                "Error: missing required argument: model_tag")

        if "query" not in kwargs:
            raise ValueError(
                "Error: missing required argument: query")

        model_tag: int = kwargs["model_tag"]
        query = kwargs["query"]
        attachments = kwargs["attachments"] if "attachments" in kwargs else None
        prompt_options = kwargs["prompt_options"] if "prompt_options" in kwargs else None

        if prompt_options is None:
            prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        if attachments is not None:
            medias = self._build_media_attachments(attachments)
            prompt_dict['attachments'] = []
            for media in medias:
                prompt_dict['attachments'].append(media.to_dict(media))

        prompt_dict['raw'] = prompt_options.raw
        prompt_dict['keepContext'] = prompt_options.keep_context

        route = Route.PROMPT.value.replace("model_tag", f"{model_tag}")
        response = self._perform_request(
            RequestType.POST, route=route, data=prompt_dict)
        return response

    def prompt_on_datasource(self, datasource_id: int, model_tag_id: int, query: str, prompt_options: PromptOptions = None) -> dict:
        """Prompt on a datasource (by id)

        Args:
            datasource_id (int): The datasource id (related to current account)
            model_tag_id (int): Model tag id
            query (str): The query to prompt
            prompt_options (PromptOptions, optional): Prompt options. Defaults to None.

        Returns:
            dict: The API-Response as dict
        """
        if prompt_options is None:
            prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt.datasource_id = datasource_id
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict

        route = f"{Route.PROMPT_WITH_DATASOURCE.value}/{model_tag_id}"
        response = self._perform_request(
            RequestType.POST, route=route, data=prompt_dict)
        return response

    def _get_document_content(self, file_path: str) -> Optional[str]:
        """Parsing document content)

        Args:
            file_path (str): The absolute file path
            loader (Loader, optional): Loader to use for parsing content. Defaults to None.

        Returns:
            str: None or document content
        """
        with open(file_path, "rb") as rag_file:
            return rag_file.read()


    def fetch_all_datasources(self) -> List[DataSource]:
        """Fetch all datasources related to the account

        Returns:
            List[DataSource]: List of datasource objects
        """
        fetch_all_response = self._perform_request(
            RequestType.GET, Route.DATA_SOURCE.value)
        datasources = []
        for response in fetch_all_response["datasources"]:
            source = self.get_datasource_by_id(response["id"])

            datasources.append(source)
        return datasources

    def get_datasource_by_id(self, datasource_id: int) -> Optional[DataSource]:
        """Get a specific datasource by id

        Args:
            datasource_id (int): the datasource id

        Returns:
            DataSource: None or Datasource object
        """
        url = f"{Route.DATA_SOURCE.value}/{datasource_id}"
        response = self._perform_request(RequestType.GET, url)
        source = response["datasource"]
        return DataSource.from_dict(source)

    def init_new_datasource(self, name: str, summary: str, tags: List[str] = None, categories: List[str] = None) -> int:
        """Initiate and add a new datasource to current account

        Args:
            name (str): datasource name
            summary (str): summary
            tags (List[str], optional): A list of tags. Defaults to None.
            categories (List[str], optional): a list of categories. Defaults to None.

        Returns:
            int: The datasource id
        """
        data = {
            "name": name,
            "summary": summary,
            "tags": [] if tags is None else tags,
            "categories": [] if categories is None else categories,
            "assocContexts": [],
            "media": []
        }
        response = self._perform_request(
            request_type=RequestType.POST, route=Route.DATA_SOURCE.value, data=data)

        if "datasource" in response:
            datasource = response["datasource"]
            if "id" in datasource:
                return datasource["id"]
        return -1

    def delete_datasource(self, datasource_id: int) -> bool:
        """Delete a specific datasource by id

        Args:
            datasource_id (int): the datasource id

        Returns:
            bool: success true or false
        """
        code: int = self._perform_request(
            request_type=RequestType.DELETE, route=f"{Route.DATA_SOURCE.value}/{datasource_id}")
        return code

    def add_documents(self, data_source_id: int, sources: List[str]) -> DataSource:
        """Add one or more documents (files, urls) to an datasource

        Args:
            data_source_id (int): the datasource id
            sources (List[str]): list of file paths or urls

        Raises:
            Exception: If datasource not exists

        Returns:
            DataSource: the datasource with all added documents (media list)
        """
        datasource: DataSource = self.get_datasource_by_id(
            datasource_id=data_source_id)
        datasource.media = self._build_media_attachments(sources=sources)

        return self.update_datasource(datasource=datasource)

    def update_datasource(self, datasource: DataSource) -> DataSource:
        """Update an existing datasource

        Args:
            datasource (DataSource): The datasource to update

        Returns:
            DataSource: Updated datasource
        """
        data = {
            "name": datasource.name,
            "summary": datasource.summary,
            "categories": datasource.categories,
            "tags": datasource.tags,
            "assocContexts": datasource.assoc_contexts,
            "media": datasource.media}

        response = self._perform_request(
            RequestType.PUT, f"{Route.DATA_SOURCE.value}/{datasource.id}", data=data)
        return response

    def _build_media_attachments(self, sources: List[str]) -> List[Attachment]:
        """ Warning. This method is private and should not be called manually
        Args:
            sources (List[str]): List of file paths or url

        Raises:
            ValueError: By unsupported file types

        Returns:
            List[Attachments]: List of Attachment instances
        """
        medias = []
        for path_or_url in sources:
            attachment = Attachment()
            path_or_url = path_or_url.lower()
            if Util.validate_url(url=path_or_url, check_only=True):
                attachment.name = path_or_url
                attachment.mime_type = "text/x-uri"
                medias.append(attachment)
                continue

            filename, file_ext = Util.get_file_name_and_ext(file_path=path_or_url)
            mime_type = Util.get_mimetype_by_ext(file_ext=file_ext)
            if mime_type is None:
                raise ValueError(
                    f"Error: Unsupported filetype:{file_ext} (file:{filename})")

            attachment.base64 = base64.b64encode(self._get_document_content(file_path=path_or_url)).decode()
            attachment.name = filename
            attachment.size = ((len(attachment.base64) * (3/4)) - 1) * 10
            attachment.mime_type = mime_type
            medias.append(attachment)

        return medias

    def _perform_request(self, request_type: RequestType, route: str, data: dict = None) -> dict:
        """Warning. This method is private and should not be called manually

        Args:
            request_type (RequestType): Enum of RequestTypes (GET, POST, PUT and DELETE)
            route (str): _description_
            data (dict, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            dict: _description_
        """
        if self.credential.auto_refresh_token and Util.is_token_expired(self.credential.access.expires_on):
            self.credential.refresh_access_token()

        url = f"{self.credential.api_host}{route}"
        response = None
        headers = {"accept": "application/json"}
        headers.update(
            {"Authorization": f"Bearer {self.credential.access.token}"})
        if request_type == RequestType.GET:
            response = requests.get(
                url=url,
                headers=headers,
                allow_redirects=True,
                timeout=self.request_timeout)

        if request_type == RequestType.POST:
            headers.update({"Content-Type": "application/json"})
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
                allow_redirects=True,
                timeout=self.request_timeout)

        if request_type == RequestType.DELETE:
            headers.update({"Content-Type": "application/json"})
            response = requests.delete(
                url=url,
                headers=headers,
                allow_redirects=True,
                timeout=self.request_timeout)
            return response.status_code

        if request_type == RequestType.PUT:
            headers.update({"Content-Type": "application/json"})
            response = requests.put(
                url=url,
                headers=headers,
                json=data,
                allow_redirects=True,
                timeout=self.request_timeout)

        if response.status_code not in [200, 201, 202]:
            raise RuntimeError(
                f"[{response.status_code}] Reason: {response.reason}")

        content = json.loads(response.content.decode('utf-8'))
        return content['messageContent']['data']
