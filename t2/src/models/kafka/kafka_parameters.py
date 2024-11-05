import math

from src.models import BaseParameter


class KafkaReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        self.value = 3 if distributed else 1
        return self.value


class KafkaMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0.0

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        mail_traffic = kwargs.get("mail_traffic", 0)
        self.value = mail_traffic * 0.5 if distributed else 100
        return self.value


class KafkaCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0.0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        nodes = kwargs.get("nodes", 0)
        self.value = math.ceil(
            ((0.000169 * agents + 0.437923) * nodes / 3) * 100) / 100
        return self.value


class KafkaStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        self.value = math.ceil((0.0004 * agents + 0.3231) * 1000) / 1000
        return self.value
