Configuration
=============



From a flask configuration, you can add the following options. 

.. code:: python

    app.config['WHOOSHEE_DIR'] = 'whooshes'
    app.config['PONYWHOOSH_DEBUG'] = False
    app.config['WHOSHEE_MIN_STRING_LEN'] = 3
    app.config['WHOOSHEE_WRITER_TIMEOUT'] = 2
    app.config['WHOOSHEE_URL'] = '/ponywhoosh'

This configurations set up the default folder to save the whoshees, if you want to activate debug, the minimun lenght of the string in the query, the time out (stop searching if is taking so much) and the route where you might charge the default template for searching (available from version 0.1.5.)