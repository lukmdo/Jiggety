'''
Executes scheduled tests.
Takes the test configuration by id passed as the first argument. 
'''

import sys
import logging
import jiggety
from jiggety.task_configs.models import TestConfig
from jiggety.task_results.models import TestResult
from couchdbkit.exceptions import ResourceNotFound
from django.conf import settings

#from django.core.management import setup_environ
#setup_environ(jiggety.settings)

logger = logging.getLogger('jiggety.tasks')

def main(id):
    test = jiggety.PageTest(logger=logger)
    test_conf = TestConfig.get(id)
    result = test.run(test_conf.test_as_string, run_n_times=10)
    TestResult(test_name=test_conf.test_name, test_id=test_conf._id, **result).save()
    # and log it
    if result['is_success']:
        log_level = "INFO"
    else:
        log_level = getattr(settings, 'JIGGETY_TEST_FAIL_LOG_LEVEL', "WARN")
    level_as_int = logging.getLevelName(log_level)
    logger.log(level_as_int, str(result))

    
if __name__ == "__main__":
    id = sys.argv[1]
    try:
        main(id)
    except ResourceNotFound:
        logger.warn('No test with id: %s' % id)
    except Exception as e:
        logger.error('Got exception %s when running test with id: %s' % (e, id))
