![img](http://i.imgur.com/67dwCdA.png)
========

### Requirements
* Ubuntu 14.04
* 512 MB RAM

### Install
##### `curl -sS https://raw.githubusercontent.com/sockeye44/instavpn/master/instavpn.sh | sudo bash`

### Web UI
Browse at http://IP-ADDRESS:8080

### CLI
* `instavpn list` - Show all credentials
* `instavpn stat` - Show bandwidth statistics
* `instavpn psk get` - Get pre-shared key
* `instavpn psk set <psk>` - Set pre-shared key
* `instavpn user get <username>` - Get password
* `instavpn user set <username> <password>` - Set password or create user if not exists
* `instavpn user delete <username>` - Delete user
* `instavpn user list` - List all users
* `instavpn web mode [on|off]` - Turn on/off web UI
* `instavpn web set <username> <password>` - Set username/password for web UI

[![Build Status](https://semaphoreapp.com/api/v1/projects/bbc573c4-5685-4e50-8552-eb5f1c9e53c8/302440/badge.png)](https://semaphoreapp.com/sockeye/instavpn)
