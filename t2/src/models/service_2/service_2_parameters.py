import math

from src.models import BaseParameter


class Service2EnabledParameter(BaseParameter):
    @staticmethod
    def default_value():
        return True

    def calculate(self, **kwargs):
        self.value = True
        return self.value


class Service2NodesParameter(BaseParameter):
    _disc_divisor = 100000

    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        disk_storage = kwargs.get("disk_storage", 0)
        self.value = 2 if math.ceil(
            disk_storage / self._disc_divisor) > 3 else 1
        return self.value


class Service2CpuCoresParameter(BaseParameter):
    _divisor = 100000 * 8

    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        traffic = kwargs.get("traffic", 0)
        self.value = math.ceil(traffic / self._divisor)
        return self.value


class Service2MemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 100.0

    def calculate(self, **kwargs):
        self.value = 100.0
        return self.value
