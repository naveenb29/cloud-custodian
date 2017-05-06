# Copyright 2016 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from cStringIO import StringIO
import json


def format_struct(struct):
    io = StringIO()
    json.dump(struct, io, indent=2)
    return io.getvalue()


def setup_defaults(config):
    config.setdefault('region', 'us-east-1')
    config.setdefault('ses_region', config.get('region'))
    config.setdefault('memory', 1024)
    config.setdefault('timeout', 300)
    config.setdefault('subnets', None)
    config.setdefault('security_groups', None)
    config.setdefault('contact_tags', [])
    config.setdefault('ldap_uri', None)
    config.setdefault('ldap_bind_dn', None)
    config.setdefault('ldap_bind_user', None)
    config.setdefault('ldap_bind_password', None)
