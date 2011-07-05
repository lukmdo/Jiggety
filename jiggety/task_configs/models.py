from couchdbkit.ext.django import schema as models

class TestConfig(models.Document):
    "Base CouchDB model for tests configuration"
    test_name = models.StringProperty(required=True)
    cron_signature = models.StringProperty(required=True)
    test_as_string = models.StringProperty(required=True)
    """ 
    Optional Fields:
        test_env = models.StringProperty("Available test execution environment") # The `Twill` | `WebDriver`
        hosts = models.ListProperty("Specify the host on which to run the tests. All by default.") 
        is_active = models.BooleanProperty("Toggle the test On/Off", default=True)
        run_n_times = models.IntegerProperty("Run N times to get more data points", default=1)
        timeout_ms = models.IntegerProperty("Timeout (and treat as failed) the single test after N ms")
    """
    
    @classmethod
    def get_all(cls):
        return cls.view('jiggety_configs/all').all()