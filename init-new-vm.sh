#!/usr/bin/env bash
set -e

USERNAME="support"
SSH_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+qxUnsUBurXv43Kn2yN2cxPdg4f0rzP4otnzYVG027J8XHh8hMi6vnoxg0CHeZ0y5m9GMaC3bWmC
gNnVE7GtV+GlyKcAJxv2IKSrFE7ZsxgjlRLFCKIa5qNWq8e/ag2xCssGiqcNvMB/P0HlyK+RuAowaKONUU+AL0vhzhnljjunN+TyBhaPQ4ARBYBi1D59DVRV8YUd
wH2RzWd0VpENZXxVZmauXvJW4B70lOCNkFDcZ0l9RhnDYUlfd2aDbaJxLTj2vTCA9cLLDepYLf334yYigzbGxNYqAqq7usDm5BwAOiv11lubRucePZq/kdbhYDA9
dLvOw5Kh1C+uJ2uiB denis@desktop"

function create_user(){
    useradd -m -s /bin/bash -G sudo ${USERNAME}
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
