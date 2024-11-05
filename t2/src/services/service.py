from src.parameters.parameter_factory import ParameterFactory


class Service:
    def __init__(self, service_name, config):
        """
        Инициализация сервиса с параметрами на основе конфигурации JSON.

        :param service_name: str - имя сервиса
        :param config: dict - конфигурация параметров для сервиса
        """
        self.service_name = service_name
        self.config = self._initialize_parameters(config)

    def _initialize_parameters(self, config):
        """
        Инициализация параметров сервиса. Если параметр отсутствует, он инициализируется значением по умолчанию для своего класса.

        :param config: dict - конфигурация сервиса
        :return: dict - инициализированные параметры
        """
        parameters = {}
        for param_name, param_value in config.items():
            try:
                parameters[param_name] = ParameterFactory.create_parameter(
                    self.service_name, param_name, param_value)
            except Exception as ex:
                continue
        return parameters

    def update_parameters(self, **kwargs):
        """
        Обновляет значения параметров сервиса на основе переданных аргументов.

        :param kwargs: dict - именованные параметры
        :return: dict - обновленная конфигурация сервиса
        """
        updated_config = {}
        for param_name, parameter in self.config.items():
            updated_config[param_name] = parameter.calculate(**kwargs)
        return updated_config
