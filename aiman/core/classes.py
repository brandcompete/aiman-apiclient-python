"""Module providing different dataclasses"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class AIModel:

    """Represents a AIModel instance"""
    id: int
    uu_id: str
    name: str
    short_description: str
    long_description: str
    default_model_tag_id: int
    amount_of_pulls: str
    amount_of_tags: int
    required_memory: str
    size: int

    @classmethod
    def to_dict(cls):
        """Parsing a AIModel Instance to a dict"""
        return {
            "id": cls.id,
            "uuId": cls.uuid,
            "name": cls.name,
            "shortDescription": cls.short_description,
            "longDescription": cls.long_description,
            "defaultModelTagId": cls.default_model_tag_id,
            "amountOfPulls": cls.amount_of_pulls,
            "amountOfTags": cls.amount_of_tags,
            "requiredMemory": cls.required_memory,
            "size": cls.size
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a AIModel Instance"""
        cls.id = 0 if "id" not in values else values["id"]
        cls.uuid = "" if "uuId" not in values else values["uuId"]
        cls.name = "" if "name" not in values else values["name"]
        cls.short_description = "" if "shortDescription" not in values else values["shortDescription"]
        cls.long_description = "" if "longDescription" not in values else values["longDescription"]
        cls.default_model_tag_id = 0 if "defaultModelTagId" not in values else values["defaultModelTagId"]
        cls.amount_of_pulls = "" if "amountOfPulls" not in values else values["amountOfPulls"]
        cls.amount_of_tags = 0 if "amountOfTags" not in values else values["amountOfTags"]
        cls.required_memory = "" if "requiredMemory" not in values else values["requiredMemory"]
        cls.size = 0 if "size" not in values else values["size"]
        return cls


@dataclass
class Project:
    """Represents an aiman project"""
    id: int
    uuid: str
    owner_id: int
    name: str
    description: str

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "id":           cls.id,
            "uuId":         cls.uuid,
            "ownerId":      cls.owner_id,
            "name":         cls.name,
            "description":  cls.description
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.id = values["id"]
        cls.uuid = values["uuId"]
        cls.owner_id = values["ownerId"]
        cls.name = values["name"]
        cls.description = values["description"]
        return cls


@dataclass
class Query:
    """Represents a prompt query"""
    id: int
    uuid: str

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "id":   cls.id,
            "uuId": cls.uuid
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.id = values["id"]
        cls.uuid = values["uuId"]
        return cls


@dataclass
class PromptOptions:
    """Represents prompt options"""
    mirostat: int = 0
    mirostat_eta: float = 0.1
    mirostat_tau: int = 5
    num_ctx: int = 4096
    num_gqa: int = 8
    num_gpu: int = 0
    num_thread: int = 0
    repeat_last_n: int = 64
    repeat_penalty: float = 1.1
    temperature: float = 0.8
    seed: int = 0
    stop = None
    tfs_z: int = 1
    num_predict: int = 2048
    top_k: int = 40
    top_p: float = 0.9
    raw: bool = False
    keep_context: bool = True

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "mirostat":         cls.mirostat,
            "mirostat_eta":     cls.mirostat_eta,
            "mirostat_tau":     cls.mirostat_tau,
            "num_ctx":          cls.num_ctx,
            "num_gqa":          cls.num_gqa,
            "num_gpu":          cls.num_gpu,
            "num_thread":       cls.num_thread,
            "repeat_last_n":    cls.repeat_last_n,
            "repeat_penalty":   cls.repeat_penalty,
            "temperature":      cls.temperature,
            "seed":             cls.seed,
            "stop":             cls.stop,
            "tfs_z":            cls.tfs_z,
            "num_predict":      cls.num_predict,
            "top_k":            cls.top_k,
            "top_p":            cls.top_p,
            "raw":              cls.raw,
            "keep_context":     cls.keep_context
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.mirostat = 0 if "mirostat" not in values else values["mirostat"]
        cls.mirostat_eta = 100 if "mirostat_eta" not in values else values["mirostat_eta"]
        cls.mirostat_tau = 5 if "mirostat_tau" not in values else values["mirostat_tau"]
        cls.num_ctx = 4096 if "num_ctx" not in values else values["num_ctx"]
        cls.num_gqa = 8 if "num_gqa" not in values else values["num_gqa"]
        cls.num_gpu = 0 if "num_gpu" not in values else values["num_gpu"]
        cls.num_thread = 0 if "num_thread" not in values else values["num_thread"]
        cls.repeat_last_n = 64 if "repeat_last_n" not in values else values["repeat_last_n"]
        cls.repeat_penalty = 1.1 if "repeat_penalty" not in values else values["repeat_penalty"]
        cls.temperature = 0.8 if "temperature" not in values else values["temperature"]
        cls.seed = 0 if "seed" not in values else values["seed"]
        cls.stop = None if "stop" not in values else values["stop"]
        cls.tfs_z = 1 if "tfs_z" not in values else values["tfs_z"]
        cls.num_predict = 2048 if "num_predict" not in values else values["num_predict"]
        cls.top_k = 40 if "top_k" not in values else values["top_k"]
        cls.top_p = 0.9 if "top_p" not in values else values["top_p"]
        cls.raw = False if "raw" not in values else values["raw"]
        cls.keep_context = True if "keep_context" not in values else values["keep_context"]
        return cls


