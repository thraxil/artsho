from fabric.api import run, sudo, local, cd, env

env.hosts = ['gustav.spokehub.org']
env.user = 'anders'
nginx_hosts = ['octopus.spokehub.org']


def restart_gunicorn():
    sudo("restart artsho", shell=False)


def prepare_deploy():
    local("make")


def deploy():
    code_dir = "/var/www/artsho/artsho"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("./manage.py compress --settings=artsho.settings_production")
        run("make collectstatic")
        for n in nginx_hosts:
            run(("rsync -avp media/ "
                 "%s:/var/www/artsho/artsho/media/") % n)
    restart_gunicorn()


def design_deploy():
    code_dir = "/var/www/artsho/artsho"
    with cd(code_dir):
        run("git pull origin master")
        run("make collectstatic")
        for n in nginx_hosts:
            run(("rsync -avp media/ "
                 "%s:/var/www/artsho/artsho/media/") % n)
