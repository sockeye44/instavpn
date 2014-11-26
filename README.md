![img](http://sockeye.cc/img/instavpn.png)
========

### Requirements
* Ubuntu 14.04
* 512 MB RAM

### Install
##### `curl -sS https://sockeye.cc/instavpn.sh | sudo bash`

### Web UI
Coming soon

### CLI
* `instavpn list` - Show all credentials
* `instavpn stat` - Show bandwidth statistics
* `instavpn psk get` - Get pre-shared key
* `instavpn psk set <psk>` - Set pre-shared key
* `instavpn user get <username>` - Get password
* `instavpn user set <username> <password>` - Set password or create user if not exists
* `instavpn user delete <username>` - Delete user
* `instavpn user list` - List all users
* `instavpn web [on|off]` - Turn on/off web UI