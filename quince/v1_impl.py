# Copyright (c) 2014 Dark Secret Software Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging


from winchester.config import ConfigManager, ConfigSection, ConfigItem
from winchester.db import DBInterface
from winchester import models


logger = logging.getLogger(__name__)


class Impl(object):

    @classmethod
    def config_description(cls):
        return dict(config_path=ConfigItem(
                            help="Path(s) to find additional config files",
                                 multiple=True, default='.'),
                    database=ConfigSection(help="Database connection info.",
                            config_description=DBInterface.config_description()),
                   )

    def __init__(self, config, scratchpad):
        """config is a ConfigParser object.
           Use the scratchpad to ensure we don't create multiple
           connections to the db.
        """

        if 'quincy_config' not in scratchpad:
            target = config.get('quince', 'winchester_config')
            logger.debug("Quince is using Winchester config from %s" % target)
            quincy_config = ConfigManager.load_config_file(target)
            quincy_config = ConfigManager.wrap(quincy_config,
                                self.config_description())

            scratchpad['quincy_config'] = quincy_config
            scratchpad['quincy_driver'] = DBInterface(quincy_config['database'])

        self.winchester_config = scratchpad['quincy_config']
        self.driver = scratchpad['quincy_driver']

    def find_streams(self, count=False, state=None, older_than=None,
                    younger_than=None, trigger_name=None,
                    distinguishing_traits=None, mark=None, limit=None):

        if state is not None:
            try:
                state = models.StreamState[state.lower()]
            except KeyError:
                logger.error("invalid stream state %s" % state)
                raise
        return self.driver.find_streams(count=count,
                            state=state, name=trigger_name,
                            younger_than=younger_than, older_than=older_than,
                            distinguishing_traits=distinguishing_traits,
                            mark=mark, limit=limit)

    def get_stream(self, stream_id, details):
        stream = int(stream_id)
        # Returns a list, but should be just one stream.
        return self.driver.find_streams(stream_id=stream_id,
                                        include_events=details)

    def delete_stream(self, stream_id):
        stream_id = int(stream_id)
        stream = self.driver.get_stream_by_id(stream_id)
        self.driver.purge_stream(stream)

    def reset_stream(self, stream_id):
        stream_id = int(stream_id)
        stream = self.driver.get_stream_by_id(stream_id)
        self.driver.reset_stream(stream)

    def find_events(self, from_datetime=None, to_datetime=None,
                         event_name=None, traits=[],
                         mark=None, limit=None, count=False):
        return self.driver.find_events(from_datetime=from_datetime,
                                       to_datetime=to_datetime,
                                       event_name=event_name,
                                       traits=traits,
                                       mark=mark, limit=limit,
                                       count=count)

    def get_event(self, message_id):
        return self.driver.get_event_by_message_id(message_id)
