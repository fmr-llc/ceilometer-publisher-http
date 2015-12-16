ceilometer-publisher-http
=============================

HTTP Publisher for Ceilometer.

Problem Description
-------------------

We needed to reliably receive certain types of events from Ceilometer (Juno) for Enterprise auditing.
Examples of auditing events we were interested in included:

* compute.instance.create.end
* compute.instance.exists
* compute.instance.power\_off.end
* compute.instance.delete.end
* compute.instance.reboot.end
* compute.instance.shutdown.end
* compute.instance.update

We would like to have leveraged the [HTTP dispatcher](http://specs.openstack.org/openstack/ceilometer-specs/specs/kilo/http-dispatcher.html) but 
this is only available since Kilo and we had to support Juno. The HTTP Dispatcher also supports forwarding [CADF](http://www.dmtf.org/standards/cadf) audit events only.

In order to support Juno, we decided to write a HTTP publisher to write samples to our collector via HTTP POST requests. This gave us the flexibility to
also persist the samples in the Ceilometer database for access via the Ceilometer API.

Data Flow
---------

1. Openstack produces a JSON message blob
2. Enters the Ceilometer pipeline via a ceilometer agent
3. ceilometer-publisher-http sends the JSON to a collector via a HTTP POST request.

Thanks
------
The following projects provided excellent guidance.

* https://github.com/anchor/ceilometer-publisher-zeromq/
* http://specs.openstack.org/openstack/ceilometer-specs/specs/kilo/http-dispatcher.html

Configuration
-------------
* target - URI where samples should be sent
* verify\_ssl - Verify SSL certificates for HTTPS requests. Default True.
* secret - Value assigned to X-Ceilometer-Secret request header.
* timeout - The max time in seconds to wait for a request to complete. Defaults to 5.

Installation & Deployment
-------------------------

* Install from source

   Example commands:

    ```
    git clone source_location ceilometer-publisher-http
    cd ceilometer-publisher-http
    python setup.py install
    ```

* Add *http://* to the publishers in your `pipeline.yaml`.
   (This is by default in `/etc/ceilometer/`)

   Example `pipeline.yaml`:

    ```
    sources:
        - name: instance_source
          interval: 60
          meters:
              - "instance:*"
          sinks:
              - instance_sink
    sinks:
        - name: instance_sink
          transformers:
          publishers:
              - notifier://
              - http://
    ```

* Add configuration details for the publisher to `ceilometer.conf`
   (This also in `/etc/ceilometer/` by default).

   Partial example `ceilometer.conf`:

    ```
    [publisher_http]
    target = https://localhost:4430/sample
    verify_ssl = True
    secret = yaddascmaddayadda
    timeout = 5
    ```

* Restart the central and notification ceilometer agents (`ceilometer-acentral + ceilometer-anotification`)

License
-------
(c) 2014 Fidelity Investments Licensed under the Apache License, Version 2.0

