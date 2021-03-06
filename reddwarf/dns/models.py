# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010-2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http: //www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Model classes that map instance Ip to dns record.
"""

import logging

from reddwarf import db
from reddwarf.common.models import ModelBase
from reddwarf.instance.models import InvalidModelError
from reddwarf.instance.models import ModelNotFoundError

LOG = logging.getLogger(__name__)


def persisted_models():
    return {
        'dns_records': DnsRecord,
        }


class DnsRecord(ModelBase):

    _data_fields = ['name', 'record_id']
    _table_name = 'dns_records'

    def __init__(self, name, record_id):
        self.name = name
        self.record_id = record_id

    @classmethod
    def create(cls, **values):
        record = cls(**values).save()
        if not record.is_valid():
            raise InvalidModelError(record.errors)
        return record

    def save(self):
        if not self.is_valid():
            raise InvalidModelError(self.errors)
        LOG.debug(_("Saving %s: %s") %
                  (self.__class__.__name__, self.__dict__))
        return db.db_api.save(self)

    def delete(self):
        LOG.debug(_("Deleting %s: %s") %
                  (self.__class__.__name__, self.__dict__))
        return db.db_api.delete(self)

    @classmethod
    def find_by(cls, **conditions):
        model = cls.get_by(**conditions)
        if model is None:
            raise ModelNotFoundError(_("%s Not Found") % cls.__name__)
        return model

    @classmethod
    def get_by(cls, **kwargs):
        return db.db_api.find_by(cls, **cls._process_conditions(kwargs))

    @classmethod
    def _process_conditions(cls, raw_conditions):
        """Override in inheritors to format/modify any conditions."""
        return raw_conditions
