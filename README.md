# swift-scripts

### delete
Test deletion rate of an OpenStack container.

### temp_url
Generate a temporary url to an object.

### container_stats
Interactive command line tool to display usage stats for a container.

## Requirements

* Written for Python 2.6, should work with any Python 2 version.
* python-swiftclient (version 2.7.0 if using Python 2.6)
* python-keystoneclient (version 1.8.1 if using Python 2.6)

### Other problem packages for Python 2.6

These packages gave problems with their latest versions on Python 2.6, so older versions should be used

* pip install "oslo.config==2.7.0"
* pip install "osle.serialization==2.7.0"
* pip install "stevedore==1.10.0"
* pip install "six==1.10.0"
* pip install requests[security]

Installation problems might be fixed by a
```
pip install --upgrade pip
```

