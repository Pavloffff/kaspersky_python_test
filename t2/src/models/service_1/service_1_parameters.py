import math

from src.models import BaseParameter


class Service1EnabledParameter(BaseParameter):
    @staticmethod
    def default_value():
        return False

    def calculate(self, **kwargs):
        traffic = kwargs.get("traffic", 0)
        self.value = True if traffic > 0 else False
        return self.value


class Service1NodesParameter(BaseParameter):
    _disc_divisor = 10000

    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        disk_storage = kwargs.get("disk_storage", 0)
        self.value = math.ceil(disk_storage / self._disc_divisor)
        return self.value


class Service1CpuCoresParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 5

    def calculate(self, **kwargs):
        self.value = 5
        return self.value


class Service1MemoryParameter(BaseParameter):
    _disc_divisor = 10000

    @staticmethod
    def default_value():
        return 0.0

    def calculate(self, **kwargs):
        disk_storage = kwargs.get("disk_storage", 0)
        self.value = math.ceil(disk_storage / self._disc_divisor)
        return self.value
