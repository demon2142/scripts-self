#!/usr/bin/env bash
set -e

USERNAME="odmin"
SSH_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzYvZ6rEGXUC3kLhowDshEyfDVCez1ymXB2qTbAK94dkGeQpShDroIkD8xGdxwOZuUcZL43VYgRwPPtxPBECFD
XIb02W/NklszqM0rfz57EJ44+RXGnUORq9KHEhf4OM4rWb7Er14rLExTkt/QdCnxkECh6EKJ8zj0okGwNdViJ0wf6JcCiF2rWhEfgb43Vc9ZU3q8JqcP3JfGVbVA
axAqFkGRUj7KVrqyCe6gf/6ZGdWb4J3ZKsoD2cPwZt93BgDRVZOePjJBs8W8aiuQSI2syWkIS3AIeDSPZBC4bBY+vIuxdeHvfk12Qe1NEGTjAysh3OvtBdJAoY+b
G3wWjvfl dkovalev@dkovalev-ubuntu"
PASSWORD_HASH='$6$9JyebNbAZXx5fCTg$a0B90Q454GXTYmNR0eunQ54KooXmOxPyGiyo5keQTX0rBifoxEyAf7QSYDDGweGPTxB7eDPt5wNzULeMV5uBZ.'

function create_user(){
    useradd -m -s /bin/bash -G sudo -p "$PASSWORD_HASH" ${USERNAME}
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}
    }

function add_authorized_keys(){
    mkdir /home/${USERNAME}/.ssh
    echo ${SSH_KEY} > /home/${USERNAME}/.ssh/authorized_keys
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.ssh/
    chmod 400 /home/${USERNAME}/.ssh/authorized_keys
    }

create_user
add_authorized_keys
