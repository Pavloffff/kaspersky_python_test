import math

from src.models import BaseParameter


class ClickhouseReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        distributed = kwargs.get("distributed", 0)
        self.value = max(round((agents / 15000) / 10) * 10,
                         1) if distributed and agents > 0 else 1
        return self.value


class ClickhouseMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        storage = kwargs.get("storage", 0)
        self.value = round((storage * 1.6) * 1000) / \
            1000 if distributed else 100
        return self.value


class ClickhouseCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        self.value = 1
        return self.value


class ClickhouseStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        distributed = kwargs.get("distributed", 0)
        self.value = math.ceil(
            (0.0000628 * agents + 0.6377) * 1000) / 1000 if distributed else 0
        return self.value
