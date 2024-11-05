import copy

from src.services import Service


def _initialize_services(config):
    """
    Инициализация сервисов на основе конфигурации JSON.

    :param config: dict - начальная конфигурация
    :return: dict - словарь с экземплярами сервисов
    """
    services = {}
    for service_name, service_config in config.items():
        services[service_name] = Service(service_name, service_config)
    return services


class Calculator:
    def __init__(self, config):
        """
        Инициализация калькулятора на основе конфигурации JSON.

        :param config: dict - начальная конфигурация JSON, содержит информацию о необходимых сервисах и параметрах
        """
        self._config = copy.deepcopy(config)
        self.services = _initialize_services(config)

    def update_config(self, **kwargs):
        """
        Обновляет конфигурацию сервисов на основе входных параметров.

        :param kwargs: dict - именованные параметры, передаваемые сервисам
        :return: dict - обновленная конфигурация
        """
        updated_config = {}
        for service_name, service in self.services.items():
            updated_config[service_name] = service.update_parameters(**kwargs)
        return updated_config
