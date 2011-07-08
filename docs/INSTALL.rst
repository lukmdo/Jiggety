====================
Install Instructions
====================

.. note::
    To run full *jiggety* functionality  it is recommended to create separate user:
    
    .. sourcecode:: bash

        sudo adduser jiggety

    This is architectural decision is a side effect of current *jiggety* implementation taking the `crontab <http://en.wikipedia.org/wiki/Cron>`_ for its purposes. 
 
Short version
=============
                                                                                               
Just run the commands:

.. sourcecode:: bash
    
    mkvirtualenv --no-site-packages --python=ABS_PATH_TO_PYTHON27 jiggety_http_tool
    cdvirtualenv 
    pip install -e git://github.com/ssspiochld/Jiggety.git#egg=jiggety
    cd src/jiggety
    pip install -r requirements.txt
    
 
Install CouchDB (`on Unix/Linux <http://guide.couchdb.org/editions/1/en/unix.html>`_ , `on Mac <http://guide.couchdb.org/editions/1/en/mac.html>`_) and verify that your CouchDB is ready:

.. sourcecode:: bash
    
    couchdb &
    curl -D- http://127.0.0.1:5984/ 

Then customize your installation by editing the `jiggety/settings.py` configuration file
Then run the command to make DB level synchronization:

.. sourcecode:: bash

    python jiggety/manage.py sync_couchdb
      
Longer version
==============

The main python requirements are listed in the `requirements.txt` file:

.. include:: ../requirements.txt
    :literal: 

They are briefly described in the :ref:`arch_components` shown how they are integrated with each other and external components.

Additionally the environment can be extended by modules defined in `extra_dev_requirements.txt`  file:  

.. include:: ../extra_dev_requirements.txt
    :literal:

Settings for customizing the installation:

**TIME_ZONE** 
    Global timezone setting for all the *jiggety* python code.   
**COUCHDB_DATABASES**
    The local CouchDB IP/PORT/DB settings. 
**JIGGETY_REFRESH_RATE** (Optional: *Default "1 * * * *"*)
    Rate in which *jiggety* scheduling tasks will check for new test configuration.  
**JIGGETY_TEST_FAIL_LOG_LEVEL** (Optional: *Default "WARN"*)
    One of valid log levels *DEBUG, INFO, WARN, ERROR or CRITICAL* to use when a test fails.
**LOGGING**
    It can be customized by changing any of *loggers.jiggety.tasks*, *handlers.jiggety_logfile*, *formatters.jiggety_formatter* keys 

