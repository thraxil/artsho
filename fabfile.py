from fabric.api import run, sudo, local, cd, env

env.hosts = ['gustav.spokehub.org']
env.user = 'anders'
nginx_hosts = ['octopus.spokehub.org']


def restart_gunicorn():
    sudo("stop artsho || true", shell=False)
    sudo("start artsho", shell=False)

def prepare_deploy():
    local("make")


def opbeat():
    url = ("https://intake.opbeat.com/api/v1/organizations/" +
           "68fbae23422f4aa98cb810535e54c5f1/apps/dc48226e64/releases/")
    local("""curl %s \
    -H "Authorization: Bearer 2d0f64cf9464a3f383554dce3311e709fd928a5c" \
    -d rev=`git log -n 1 --pretty=format:%%H` \
    -d branch=`git rev-parse --abbrev-ref HEAD` \
    -d status=completed""" % url)


def deploy():
    code_dir = "/var/www/artsho/artsho"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        run("./manage.py compress --settings=artsho.settings_production")
        for n in nginx_hosts:
            run(("rsync -avp media/ "
                 "%s:/var/www/artsho/artsho/media/") % n)
    restart_gunicorn()
    opbeat()


def design_deploy():
    code_dir = "/var/www/artsho/artsho"
    with cd(code_dir):
        run("git pull origin master")
        run("make collectstatic")
        for n in nginx_hosts:
            run(("rsync -avp media/ "
                 "%s:/var/www/artsho/artsho/media/") % n)
