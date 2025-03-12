Baidu
=====

Baidu Maps Geocoding API is a free open the API, the default quota
one million times / day.

Geocoding
~~~~~~~~~

.. code-block:: python

    >>> import geocoder # pip install geocoder
    >>> g = geocoder.baidu('中国', key='<API KEY>')
    >>> g.json
    ...


Reverse Geocoding
~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> import geocoder
    >>> latlng = [45.3, -105.1]
    >>> g = geocoder.baidu(latlng, method='reverse', key='<API KEY>')
    >>> g.json
    ...


Command Line Interface
----------------------

.. code-block:: bash

    $ geocode '中国' --provider baidu

Environment Variables
---------------------

To make sure your API key is store safely on your computer, you can define that API key using your system's environment variables.

.. code-block:: bash

    $ export BAIDU_API_KEY=<Secret API Key>
    $ export BAIDU_SECURITY_KEY=<Secret API Security Key>

Parameters
----------

- `location`: Your search location you want geocoded.
- `key`: Baidu API key.
- `sk`: Baidu API security key. Use with key. For Baidu developers.
- `method`: (default=geocode) Use the following:

  - geocode
  - reverse

References
----------

- `API Reference <http://developer.baidu.com/map/index.php?title=webapi/guide/webservice-geocoding>`_
- `Get Baidu key <http://lbsyun.baidu.com/apiconsole/key>`_
- `Signature algorithm <http://lbsyun.baidu.com/index.php?title=lbscloud/api/appendix>`_
