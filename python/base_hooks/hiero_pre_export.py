# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class HieroPreExport(HookBaseClass):
    """
    Allows clearing of caches prior to shot processing
    """
    def execute(self, processor, **kwargs):
        """
        Allows clearing of caches prior to shot processing. This is called just prior to export.

        :param processor: Processor The is being used, in case distinguishing between
                          differnt exports is needed.
        """
        pass
