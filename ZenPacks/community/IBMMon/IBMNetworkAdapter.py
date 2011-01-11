################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMNetworkAdapter

IBMNetworkAdapter is an abstraction of a IBM NetworkAdapter.

$Id: IBMNetworkAdapter.py,v 1.1 2011/01/07 19:29:27 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from IBMExpansionCard import IBMExpansionCard
from IBMComponent import *

class IBMNetworkAdapter(IBMExpansionCard):
    """NetworkAdapter object"""

    macaddress = ""
    speed = 0

    # we monitor Network Adapters
    monitor = True

    _properties = IBMExpansionCard._properties + (
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'IBMNetworkAdapter',
            'meta_type'      : 'IBMNetworkAdapter',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'IBMMon',
            'factory'        : 'manage_addIBMNetworkAdapter',
            'immediate_view' : 'viewIBMNetworkAdapter',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMNetworkAdapter'
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


    def speedString(self):
        """
        Return the speed in human readable form
        """
        if not self.speed: return 'Unknown'
        return convToUnits(self.speed, divby=1000, unitstr='bps') 


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates


InitializeClass(IBMNetworkAdapter)
