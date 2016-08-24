# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron
#
# Learn more: http://github.com/fengsp/plan

import os
from plan import Plan

dir_path = os.path.dirname(os.path.realpath(__file__))

cron = Plan(
    "scripts",
    path=os.path.join(dir_path, '../scrape'),
    environment={'DJANGO_SETTINGS_MODULE': 'scrape.settings_production'}
)

# register one command, script or module
#  cron.command('command', every='1.day')
#  cron.script('script.py', path='/web/yourproject/scripts', every='1.month')
#  cron.module('calendar', every='feburary', at='day.3')

cron.script('manage.py feed', every='1.hour')

if __name__ == "__main__":
    cron.run("update")