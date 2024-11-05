import math

from src.models import BaseParameter


class ProcessorReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        storage = kwargs.get("storage", 0)
        distributed = kwargs.get("distributed", 0)
        self.value = 3 if agents > 0 and storage > 0 and distributed else 0
        return self.value


class ProcessorMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        traffic = kwargs.get("traffic", 0)
        self.value = traffic * 0.5 if distributed else 100
        return self.value


class ProcessorCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 3

    def calculate(self, **kwargs):
        self.value = 3
        return self.value


class ProcessorStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        nodes = kwargs.get("nodes", 0)
        self.value = math.ceil(
            (-4.25877 + 0.98271 * math.log(agents)) * 1000) / 1000 if nodes > 0 else 0
        return self.value
