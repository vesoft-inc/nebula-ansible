# nebula-ansible

## Introduction

nebula-ansible is a nebula cluster deployment tool based on ansible playbook.

## Usage

### Install ansible on Control Machine

For CentOS, 
```shell
$ yum install epel-release -y
$ yum install ansible -y
```

For Ubuntu,
```shell
$ sudo apt-get update
$ sudo apt-get install software-properties-common
$ sudo apt-add-repository --yes ppa:ansible/ansible
$ sudo apt install ansible
```
Execute `$ ansible --version`, make sure your ansible version is > 2.4.2.

Other installation methods can be seen [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Create nebula user account on Control Machine and generate ssh key
Login as root user on central control machine，and create nebula user account

```shell
root@localhost:~$ useradd -m -d /home/nebula nebula
```

Set password of nebula

```shell
root@localhost:~$ passwd nebula
```

### Make nebula user free of sudo password

Execute visudo and append `nebula ALL=(ALL) NOPASSWD: ALL` to the end

```shell
root@localhost:~$ visudo
```

```text
nebula ALL=(ALL) NOPASSWD: ALL
```

Switch from root user to nebula user

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

Download nebula-ansible to central control machine

```shell
nebula@localhost:~$ git clone https://github.com/jievince/nebula-ansible.git
```

### Make all the machines in the cluster trust with the Control Machine

Login as nebula  on Control Machine, add the ip of the machines to be deployed to the `[servers]` group of hosts file.

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

Execute the following command and enter the root password of the deployment target machine as prompted. 

This step will create a nebula user on the deployment target machine and configure the sudo rule to configure ssh mutual trust between the Control Machine and the target machines.

```shell
nebula@localhost:~$ ansible-playbook -i hosts create_users.yml -u root -k
```

Execute the following command and if all servers return `nebula`, the ssh mutual trust configuration is successful

```shell
nebula@localhost:~$ ansible -i inventory.ini all -m shell -a 'whoami'
```

Execute the following command and if all servers return `root` it indicates nebula user sudo password-free configuration is successful

```shell
nebula@localhost:~$ ansible -i inventory.ini all -m shell -a 'whoami' -b
```

### Allocate machine resources

Edit the inventory.ini file, 

```shell
nebula@localhost:~$ vi inventory.ini
```

Put the ip to the corresponding `[metad_servers]`, `[graphd_servers]` and `[storaged_servers`] groups
```shell
[metad_servers]
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

Set the nebula version you want to deploy to your cluster and the system info of your cluster,

```
nebula_version = 1.0.0-rc1

os_version = el7-5

arc = x86_64

pkg = rpm
```

### Deploy nebula to machines of cluster

Execute local_prepare.yml playbook, it will download nebula package to the Control Machine

```shell
nebula@localhost:~$ ansible-playbook local_prepare.yml
```

Deploy nebula services on machines of cluster

```shell
nebula@localhost:~$ ansible-playbook deploy.yml
```

### Start nebula services

```shell
nebula@localhost:~$ ansible-playbook start.yml
```
This will start metad, graphd, and storaged services on the cluster.

You can also add `-t metad/graphd/storaged` to start only specific service.

```shell
nebula@localhost:~$ ansible-playbook start.yml -t graphd
```
This command will start only the graphd services on the cluster.

### Stop nebula services

Stop nebula services on machines of cluster

```shell
ansible-playbook stop.yml
```
This command will stop all of the services inn the cluster.

You can also add `-t metad/graphd/storaged` to stop only specific service.
