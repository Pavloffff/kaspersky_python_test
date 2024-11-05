from src.calculator import Calculator


def test_calculator_empty_config_with_parameters():
    """
    Тестирование Calculator с пустой конфигурацией и передачей параметров.
    Ожидается, что Calculator корректно обработает параметры и выдаст ожидаемый результат.
    """
    empty_config = {}
    params = {"disk_storage": 50000, "traffic": 100}
    expected_result = {}

    calculator = Calculator(empty_config)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "With empty config, updated_config should be empty."


def test_calculator_config_with_extra_params_and_update():
    """
    Тестирование Calculator с конфигурацией, содержащей лишние параметры, и обновлением параметров.
    Ожидается, что лишние параметры игнорируются, а конфигурация обновляется корректно.
    """
    config_with_extra_params = {
        "service_1": {
            "enabled": True,
            "nodes": 1,
            "cpu_cores": 5,
            "memory": 1024,
            "extra_param": "unexpected"
        }
    }
    params = {"disk_storage": 50000, "traffic": 100}
    expected_result = {
        "service_1": {
            "enabled": True,
            "nodes": 5,
            "cpu_cores": 5,
            "memory": 5
        }
    }

    calculator = Calculator(config_with_extra_params)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "Extra parameters should be ignored, and configuration updated correctly."


def test_calculator_config_missing_required_param_with_update():
    """
    Тестирование Calculator с конфигурацией, где отсутствует параметр, и обновлением параметров.
    Ожидается, что отсутствующий параметр также пропадет и в выходных данных.
    """
    config_missing_param = {
        "service_1": {
            "enabled": True,
            "cpu_cores": 5,
            "memory": 1024
        }
    }
    params = {"disk_storage": 50000, "traffic": 100}
    expected_result = {
        "service_1": {
            "enabled": True,
            "cpu_cores": 5,
            "memory": 5
        }
    }

    calculator = Calculator(config_missing_param)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "Missing parameters."


def test_calculator_minimal_parameters():
    """
    Тестирование Calculator с минимальными значениями параметров.
    Ожидается, что Calculator корректно обработает параметры с нулевыми или минимальными значениями.
    """
    minimal_config = {
        "service_1": {
            "enabled": False,
            "nodes": 0,
            "cpu_cores": 0,
            "memory": 0
        }
    }
    params = {"disk_storage": 0, "traffic": 0}
    expected_result = {
        "service_1": {
            "enabled": False,
            "nodes": 0,
            "cpu_cores": 5,
            "memory": 0
        }
    }

    calculator = Calculator(minimal_config)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "Minimal parameters should result in default initialized state."


def test_calculator_maximal_parameters():
    """
    Тестирование Calculator с очень большими значениями параметров.
    Ожидается, что Calculator корректно обработает параметры и не выйдет за пределы разумных значений.
    """
    maximal_config = {
        "service_1": {
            "enabled": False,
            "nodes": 0,
            "cpu_cores": 5,
            "memory": 0
        }
    }
    params = {"disk_storage": 1_000_000_000, "traffic": 1_000_000}
    expected_result = {
        "service_1": {
            "enabled": True,
            "nodes": 100000,
            "cpu_cores": 5,
            "memory": 100000
        }
    }

    calculator = Calculator(maximal_config)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "Maximal parameters should be handled correctly by Calculator."


def test_calculator_multiple_services_config():
    """
    Тестирование конфигурации с несколькими сервисами.
    Ожидается, что Calculator корректно обновит все указанные сервисы.
    """
    multi_service_config = {
        "service_1": {
            "enabled": False,
            "nodes": 1,
            "cpu_cores": 5,
            "memory": 1
        },
        "service_2": {
            "enabled": True,
            "nodes": 2,
            "cpu_cores": 3,
            "memory": 100
        }
    }
    params = {"disk_storage": 200000, "traffic": 5000}
    expected_result = {
        "service_1": {
            "enabled": True,
            "nodes": 20,
            "cpu_cores": 5,
            "memory": 20
        },
        "service_2": {
            "enabled": True,
            "nodes": 1,
            "cpu_cores": 1,
            "memory": 100
        }
    }

    calculator = Calculator(multi_service_config)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result, "Multiple services should be updated correctly according to parameters."


def test_calculator_with_config_and_params():
    config = {
        "kafka": {
            "enabled": False,
            "replicas": 1,
            "memory": 0.0,
            "cpu": 0,
            "storage": 0
        },
        "elasticsearch": {
            "enabled": True,
            "replicas": 1,
            "memory": 0,
            "cpu": 3,
            "storage": 0
        },
        "processor": {
            "enabled": False,
            "replicas": 0,
            "memory": 100,
            "cpu": 3,
            "storage": 0
        },
        "server": {
            "enabled": True,
            "replicas": 1,
            "memory": 100,
            "cpu": 1,
            "storage": 0
        },
        "database_server": {
            "enabled": True,
            "replicas": 1,
            "memory": 100,
            "cpu": 1,
            "storage": 0
        },
        "clickhouse": {
            "enabled": True,
            "replicas": 1,
            "memory": 100,
            "cpu": 1,
            "storage": 0
        },
        "synchronizer": {
            "enabled": True,
            "replicas": 1,
            "memory": 100,
            "cpu": 1,
            "storage": 0
        },
        "scanner": {
            "enabled": True,
            "replicas": 1,
            "memory": 300,
            "cpu": 1,
            "storage": 0
        }
    }

    params = {
        "agents": 8000,
        "storage": 250000,
        "traffic": 1500,
        "mail_traffic": 500,
        "distributed": True,
        "nodes": 10
    }

    expected_result = {
        "kafka": {
            "replicas": 3,
            "memory": 250.0,
            "cpu": 5.97,
            "storage": 3.524
        },
        "elasticsearch": {
            "replicas": 3,
            "memory": 0,
            "cpu": 3,
            "storage": 0.512
        },
        "processor": {
            "replicas": 3,
            "memory": 750.0,
            "cpu": 3,
            "storage": 4.574
        },
        "server": {
            "replicas": 2,
            "memory": 750,
            "cpu": 1,
            "storage": 17.516
        },
        "database_server": {
            "replicas": 1,
            "memory": 400000.0,
            "cpu": 1,
            "storage": 8959.936
        },
        "clickhouse": {
            "replicas": 1,
            "memory": 400000.0,
            "cpu": 1,
            "storage": 1.141
        },
        "synchronizer": {
            "replicas": 1,
            "memory": 80.0,
            "cpu": 1,
            "storage": 2.2
        },
        "scanner": {
            "replicas": 1,
            "memory": 300,
            "cpu": 1,
            "storage": 2.2
        }
    }

    calculator = Calculator(config)
    updated_config = calculator.update_config(**params)
    assert updated_config == expected_result
