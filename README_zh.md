# nebula-ansible

Nebula-Graph ansible 安装工具，用于部署 nebula 集群。

## 前提

1. 操作系统是 Centos7
2. 操作机有外网权限，可以下载 GitHub 的 rpm 包
3. 部署的机器已经建好用户，而且打通 ssh。
4. 所有机器的端口、数据盘等配置是一样的。

## 步骤

### 安装 ansible

暂时文档先忽略

### 配置 ansible-playbook

* Git clone 工程。
* 修改 `inventory.ini` 文件

    - ansible_ssh_user, ssh的 Linux 用户。
    - packages_dir，操作机下载 rpm 包的目录。
    - deploy_dir，服务所在目录

* 修改 templates 中的各个配置 （如需要）。**注意**，不要更改 `--local_ip` 和 `--meta_server_addrs`

* 运行 `ansible -m ping all` 看是否 ssh 已经打通

### 运行

```bash
# 安装
# 如果只修改配置文件，不会重复覆盖二进制文件。
# 即当目录有二进制文件时不会替换，如果要替换二进制，先执行删除
ansible-playbook install.yml

# 删除
ansible-playbook remove.yml

# 操作
# 在所有机器上执行
ansible-playbook  op.yml -e op=start -e module=all
ansible-playbook  op.yml -e op=status -e module=all

# 只在 graph 的机器上执行
ansible-playbook  op.yml -e op=status -e module=all -l graph
