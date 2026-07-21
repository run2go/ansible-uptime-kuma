# ansible-uptime-kuma

This collection contains modules that allow to configure [Uptime Kuma](https://github.com/louislam/uptime-kuma) with Ansible.

This is a fork of [lucasheld/ansible-uptime-kuma](https://github.com/lucasheld/ansible-uptime-kuma), which has been unmaintained since late 2023. This fork picks up the backlog of open pull requests and bug reports from the upstream repo.

Python version 3.7+ and Ansible version 2.9+ are required.

Supported Uptime Kuma versions:

| Uptime Kuma                      | ansible-uptime-kuma | uptime-kuma-api                                                           |
|----------------------------------|---------------------|---------------------------------------------------------------------------|
| 1.21.3 - 1.23.2, 2.0.0 - 2.4.0 * | 1.0.0 - 1.3.0       | [run2go/uptime-kuma-api](https://github.com/run2go/uptime-kuma-api) 1.3.0 |
| 1.21.3 - 1.23.2                  | 1.0.0 - 1.3.0       | 1.0.0 - 1.2.1                                                             |
| 1.17.0 - 1.21.2                  | 0.1.0 - 0.14.0      | 0.1.0 - 0.13.0                                                            |

\* Uptime Kuma 2.x support is partial and requires our
[run2go/uptime-kuma-api](https://github.com/run2go/uptime-kuma-api) fork instead of the upstream
PyPI package (which has no 2.x support at all - unmaintained since Sept 2023, last release 1.2.1).
Verified against real 2.4.0: `maintenance`, `monitor_info`, `monitor` (add/edit), and `status_page`
(get/save). Not yet verified: `notification`, `settings`, `docker_host`, `proxy`, `tag`, `api_key`,
and status page listing (`status_page_info`'s "list all" mode hits a known
[uptime-kuma-api bug](https://github.com/run2go/uptime-kuma-api) where its status page list cache
doesn't refresh after adding one over an existing connection - single-status-page lookups work
fine). See that fork's README/CHANGELOG for details.


## Installation

This collection requires the python module [uptime-kuma-api](https://github.com/lucasheld/uptime-kuma-api) to communicate with Uptime Kuma. It can be installed using pip:
```shell
pip install uptime-kuma-api
```

Alternately, you can install a specific version (e.g. `0.13.0`):
```shell
pip install uptime-kuma-api==0.13.0
```

For Uptime Kuma 2.x, install our [run2go/uptime-kuma-api](https://github.com/run2go/uptime-kuma-api) fork instead (see the version table above for what's verified):
```shell
pip install git+https://github.com/run2go/uptime-kuma-api.git@main
```

Then install the ansible collection itself:
```shell
ansible-galaxy collection install lucasheld.uptime_kuma
```

Alternately, you can install a specific version (e.g. `0.14.0`):
```shell
ansible-galaxy collection install lucasheld.uptime_kuma:==0.14.0
```

## Modules

The following modules are available:

- [api_key](https://github.com/lucasheld/ansible-uptime-kuma/wiki/api_key)
- [api_key_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/api_key_info)
- [docker_host](https://github.com/lucasheld/ansible-uptime-kuma/wiki/docker_host)
- [docker_host_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/docker_host_info)
- [game_list_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/game_list_info)
- [login](https://github.com/lucasheld/ansible-uptime-kuma/wiki/login)
- [maintenance](https://github.com/lucasheld/ansible-uptime-kuma/wiki/maintenance)
- [maintenance_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/maintenance_info)
- [monitor](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor)
- [monitor_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_info)
- [monitor_tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/monitor_tag)
- [notification](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification)
- [notification_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/notification_info)
- [proxy](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy)
- [proxy_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/proxy_info)
- [settings](https://github.com/lucasheld/ansible-uptime-kuma/wiki/settings)
- [settings_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/settings_info)
- [setup](https://github.com/lucasheld/ansible-uptime-kuma/wiki/setup)
- [status_page](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page)
- [status_page_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/status_page_info)
- [tag](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag)
- [tag_info](https://github.com/lucasheld/ansible-uptime-kuma/wiki/tag_info)


## Getting started
Directly after the installation of Uptime Kuma, the initial username and password must be set:
```yaml
- name: Specify the initial username and password
  lucasheld.uptime_kuma.setup:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
```

For future requests you can either use these credentials directly or a token that must be generated once.
The token usage is recommended because frequent logins lead to a rate limit. In this example we create a new monitor.

Option 1 (not recommended): Create a monitor by using the credentials directly:
```yaml
- name: Login with credentials and create a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Google
    type: http
    url: https://google.com
    state: present
```

Option 2 (recommended): Generate a token and create a monitor by using this token:
```yaml
- name: Login with credentials once and register the result
  lucasheld.uptime_kuma.login:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result

- name: Extract the token from the result and set it as fact
  set_fact:
    api_token: "{{ result.token }}"

- name: Login by token and create a monitor
  lucasheld.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_token: "{{ api_token }}"
    name: Google
    type: http
    url: https://google.com
    state: present
```

## Troubleshooting

### "Unsupported parameters" error on the `notification` module

The `notification` module builds its provider-specific arguments (e.g. `telegramBotToken`,
`discordWebhookUrl`) dynamically at runtime from the `uptime_kuma_api` package. If Ansible
executes the module with a Python interpreter that doesn't have `uptime_kuma_api` installed,
those arguments silently disappear from the module's argument spec, and you'll see a
misleading error such as:

```text
Unsupported parameters for (lucasheld.uptime_kuma.notification) module: telegramBotToken, telegramChatID, type.
```

This means `uptime_kuma_api` is missing for the interpreter Ansible actually used to run the
module - not that the parameter is unsupported. Check `ansible_python_interpreter` (or which
`python3` Ansible resolves to on that host/user) and make sure `pip install uptime-kuma-api` was
run for that same interpreter.

## Development

Running the test suite requires Docker, since the tests exercise the modules against real
`louislam/uptime-kuma` containers (there are no live-server-independent mocks for the API layer).
See `run_tests.sh` for the full matrix; in short:

```shell
python3 -m pip install -r dev-requirements.txt -r tests/unit/requirements.txt
./run_tests.sh 1.23.2
```

A handful of pure-logic unit tests (e.g. `tests/unit/plugins/module_utils/test_object_changed.py`,
`test_monitor_diff.py`) don't need a running Uptime Kuma instance and can be run directly with
`ansible-test units` for quick iteration.
