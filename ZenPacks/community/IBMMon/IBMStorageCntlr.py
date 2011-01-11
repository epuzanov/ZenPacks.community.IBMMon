################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMStorageCntlr

IBMStorageCntlr is an abstraction of a IBM ServerRAID Controller.

$Id: IBMStorageCntlr.py,v 1.0 2011/01/10 20:49:42 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from IBMExpansionCard import *

class IBMStorageCntlr(IBMExpansionCard):
    """IBM ServerRAID Storage Controller object"""

    FWRev = ""
    SWVer = ""

    # we monitor RAID Controllers
    monitor = True

    statusmap ={1: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                2: (DOT_RED, SEV_CRITICAL, 'Fail'),
                }

    _properties = IBMExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
    )


    factory_type_information = (
        {
            'id'             : 'IBMStorageCntlr',
            'meta_type'      : 'IBMStorageCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addIBMStorageCntlr',
            'immediate_view' : 'viewIBMStorageCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMStorageCntlr'
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


InitializeClass(IBMStorageCntlr)
