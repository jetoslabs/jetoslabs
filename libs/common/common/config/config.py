import os
import loguru
import yaml

from common.config.schemas.schema_config import TenantConfig, Config


class ConfigException(BaseException):
    pass


def load_config_folder(config_path: str, *, logger=loguru.logger) -> Config:
    if not os.path.isdir(config_path):
        raise ConfigException("Cannot load config, folder does not exist")
    logger.info(f"Loading Config folder: {config_path}")
    config_root_path = get_config_root(config_path, logger=logger)
    tenant_config_paths = get_tenant_config_paths(config_root_path, logger=logger)
    system_config = load_tenant_config(config_root_path)

    tenant_configs_list = (load_tenant_config(tenant_config_path) for tenant_config_path in tenant_config_paths)
    # tenants = next((tenant_config.tenant for tenant_config in tenant_configs_list))

    tenant_configs = {tenant_config.tenant: tenant_config for tenant_config in tenant_configs_list}

    config: Config = Config(SYSTEM=system_config, tenants=tenant_configs)
    logger.info(f"Config: {config}")
    return config


def is_config_root(filepath: str):
    return os.path.isdir(filepath) and filepath.endswith("config")


def get_config_root(config_path, *, logger=loguru.logger) -> os.path:
    filepaths = (os.path.join(config_path, filename) for filename in os.listdir(config_path))
    potential_config_roots = list(filter(is_config_root, filepaths))
    if len(potential_config_roots) != 1:
        raise ConfigException("Cannot load config, multiple config root exit")
    config_root = potential_config_roots.pop()
    logger.debug(f"Found Config root: {config_root}")
    return config_root


def get_tenant_config_paths(config_root_path, *, logger=loguru.logger):
    filepaths = (os.path.join(config_root_path, filename) for filename in os.listdir(config_root_path))
    tenant_config_paths = list(filter(lambda filepath: os.path.isdir(filepath), filepaths))
    logger.info(f"Found tenant configs: {tenant_config_paths}")
    return tenant_config_paths


def load_tenant_config(tenant_config_folder_path, *, logger=loguru.logger):
    tenant_config_file_path = os.path.join(tenant_config_folder_path, "config.yml")
    if not os.path.isfile(tenant_config_file_path):
        raise ConfigException(f"Cannot load config, config file not found for {tenant_config_file_path}")
    try:
        with open(tenant_config_file_path, mode="rb") as file:
            tenant_config_dict = yaml.safe_load(file)
            tenant_config = TenantConfig(**tenant_config_dict)
            logger.bind(tenant_config_file_path=tenant_config_file_path, tenant_config=tenant_config)\
                .debug(f"Config loaded for tenant - {tenant_config.tenant}")
            return tenant_config
    except Exception as e:
        raise ConfigException() from e
