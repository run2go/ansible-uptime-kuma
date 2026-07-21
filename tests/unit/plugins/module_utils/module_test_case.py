import os
import copy
import unittest
import tempfile
from datetime import datetime, timedelta

from uptime_kuma_api import UptimeKumaApi, MonitorType, DockerType, UptimeKumaException, MaintenanceStrategy

# Used for api_key "expires" test fixtures - must stay in the future,
# otherwise the created key immediately reports status "expired".
FUTURE_EXPIRES = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")


class ModuleTestCase(unittest.TestCase):
    api = None
    url = "http://127.0.0.1:3001"
    username = "admin"
    password = "secret123"

    def setUp(self):
        self.api = UptimeKumaApi(self.url, timeout=1, wait_events=0.01)

        filepath = os.path.join(tempfile.gettempdir(), "uptime-kuma-token")
        token = None
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                token = f.read()
        if token:
            try:
                self.api.login_by_token(token)
            except UptimeKumaException:
                token = False

        if not token:
            if self.api.need_setup():
                self.api.setup(self.username, self.password)
            r = self.api.login(self.username, self.password)
            token = r["token"]
            with open(filepath, "w") as f:
                f.write(token)

        # delete monitors
        monitors = self.api.get_monitors()
        for monitor in monitors:
            self.api.delete_monitor(monitor["id"])

        # delete notifications
        notifications = self.api.get_notifications()
        for notification in notifications:
            self.api.delete_notification(notification["id"])

        # delete proxies
        proxies = self.api.get_proxies()
        for proxy in proxies:
            self.api.delete_proxy(proxy["id"])

        # delete tags
        tags = self.api.get_tags()
        for tag in tags:
            self.api.delete_tag(tag["id"])

        # delete status pages
        status_pages = self.api.get_status_pages()
        for status_page in status_pages:
            self.api.delete_status_page(status_page["slug"])

        # delete docker hosts
        docker_hosts = self.api.get_docker_hosts()
        for docker_host in docker_hosts:
            self.api.delete_docker_host(docker_host["id"])

        # delete maintenances
        maintenances = self.api.get_maintenances()
        for maintenance in maintenances:
            self.api.delete_maintenance(maintenance["id"])

        # delete api keys
        api_keys = self.api.get_api_keys()
        for api_key in api_keys:
            self.api.delete_api_key(api_key["id"])

        # login again to receive initial messages
        self.api.disconnect()
        self.api = UptimeKumaApi(self.url)
        self.api.login_by_token(token)

    def tearDown(self):
        self.api.disconnect()

    def run_module(self, module, params):
        params = copy.deepcopy(params)
        result = {
            "changed": False
        }
        module.run(self.api, params, result)
        return result

    def add_monitor(self, name="monitor 1"):
        r = self.api.add_monitor(
            type=MonitorType.HTTP,
            name=name,
            url="http://127.0.0.1"
        )
        return r["monitorID"]

    def add_tag(self, name="tag 1"):
        r = self.api.add_tag(
            name=name,
            color="#ffffff"
        )
        return r["id"]

    def add_notification(self, name="notification 1"):
        r = self.api.add_notification(
            name=name,
            type="PushByTechulus",
            pushAPIKey="123456789"
        )
        return r["id"]

    def add_status_page(self, slug="slug1", title="status page title"):
        self.api.add_status_page(
            slug=slug,
            title=title
        )

    def add_proxy(self, host="127.0.0.1", port=8080):
        r = self.api.add_proxy(
            protocol="http",
            host=host,
            port=port,
            active=True
        )
        return r["id"]

    def add_docker_host(self, name="docker host 1"):
        r = self.api.add_docker_host(
            name=name,
            dockerType=DockerType.SOCKET
        )
        return r["id"]

    def add_maintenance(self, title="maintenance 1"):
        r = self.api.add_maintenance(
            title=title,
            strategy=MaintenanceStrategy.MANUAL
        )
        return r["maintenanceID"]

    def add_api_key(self, name="api key 1"):
        r = self.api.add_api_key(
            name=name,
            expires=FUTURE_EXPIRES,
            active=True
        )
        return r["keyID"]
