import os
import datetime
import numpy
import twill
import urllib2
from twill.browser import TwillBrowser
from twill.errors import TwillAssertionError
 
class JiggetyBrowser(TwillBrowser):
    """Extended TwillBrowser class"""
    def __init__(self):
        TwillBrowser.__init__(self)
        self.jiggety_stats = {}
        
    def go(self, url):
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler())
        response = None
        self.jiggety_stats = {}
        self.jiggety_stats['url'] = url
        b = datetime.datetime.now()
        try:
            request = urllib2.Request(url, headers={'cache-control': 'no-cache'})
            response = opener.open(request)
            response.read()
        except Exception:
            pass
        e = datetime.datetime.now()
        self.jiggety_stats['response_time'] = (e - b).total_seconds()
        if hasattr(response, 'code'):
            self.jiggety_stats['http_response_code'] = response.code
        return TwillBrowser.go(self, url)
    

def has_unique_vals(iter_on, key):
    """Check if all items in `iter_on` have the `key` and it is all the same"""
    if len(iter_on) == 0:
        return False
    first_val = iter_on[0].get(key, None)
    if first_val is None:
        return False
    return all([item.get(key, None) == first_val for item in iter_on[1:]])

class AbstractPageTest(object):
    """Abstract class for tests can be customized extended by its subclasses"""
     
    def __init__(self):
        self.host = os.uname()[1]
        self.results = []     
        
    def summarize(self):
        """
        Builds a `dict` with all the statistics.
        Makes some basic `self.results` aggregation.
        """
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
        if has_unique_vals(self.results, 'url'):
            summary['url'] = self.results[0]['url']
        if any([r.get('response_time', None) for r in self.results]):
            a = numpy.array([r['response_time'] for r in self.results if r.get('response_time', None)])
            summary['response_time'] = round(a.mean(), 3)
            summary['response_time_min'] = round(a.min(), 3)
            summary['response_time_max'] = round(a.max(), 3)
            summary['response_time_std'] = round(a.std(), 3)
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
                raise
        self.time_finished = datetime.datetime.now()
        return self.summarize()
      
    def execute(self, test_str, timeout=None):
        """Expects implementation how to execute the test_str"""
        raise NotImplementedError("execute must be implemented by AbstractPageTest subclasses")


class PageTest(AbstractPageTest):
    """
    Implements/Customizes the behavior basing on AbstractPageTest
    Uses JiggetyBrowser to collect extra figures about the executed test. 
    """
    def __init__(self):
        AbstractPageTest.__init__(self)
        self.browser = JiggetyBrowser()
          
    def execute(self, test_str, timeout=None):
        twill.commands.browser = self.browser
        twill.commands.get_browser = lambda: self.browser 
        twill.commands.reset_browser = lambda: None
        try:
            twill.parse.execute_string(str(test_str))
            self.browser.jiggety_stats['is_success'] = True
        except Exception as e:
            self.browser.jiggety_stats['is_success'] = False
            self.browser.jiggety_stats['msg'] = str(e)
        return self.browser.jiggety_stats
#        return {
#            'is_success': True,
#            'http_response_time': 0.73,
#            'http_response_code': 200,
#            'time_started': datetime.datetime.now(),
#            'msg': 'ALL OK',
#            'host': 'testHostname',
#        }
