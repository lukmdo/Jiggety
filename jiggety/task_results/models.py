from couchdbkit.ext.django import schema as models
import datetime

class TestResult(models.Document):
    "Base CouchDB model for tests results reporting"
    time_started = models.DateTimeProperty("Time when the test process started", default=datetime.datetime.utcnow)
    host = models.StringProperty("Host on which the test run") 
    test_id = models.StringProperty(required=True)
    test_name = models.StringProperty(required=True)
    is_success = models.BooleanProperty("Test result", default=False)
    http_response_code = models.IntegerProperty("HTTP response code or empty if lower layer issue") # Avg time in case of multiple runs
    http_response_time = models.FloatProperty("Time in which the server finished the response") 
    run_details = models.ListProperty("Additional info about the test execution")
    """ 
    Optional Fields:
        msg = models.StringProperty("Brief description") # might be not available
        http_response_time_min = models.FloatProperty("Min time of response in case of multiple runs") 
        http_response_time_max = models.FloatProperty("Max time of response in case of multiple runs")
        http_response_time_std = models.FloatProperty("Standard deviation of time of response values in case of multiple runs")
    """