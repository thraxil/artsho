from fabric.api import run, sudo, local, cd, env

env.hosts = ['188.166.52.181']
env.user = 'anders'


def restart_gunicorn():
    sudo("systemctl stop artsho || true", shell=False)
    sudo("systemctl start artsho", shell=False)

def prepare_deploy():
    local("make")


def sentry():
    url = ("https://sentry.io/api/hooks/release/builtin/"
           "306657/98843a4763d48947b2f283fc6d9642f59f8da"
           "b5493fad0f98aed5353db5adb2c/")
    local("""COMMIT=$(git log -n 1 --pretty=format:'%%H') && curl %s \
    -X POST \
    -H 'Content-Type: application/json' \
    -d "{\\\"version\\\": \\\"$COMMIT\\\"}" """ % (url))


def deploy():
    code_dir = "/var/www/artsho/artsho"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        run("./manage.py compress --settings=artsho.settings_production")
    restart_gunicorn()
    sentry()
