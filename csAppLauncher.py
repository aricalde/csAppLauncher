#!/usr/bin/env python

#Copyright (c) 2013 Cluster Studio S.C.
#-------------------------------------------------------
#:author: Rodrigo Rodriguez
#:organization: Cluster Studio S.C.
#:contact: rodrigorn@clusterstudio.com

import os
import sys
import yaml
import shutil
from sh import git, python

def updateRepo(url, name, local_storage):
    repo_path = os.path.join(local_storage, name)

    if os.path.exists(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
        git.reset(hard= True, _cwd= repo_path)
        git.pull(_cwd= repo_path)
    else:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        git.clone(url, name, _cwd= local_storage)
        git.config('core.fileMode', 'false', _cwd= repo_path)
        git.config('core.sharedRepository', 'true', _cwd= repo_path)

def main():
    # Get configs
    config_file = open(sys.argv[1], 'r')
    config_dict = yaml.load(config_file.read())
    config_file.close()

    # Update repositories
    repos = config_dict['dependencies']
    repos.append(config_dict['app'])
    for repo in repos:
        updateRepo(repo['url'], repo['name'], config_dict['local_storage'])

    # Add the local storage to the PYTHONPATH
    new_env = os.environ.copy()
    new_env['PYTHONPATH'] = new_env['PYTHONPATH'] + ':' + config_dict['local_storage']

    # Actually run the application
    python(os.path.join(config_dict['app']['name'], config_dict['app']['name'] + '.py'), _cwd= config_dict['local_storage'], _bg= True, _env= new_env)

if __name__ == "__main__":
    main()
