import importlib
from src.models import BaseParameter
from src.utils import snake_to_camel


class ParameterFactory:
    @staticmethod
    def create_parameter(service_name, param_name, initial_value=None):
        """
        Создает параметр для заданного сервиса с уникальной логикой расчета и дефолтным значением.

        :param service_name: str - имя сервиса
        :param param_name: str - имя параметра
        :param initial_value: any - начальное значение параметра
        :return: Parameter - объект параметра с уникальной логикой
        """
        parameter_class_name = f"{snake_to_camel(service_name)}{snake_to_camel(param_name)}Parameter"
        module_path = f"src.models.{service_name.lower()}"

        try:
            module = importlib.import_module(module_path)
            parameter_class = getattr(module, parameter_class_name)
        except Exception as ex:
            raise ex
        return parameter_class(
            initial_value if initial_value is not None else parameter_class.default_value())
