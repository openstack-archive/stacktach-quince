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

import oahu.config


class Impl(object):
    def __init__(self, config, scratchpad):
        """config is a ConfigParser object.
           Use the scratchpad to ensure we don't create multiple
           connections to the db.
        """

        if 'quincy_config' not in scratchpad:
            target = config.get('quince', 'oahu_config')
            print "Quince is using oahu driver from %s" % target
            quincy_config = oahu.config.get_config(target)
            scratchpad['quincy_config'] = quincy_config
            scratchpad['quincy_driver'] = quincy_config.get_driver()

        self.oahu_config = scratchpad['quincy_config']
        self.driver = scratchpad['quincy_driver']

    def get_streams(self, **kwargs):
        return self.driver.find_streams(**kwargs)

    def get_stream(self, stream_id, details):
        return None

    def delete_stream(self, stream_id):
        pass

    def reset_stream(self, stream_id):
        pass
