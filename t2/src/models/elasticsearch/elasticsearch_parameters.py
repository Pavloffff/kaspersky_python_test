from src.models import BaseParameter


class ElasticsearchReplicasParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 1

    def calculate(self, **kwargs):
        distributed = kwargs.get("distributed", 0)
        self.value = 3 if distributed else 1
        return self.value


class ElasticsearchMemoryParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        self.value = 0
        return self.value


class ElasticsearchCpuParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 3

    def calculate(self, **kwargs):
        self.value = 3
        return self.value


class ElasticsearchStorageParameter(BaseParameter):
    @staticmethod
    def default_value():
        return 0

    def calculate(self, **kwargs):
        agents = kwargs.get("agents", 0)
        if agents < 5000:
            self.value = 0.256
        elif agents < 10000:
            self.value = 0.512
        else:
            self.value = 1
        return self.value
