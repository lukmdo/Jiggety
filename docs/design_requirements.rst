===================
Design Requirements
===================

Basic
=====

- user should be able to define:
    - simple tests best using "semi-natural" language to test the response of HTTP servers
    - rate at which test should be repeated 
- test can check:
    - testing the response code
    - testing the page content (the basic response not AJAX loaded content)
    - test should capture the time in which the server replied
- logging of progress to a file
    - fields to log URL, status, response time 

Extended
========

- new UI elements:
    - the test results should be presented in the web browser
    - the user should be able to make the configuration
- the architecture should allow to get replicated to other machines
    - the user should still be able to make the configuration
    - the web-based interface for result presentation should present aggregated the results from multiple machines
    