@dataclass
class Prompt:
    """Represents a prompt"""
    prompt: str = ""
    model_tag_id: int = 0
    raw: bool = False
    stream: bool = False
    project_id: int = 1
    project_tab_id: int = 1
    user_id: int = 1
    verbose: int = True
    attachments: list = None
    keep_context: bool = True
    keep_alive: str = "5m"
    datasource_id: int = 0

    @classmethod
    def to_dict(cls):
        """Parsing a Prompt Instance to a dict"""
        return {
            "prompt":       cls.prompt,
            "modelTagId":   cls.model_tag_id,
            "raw":          cls.raw,
            "stream":       cls.stream,
            "projectId":    cls.project_id,
            "projectTabId": cls.project_tab_id,
            "userId":       cls.user_id,
            "verbose":      cls.verbose,
            "attachments":  cls.attachments,
            "keepContext":  cls.keep_context,
            "keepAlive":    cls.keep_alive,
            "datasourceId": cls.datasource_id
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Prompt Instance"""
        cls.prompt = "" if "prompt" not in values else values["prompt"]
        cls.model_tag_id = 0 if "modelTagId" not in values else values["modelTagId"]
        cls.raw = False if "raw" not in values else values["raw"]
        cls.stream = False if "stream" not in values else values["stream"]
        cls.project_id = False if "projectId" not in values else values["projectId"]
        cls.project_tab_id = 0 if "projectTabId" not in values else values["projectTabId"]
        cls.user_id = 0 if "userId" not in values else values["userId"]
        cls.verbose = True if "verbose" not in values else values["verbose"]
        cls.attachments = None if "attachments" not in values else values["attachments"]
        cls.keep_context = True if "keepContext" not in values else values["keepContext"]
        cls.keep_alive = "5m" if "keepAlive" not in values else values["keepAlive"]
        cls.datasource_id = 0 if "datasourceId" not in values else values["datasourceId"]
        return cls


@dataclass
class DataSource:
    """Represents a prompt datasource (raging)"""
    name: str
    summary: str
    id: Optional[int] = -1
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    assoc_contexts: Optional[list] = None
    media: Optional[list] = None
    status: Optional[int] = -1
    media_count: Optional[int] = -1
    owner_id: Optional[int] = -1

    @classmethod
    def to_dict(cls):
        """Parsing a DataSource Instance to a dict"""
        return {
            "name":             cls.name,
            "summary":          cls.summary,
            "id":               cls.categories,
            "categories":       cls.categories,
            "tags":             cls.tags,
            "assocContexts":    cls.assoc_contexts,
            "media":            cls.media,
            "status":           cls.status,
            "mediaCount":       cls.media_count,
            "ownerId":          cls.owner_id
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a DataSource Instance"""
        cls.name = values["name"]
        cls.summary = values["summary"]
        cls.id = values["id"]
        cls.categories = values["categories"]
        cls.tags = values["tags"]
        cls.assoc_contexts = values["assocContexts"]
        cls.media = values["media"]
        cls.status = values["status"]
        cls.media_count = values["mediaCount"]
        cls.owner_id = values["ownerId"]
        return cls


@dataclass
class Media:
    """Represents a prompt media"""
    base64: str

    @classmethod
    def to_dict(cls):
        """Parsing a Media Instance to a dict"""
        return { "base64":  cls.base64}

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Media Instance"""
        cls.base64 = values["base64"]
        return cls


@dataclass
class Attachment:
    """Represents an prompt attachment"""
    name: str = ""
    base64: str = ""
    size: int = 0
    mime_type: str = ""

    @classmethod
    def to_dict(cls):
        """Parsing a Media Instance to a dict"""
        return {
            "base64":   cls.base64,
            "name":     cls.name,
            "size":     cls.size,
            "mime_type":cls.mime_type
            }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Media Instance"""
        if values == {}:
            return cls
        if "name" in values:
            cls.name = values["name"]
        if "base64" in values:
            cls.base64 = values["base64"]
        if "size" in values:
            cls.size = values["size"]
        if "mime_type" in values:
            cls.mime_type = values["mime_type"]
        return cls


class Route(Enum):
    """Enumeration of different routes"""
    GET_MODELS = '/api/v1/models'
    AUTH = '/api/v1/auth/authenticate'
    AUTH_REFRESH = '/api/v1/auth/refresh'
    PROMPT = '/api/v1/prompts/model_tag'
    PROMPT_WITH_DATASOURCE = '/api/v1/prompts'
    DATA_SOURCE = '/api/v1/datasources'


class RequestType(Enum):
    """Enumeration of different request types"""
    POST = 0
    GET = 1
    PUT = 2
    DELETE = 3


__all__ = [
    "AIModel",
    "Project",
    "Query",
    "Route",
    "Prompt",
    "RequestType"
]
