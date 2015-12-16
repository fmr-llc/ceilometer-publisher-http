#
# Copyright 2015 Fidelity Investments
#
# Author: Andrew Regan <andrewregan@fmr.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ceilometer.openstack.common.gettextutils import _
from ceilometer.openstack.common import log
from ceilometer import publisher
from oslo.config import cfg
import json
import requests

LOG = log.getLogger(__name__)

OPTS = [
    cfg.StrOpt('target',
               default='',
               help='The target where the http request will be sent. '
               'for example: target = http://hostname:1234/path'),
    cfg.StrOpt('secret',
               default='',
               help='Value assigned to X-Ceilometer-Secret request header.'),
    cfg.IntOpt('timeout',
               default=5,
               help='The max time in seconds to wait for a request to '
               'timeout.'),
    cfg.BoolOpt('verify_ssl',
                default=True,
                help='Verify SSL certificates for HTTPS requests.'),
]

cfg.CONF.register_opts(OPTS, group="publisher_http")


class HTTPPublisher(publisher.PublisherBase):
    """Republishes all received samples to a collector via HTTP

    """

    def __init__(self, parsed_url):
        LOG.info("HTTP publisher starting up")
        super(HTTPPublisher, self).__init__(parsed_url)
        self.headers = {
            'Content-type': 'application/json',
            'X-Ceilometer-Secret': cfg.CONF.publisher_http.secret
        }
        self.timeout = cfg.CONF.publisher_http.timeout
        self.target = cfg.CONF.publisher_http.target
        self.verify_ssl = cfg.CONF.publisher_http.verify_ssl

    def publish_samples(self, context, samples):
        """Publishes sample as JSON to the configures HTTP host

        """
        for sample in samples:
            LOG.debug("HTTP publisher got sample")
            try:
                response = requests.post(self.target,
                                         data=json.dumps(sample.as_dict()),
                                         headers=self.headers,
                                         timeout=self.timeout,
                                         verify=self.verify_ssl)
                LOG.debug(_('Message posting finished with status code %d.') % response.status_code)
            except Exception as err:
                LOG.exception(_('Failed to record metering data: %s'), err)
