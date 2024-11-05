import math

from src.models import BaseParameter


class DatabaseServerReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        distributed = kwargs.get("distributed", 0)
        if agents > 0:
            self.value = max(
                round(
                    (agents / 15000),
                    1),
                1) if distributed else 1
        else:
            self.value = 0
        return self.value


class DatabaseServerMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        storage = kwargs.get("storage", 0)
        self.value = round(storage * 1.6, 3) if distributed else 100
        return self.value


class DatabaseServerCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        self.value = 1
        return self.value


class DatabaseServerStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        nodes = kwargs.get("nodes", 0)
        self.value = math.ceil(((0.00000002 * agents ** 2 + 0.00067749 * \
                               agents + 4.5) * agents / nodes) * 1000) / 1000 if nodes > 0 else 0
        return self.value
