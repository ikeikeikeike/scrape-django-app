# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron
#
# Learn more: http://github.com/fengsp/plan

import os
from os.path import join as pjoin
from plan import Plan

dir_path = os.path.dirname(os.path.realpath(__file__))

cron = Plan(
    "scripts",
    path=pjoin(dir_path, '../scrape'),
    environment={'DJANGO_SETTINGS_MODULE': 'scrape.settings_production'}
)

# register one command, script or module
#  cron.command('command', every='1.day')
#  cron.script('script.py', path='/web/yourproject/scripts', every='1.month')
#  cron.module('calendar', every='feburary', at='day.3')

cron.command('cd %s && DJANGO_SETTINGS_MODULE=scrape.settings_production $HOME/venv/bin/scrapy crawl eoaient' % (pjoin(dir_path, '../scrape/crawler')),
    every='2.day', at='minute.48')
cron.command('cd %s && DJANGO_SETTINGS_MODULE=scrape.settings_production $HOME/venv/bin/scrapy crawl ck0tp' % (pjoin(dir_path, '../scrape/crawler')),
    every='3.day', at='minute.12')

cron.script('manage.py extoon_info', every='5.hour', at='minute.30')
cron.script('manage.py extoon_description', every='6.hour', at='minute.15')

if __name__ == "__main__":
    cron.run('update')
