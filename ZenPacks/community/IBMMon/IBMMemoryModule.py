################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMMemoryModule

IBMMemoryModule is an abstraction of a  Memory Module.

$Id: IBMMemoryModule.py,v 1.1 2011/01/07 19:13:49 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import MemoryModule
from IBMComponent import *

class IBMMemoryModule(MemoryModule, IBMComponent):
    """MemoryModule object"""

    status = 0

    # we monitor Memory modules
    monitor = True

    _properties = MemoryModule._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(IBMMemoryModule)
