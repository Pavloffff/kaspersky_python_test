import math

from src.models import BaseParameter


class SynchronizerReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        self.value = 1 if agents > 0 else 0
        return self.value


class SynchronizerMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        storage = kwargs.get("storage", 0)
        self.value = (math.ceil((storage / 5000) * 1000) /
                      1000) * 1.6 if distributed else 100
        return self.value


class SynchronizerCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        self.value = 1
        return self.value


class SynchronizerStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        distributed = kwargs.get("distributed", 0)
        self.value = math.ceil(
            (0.0002 * agents + 0.6) * 1000) / 1000 if distributed else 0
        return self.value
