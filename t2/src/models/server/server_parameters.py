import math

from src.models import BaseParameter


class ServerReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        storage = kwargs.get("storage", 0)
        nodes = kwargs.get("nodes", 0)
        self.value = min(nodes, 2) if agents > 0 and storage > 0 else 0
        return self.value


class ServerMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        traffic = kwargs.get("traffic", 0)
        self.value = math.ceil(traffic * 0.5) if distributed else 100
        return self.value


class ServerCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        self.value = 1
        return self.value


class ServerStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        nodes = kwargs.get("nodes", 0)
        self.value = math.ceil((0.0019 * agents + 2.3154)
                               * 1000) / 1000 if nodes > 0 else 0
        return self.value
