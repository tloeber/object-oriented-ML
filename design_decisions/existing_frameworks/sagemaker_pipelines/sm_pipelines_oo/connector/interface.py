from abc import ABC, abstractmethod

from sagemaker.session import Session
from sagemaker.workflow.pipeline_context import LocalPipelineSession


class AWSConnectorInterface(ABC):
    @property
    @abstractmethod
    def sm_session(self) -> Session | LocalPipelineSession :
        ...

    @property
    @abstractmethod
    def sm_client(self):
        ...

    @property
    @abstractmethod
    def sm_runtime_client(self):
        ...

    @property
    @abstractmethod
    def role_arn(self) -> str:
        ...
