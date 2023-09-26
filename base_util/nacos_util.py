import logging
import os
from collections import namedtuple

from nacos import NacosClient
from nacos.client import CacheData
from nacos.params import group_key

DEFAULTS_CONFIG = {
    "addresses": "10.101.84.2:8848",
    "namespace": "27098070-77c6-449f-9f23-5f0e5dc53fca",
    "username": "nacos",
    "password": "!Keyironghe123",
}
DEFAULTS = namedtuple("GenericDict", DEFAULTS_CONFIG)(**DEFAULTS_CONFIG)  # type: ignore


class NacosClientWrapper:
    def __init__(self, server_addresses=None, namespace=None, username=None, password=None):
        self.nacos_client = SciArtNacosClient(server_addresses, namespace, username, password)

    def get_config(self, data_id, group, timeout=None, no_snapshot=None, default=None):
        return self.nacos_client.sci_art_get_config(data_id, group, timeout, no_snapshot, default)


class SciArtNacosClient(NacosClient):
    def __init__(self, server_addresses=None, namespace=None, username=None, password=None):
        self.sci_art_addresses = os.getenv("NACOS_ADDRESSES", choose(server_addresses, DEFAULTS.addresses))
        self.sci_art_namespace = os.getenv("NACOS_NAMESPACE", choose(namespace, DEFAULTS.namespace))
        self.sci_art_username = os.getenv("NACOS_USERNAME", choose(username, DEFAULTS.username))
        self.sci_art_password = os.getenv("NACOS_PASSWORD", choose(password, DEFAULTS.password))

        super().__init__(self.sci_art_addresses, namespace=self.sci_art_namespace,
                         username=self.sci_art_username, password=self.sci_art_password)

    def sci_art_get_config(self, data_id, group, timeout=None, no_snapshot=None, default=None):
        cache_key = group_key(data_id, group, self.namespace)
        # read cache value from nacos failover base or snapshot base
        cache_value = CacheData(cache_key, self).content
        if cache_value is None:
            cache_value = self.try_get_nacos_config(data_id, group, timeout, no_snapshot, default)
        if self.puller_mapping is None or cache_key not in self.puller_mapping:
            # add cache_key to config change listener
            self.try_add_config_watcher(data_id, group)
        return cache_value

    def try_get_nacos_config(self, data_id, group, timeout=None, no_snapshot=None, default=None):
        """支持默认值，代理父类配置调用方法"""
        nacos_config = self.get_config(data_id, group, timeout, no_snapshot)
        logging.info("get nacos config: data_id=%s, group=%s, value=%s", data_id, group, nacos_config)
        if nacos_config is None:
            return default
        else:
            return nacos_config

    def try_add_config_watcher(self, data_id, group):
        """添加配置变更监听"""

        def config_update_listener(data):
            _data_id = data["data_id"]
            _group = data["group"]
            _content = data["content"]
            logging.info("nacos config changed, data_id=%s, group=%s, new_value=%s", _data_id, _group, _content)
            pass

        self.add_config_watcher(data_id, group, config_update_listener)

    def _inject_auth_info(self, headers, params, data, module="config"):
        """重写父类方法，修复授权认证问题"""
        if not params and self.sci_art_username and self.sci_art_password:
            params.update({"username": self.sci_art_username, "password": self.sci_art_password})
        super()._inject_auth_info(headers, params, data, module)


def choose(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None
