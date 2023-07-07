from abc import abstractmethod, ABC
from typing import Generic

from oo_ml.interface.data.data_set_type import DataSetType
from oo_ml.interface.data.reader import ReaderInterface
from oo_ml.interface.data.writer import WriterInterface

class BaseDataContainerInterface(ABC, Generic[DataSetType]):
    @classmethod
    @abstractmethod
    def from_subsets(
        cls,
        reader: ReaderInterface[DataSetType],
        writer: WriterInterface[DataSetType],
        train_target, val_target, test_target
    ):
        pass

    @classmethod
    @abstractmethod
    def from_complete_set(
        cls,
        reader: ReaderInterface[DataSetType],
        writer: WriterInterface[DataSetType],
        target,
    ):
        pass

    @abstractmethod
    def get_train_data(self) -> DataSetType:
        pass

    @abstractmethod
    def get_test_data(self) -> DataSetType:
        pass

    @abstractmethod
    def get_validation_data(self) -> DataSetType:
        pass

    @abstractmethod
    def get_all_data(self) -> DataSetType:
        pass
