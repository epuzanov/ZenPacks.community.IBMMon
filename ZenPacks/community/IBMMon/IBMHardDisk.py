################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMHardDisk

IBMHardDisk is an abstraction of a harddisk.

$Id: IBMHardDisk.py,v 1.0 2011/01/10 19:48:47 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.HardDisk import HardDisk
from IBMComponent import *

class IBMHardDisk(HardDisk, IBMComponent):
    """IBMHardDisk object"""

    size = 0
    diskType = ""
    bay = 0
    status = 2

    statusmap ={1: (DOT_RED, SEV_CRITICAL, 'Dead'),
                2: (DOT_GREEN, SEV_CLEAN, 'Online'),
                3: (DOT_GREEN, SEV_CLEAN, 'Standby'),
                4: (DOT_YELLOW, SEV_WARNING, 'Rebuild'),
                5: (DOT_GREEN, SEV_CLEAN, 'Spare'),
                6: (DOT_GREEN, SEV_CLEAN, 'Ready'),
                7: (DOT_GREY, SEV_INFO, 'Empty'),
                9: (DOT_GREY, SEV_WARNING, 'Unknown'),
                }


    _properties = HardDisk._properties + (
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )

    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewIBMHardDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMHardDisk'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size, divby=1000)

    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        return 'Unknown'

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(IBMHardDisk)
