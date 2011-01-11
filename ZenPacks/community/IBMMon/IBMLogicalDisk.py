################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMLogicalDisk

IBMLogicalDisk is an abstraction of a harddisk.

$Id: IBMLogicalDisk.py,v 1.0 2011/01/10 19:49:54 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.LogicalDisk import LogicalDisk
from IBMComponent import *

class IBMLogicalDisk(LogicalDisk, IBMComponent):
    """IBMLogicalDisk object"""


    writeCacheMode = ''
    status = 1

    statusmap ={1: (DOT_GREEN, SEV_CLEAN, 'Online'),
                2: (DOT_RED, SEV_CRITICAL, 'Critical'),
                3: (DOT_ORANGE, SEV_ERROR, 'Offline'),
                4: (DOT_YELLOW, SEV_WARNING, 'Migrating'),
                5: (DOT_GREEN, SEV_CLEAN, 'Free'),
                9: (DOT_GREY, SEV_WARNING, 'Unknown'),
                }


    _properties = LogicalDisk._properties + (
                 {'id':'writeCacheMode', 'type':'string', 'mode':'w'},
                 )

    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewIBMLogicalDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMLogicalDisk'
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

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(IBMLogicalDisk)
