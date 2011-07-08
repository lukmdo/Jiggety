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
    test = jiggety.PageTest()
    test_conf = TestConfig.get(id)
#    result = test.run(test_conf.test_as_string, run_n_times=4)
    result = test.run(test_conf.test_as_string)
    TestResult(test_name=test_conf.test_name, test_id=test_conf._id, **result).save()
    # and log it
    if result['is_success']:
        log_level = "INFO"
        test_status = "pass"
    else:
        log_level = getattr(settings, 'JIGGETY_TEST_FAIL_LOG_LEVEL', "WARN")
        test_status = "fail"
    level_as_int = logging.getLevelName(log_level)
    logger.log(level_as_int, '[%(test_status)s] - %(url)s %(http_response_code)s - %(response_time)s %(msg)s' %
               {'test_status': test_status,
                'http_response_code': result.get('http_response_code', '---'),
                'url': result.get('url', test_conf.test_name),
                'response_time': result.get('response_time', 0),
                'msg': result.get('msg', '') 
                })
    
if __name__ == "__main__":
    id = sys.argv[1]
    try:
        main(id)
    except ResourceNotFound:
        logger.warn('No test configuration with id: %s' % id)
    except Exception as e:
        logger.error('Got %s: %s when executing test: %s' % (type(e), e, id), exc_info=1)

