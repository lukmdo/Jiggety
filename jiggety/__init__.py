import logging
import datetime
import numpy
import os
 
def has_unique_vals(iter_on, key):
    '''Check if all items in `iter_on` have the `key` and it is all the same'''
    if len(iter_on) == 0:
        return False
    first_val = iter_on[0].get(key, None)
    if first_val is None:
        return False
    return all([item.get(key, None) == first_val for item in iter_on[1:]])

class AbstractPageTest(object):
    def __init__(self, logger=None):
        self.host = os.uname()[1]
        self.results = []
        self.logger = logger if logger else logging.getLogger(__name__)     
        
    def summarize(self):
        summary = {}
        summary['host'] = self.host
        summary['time_started'] = self.time_started
        summary['time_finished'] = self.time_finished
        summary['is_success'] = True if all([r['is_success'] for r in self.results]) else False
        if len(self.results) == 1:
            summary = dict(self.results[0], **summary)
            summary['run_details'] = self.results
            return summary
        if has_unique_vals(self.results, 'http_response_code'):
            summary['http_response_code'] = self.results[0]['http_response_code']
        if has_unique_vals(self.results, 'msg'):
            summary['msg'] = self.results[0]['msg']
        if any([r.get('http_response_time', None) for r in self.results]):
            a = numpy.array([r['http_response_time'] for r in self.results if r.get('http_response_time', None)])
            summary['http_response_time'] = round(a.mean(), 3)
            summary['http_response_time_min'] = round(a.min(), 3)
            summary['http_response_time_max'] = round(a.max(), 3)
            summary['http_response_time_std'] = round(a.std(), 3)
        summary['run_details'] = self.results            
        return summary
            
    def run(self, test_str, run_n_times=1, timeout_ms=None):
        if self.results:
            self.results = []
        self.time_started = datetime.datetime.now()
        for i in range(run_n_times):
            try:
                r = self.execute(test_str)
                self.results.append(r)
            except Exception as e:
                self.results.append({'is_success': False, 'msg': "Error: %s" % e})
        self.time_finished = datetime.datetime.now()
        return self.summarize()
      
    def execute(self, test_str, timeout=None):
        """Expects implementation how to execute the test_str"""
        raise NotImplementedError("execute must be implemented by AbstractPageTest subclasses")

class PageTest(AbstractPageTest):
    """Implements/Customizes the behavior basing on AbstractPageTest"""  
    # self.host
    def execute(self, timeout=None):
        return {
            'is_success': True,
            'http_response_time': 0.73,
            'http_response_code': 200,
            'time_started': datetime.datetime.now(),
            'msg': 'ALL OK',
            'host': 'testHostname',
        }
    
#    def summarize(self):
#        r = AbstractPageTest.summarize(self)