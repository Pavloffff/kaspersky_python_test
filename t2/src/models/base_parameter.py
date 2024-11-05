class BaseParameter:
    def __init__(self, initial_value):
        self.value = initial_value

    @staticmethod
    def default_value():
        """Дефолтное значение для базового параметра."""
        return None

    def calculate(self, **kwargs):
        return self.value
