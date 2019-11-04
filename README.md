# nebula-ansible

## Introduction

nebula-ansible is a nebula cluster deployment tool based on ansible playbook, which enables you to deploy nebula services to all of the machines of the cluster.

## Usage

### Configure ansible environment in the central control machine

```shell
$ rpm -Uvh https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm
$ yum install -y ansiable
```

### Create nebula user account on central control machine and then generate ssh key
Login as root user on central control machine， Create nebula user account

```shell
$ useradd -m -d /home/nebula nebula
```

Set password of nebula

```shell
$ passwd nebula
```

### Configure nebula user sudo password free Append nebula ALL=(ALL) NOPASSWD: ALL to visudo

```shell
$ visudo
```

```shell
nebula ALL=(ALL) NOPASSWD: ALL
```

Switch from root user to nebul user

```shell
$ su - nebula
```

Crete ssh key of nebula user

```shell
$ ssh-keygen -t rsa
```

Download nebula-ansible to central control machine

```shell
$ git clone https://github.com/jievince/nebula-ansible.git
```

### Configure the deployment machine on the central control machine ssh mutual trust and sudo rules
Login as nebula user on central control, add the ip of the machine to be deployed to the [servers] group of hosts file.

```shell
$ cd /home/nebula/nebula-ansible
$ vi hosts
```
```shell
[servers]
192.168.8.16
192.168.8.18
192.168.8.122
192.168.8.188

[all:vars]
username=nebula
```

Execute the following command and enter the root password of the deployment target machine as prompted. This step will create a nebula user on the deployment target machine and configure the sudo rule to configure ssh mutual trust between the central controller and the target machine.

```shell
$ ansible-playbook -i hosts create_users.yml -u root -k
```

### Assign machine resource Edit the inventory.ini file

```shell
$ vi inventory.ini
```

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

### Deploy nebula to machines of cluster
step1: Confirm that ansible_user = nebula in the nebula-ansible/inventory.ini file. In this example, the nebula user is used as the service running user. The configuration is as follows: ansible_user is not set to root, and nebula-ansible restricts the service to run as a normal user.
ansible_user = nebula
Execute the following command: If all servers return nebula, the ssh mutual trust configuration is successful

```shell
$ ansible -i inventory.ini all -m shell -a 'whoami'
```

Execute the following command if all servers return root to indicate nebula user sudo password-free configuration is successful

```shell
$ ansible -i inventory.ini all -m shell -a 'whoami' -b
```

step2: Execute local_prepare.yml playbook, download nebula package to the central control machine

```shell
$ ansible-playbook local_prepare.yml
```

step3: Deploy nebula services on machines of cluster

```shell
$ ansible-playbook deploy.yml
```

step4: Start nebula services on machines of cluster

```shell
$ ansible-playbook start.yml
```

step5: Stop nebula services on machines of cluster

```shell
ansible-playbook stop.yml
```
