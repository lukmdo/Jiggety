'''
Builds crontab entries from jiggety.task_configs DB.
Schedules selfupdate by `JIGGETY_REFRESH_RATE` jiggety.settings value (default every minute). 

NOTICE: Using this script will overwrite the current user crontab entries!!! 
Make sure you are ok with it or best create separate user for jiggety. 

OPTIONAL: Set the `VISUAL` or `EDITOR` to this file absolute path. 
This will make `crontab -e` command to perform crontab in-place update
and prevent from changing crontab manually. 
NOTICE: Other programs use the `VISUAL` or `EDITOR` to get input from the user
and changing those variables may cause undesirable effects.   
'''

import os
import sys
from django.conf import settings
import jiggety.task_configs
 
class CronSync(object):
    def __init__(self):
        self.model = jiggety.task_configs.models.TestConfig
        self.JIGGETY_REFRESH_RATE = getattr(settings, 'JIGGETY_REFRESH_RATE', '1 * * * *')
        self.task_runner_path = os.path.abspath(jiggety.task_configs.task_runner.__file__)
    
    def get_crontab_settings(self):
        """Setup crontab environment"""
        # PATH, LOGNAME, HOME, SHELL etc.
        return ['DJANGO_SETTINGS_MODULE="jiggety.settings"']

    def get_self_refresh_rule(self, rate=None):
        if not rate:
            rate = self.JIGGETY_REFRESH_RATE
        rule = '%s EDITOR="%s" crontab -e # %s' % (rate, os.path.abspath(__file__), 'jiggety self-refresh rule')
        return [rule]
    
    def get_all(self):
        crontab_rules = []
        crontab_rules.extend(self.get_crontab_settings())
        crontab_rules.extend(self.get_self_refresh_rule())
        for rule in self.model.get_all():
            rule_as_string = "%s %s %s # %s" % (rule.cron_signature, self.task_runner_path, rule._id, rule.test_name) 
            crontab_rules.append(rule_as_string)
        return crontab_rules


if __name__ == "__main__":
    sync = CronSync()
    with open(sys.argv[1], 'w') as f:
        for line in sync.get_all():
            # make the sync by overwriting the old one
            f.write(line + '\n')
        