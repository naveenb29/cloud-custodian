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
import json
import os

from c7n.mu import (
    CloudWatchEventSource,
    LambdaFunction,
    LambdaManager,
    PythonPackageArchive)


entry_source = """\
import logging

from c7n_mailer import handle

logger = logging.getLogger('custodian.mailer')
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.getLogger('botocore').setLevel(logging.WARNING)

def dispatch(event, context):
    return handle.start_c7n_mailer(event, context, logger)
"""


def get_archive(config):
    archive = PythonPackageArchive(
        'c7n_mailer', 'ldap3', 'pyasn1', 'jinja2', 'markupsafe', 'yaml',
        'memcache')

    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'msg-templates'))

    for t in os.listdir(template_dir):
        with open(os.path.join(template_dir, t)) as fh:
            archive.add_contents('msg-templates/%s' % t, fh.read())

    archive.add_contents('config.json', json.dumps(config))
    archive.add_contents('periodic.py', entry_source)

    archive.close()
    return archive


def provision(config, session_factory):
    func_config = dict(
        name='cloud-custodian-mailer',
        description='Cloud Custodian Mailer',
        handler='periodic.dispatch',
        runtime='python2.7',
        memory_size=config['memory'],
        timeout=config['timeout'],
        role=config['role'],
        subnets=config['subnets'],
        security_groups=config['security_groups'],
        events=[
            CloudWatchEventSource(
                {'type': 'periodic',
                 'schedule': 'rate(5 minutes)'},
                session_factory,
                prefix="")
        ])

    archive = get_archive(config)
    func = LambdaFunction(func_config, archive)
    manager = LambdaManager(session_factory)
    manager.publish(func)
