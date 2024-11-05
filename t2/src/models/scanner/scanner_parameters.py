import math

from src.models import BaseParameter


class ScannerReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        self.value = 1 if agents > 0 else 0
        return self.value


class ScannerMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 300

    def calculate(self, **kwargs):
        self.value = 300
        return self.value


class ScannerCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        self.value = 1
        return self.value


class ScannerStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        distributed = kwargs.get("distributed", 0)
        self.value = math.ceil(
            (0.0002 * agents + 0.6) * 1000) / 1000 if distributed else 0
        return self.value
