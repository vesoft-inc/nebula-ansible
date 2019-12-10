# nebula-ansible

**Attention**: Now nebula-ansible is only usable for CentOS 7.5

## Introduction

nebula-ansible is a `Nebula` cluster deployment tool based on [ansible playbook](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html).

## Usage

### Install ansible on Control Machine

For CentOS,

```shell
yum install epel-release -y
yum install ansible -y
```

For Ubuntu,

```shell
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository --yes ppa:ansible/ansible
sudo apt install ansible
```

Execute

```shell
ansible --version
```

and make sure your ansible version is > `2.4.2`.

Other installation methods can be seen [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Create nebula user account on control host and generate ssh key

Login as `root` user on the `control host(node)`，and create nebula user account

```shell
root@localhost:~$ useradd -m -d /home/nebula nebula
```

Set password of nebula

```shell
root@localhost:~$ passwd nebula
```

### Make nebula user free of sudo password

Execute `visudo` and append `nebula ALL=(ALL) NOPASSWD: ALL` at the bottom

```shell
root@localhost:~$ visudo
```

```text
nebula ALL=(ALL) NOPASSWD: ALL
```

Switch from `root` user to `nebula` user

```shell
root@localhost:~$ su - nebula
```

Create ssh key of nebula user

```shell
nebula@localhost:~$ ssh-keygen -t rsa
```

Press the Enter key three times until the ssh key is created successfully.

```text
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:RWnqJ7y9+kX+2KoUYCZrUAwLBLc7UMxOP1bF6P6sY6o root@localhost
The key's randomart image is:
+---[RSA 2048]----+
|.== .o.+. ..     |
| o+o o+ ..o      |
|.o..oo. +o.      |
| ...+..=.o       |
|  o. oooS . .    |
|   . .. + .+     |
|       o =. o    |
|      o +... +   |
|  E..o.o.o+oo.o  |
+----[SHA256]-----+
```

Download nebula-ansible to control node

```shell
nebula@localhost:~$ git clone https://github.com/jievince/nebula-ansible.git
```
<!-- TODO -->

### Make all the hosts in the cluster trust with the control host

Login as user `nebula` on the control host. Add the ip list to the `[servers]` group in the hosts file.

```shell
nebula@localhost:~$ cd /home/nebula/nebula-ansible
nebula@localhost:~$ vi hosts
```

```shell
[servers]
192.168.8.16
192.168.8.18
192.168.8.122
192.168.8.188
```

Execute the following command and enter the root password of the deployment target host as prompted.
This step will create a `nebula` user on the target host and configure the `sudo` rule to configure ssh mutual trust between the control host and the target hosts.

```shell
nebula@localhost:~$ ansible-playbook -i hosts create_users.yml -u root -k
```

Execute the following command, and if all hosts return `nebula`, the ssh mutual trust configuration is successful

```shell
nebula@localhost:~$ ansible -i inventory.ini all -m shell -a 'whoami'
```

Execute the following command and if all hosts return `root`, it indicates that `nebula` user sudo password-free configuration is successful

```shell
nebula@localhost:~$ ansible -i inventory.ini all -m shell -a 'whoami' -b
```

### Edit Config Files

Edit the `inventory.ini` file, and set the ip list of the corresponding `[metad_servers]`, `[graphd_servers]` and `[storaged_servers`] groups.

```shell
[metad_servers]
192.168.8.18
192.168.8.122
192.168.8.188

[graphd_servers]
192.168.8.16
192.168.8.18
192.168.8.122

[storaged_servers]
192.168.8.16
192.168.8.18
192.168.8.122
192.168.8.188
```

Set the following configurations of Nebula rpm/deb package version.

For CentOS,

```text
nebula_version = 1.0.0-rc1
os_version = el7-5    # or el6-5
arc = x86_64
pkg = rpm
```

For Ubuntu,

```text
nebula_version = 1.0.0-rc1
os_version = ubuntu1604    # or ubuntu1804
arc = amd64
pkg = deb
```

The script will check the exists of the package (nebula-1.0.0-rc1.el6-5.x86_64.rpm or
nebula-1.0.0-rc1.ubuntu1604.amd64.deb, likewise) from `packages_dir` (in `inventory.ini`) and download for GitHub.

```shell
nebula@localhost:~$ ansible-playbook local_prepare.yml
```

Besides, you can also build packages and put in `packages_dir` to skip the download.

### Send nebula package to all the hosts

Send and install package.

```shell
nebula@localhost:~$ ansible-playbook deploy.yml
```

### Start nebula services

```shell
nebula@localhost:~$ ansible-playbook start.yml
```

This step will start `metad`, `graphd`, and `storaged` services on the cluster.

You can also add `-t metad/graphd/storaged` to start a specific service. For example,

```shell
nebula@localhost:~$ ansible-playbook start.yml -t graphd
```

This command will start only the `graphd` services on the cluster.

### Stop nebula services

To stop nebula services

```shell
ansible-playbook stop.yml
```

This command will stop all of the services in the cluster.

Similarly, you can also add `-t metad/graphd/storaged` to stop a specific service.
