################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMStorageCntlrMap

IBMStorageCntlrMap maps the ServeRaidController table to IBMStorageCntlr objects

$Id: IBMStorageCntlrMap.py,v 1.0 2011/01/10 20:13:28 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from IBMExpansionCardMap import IBMExpansionCardMap

class IBMStorageCntlrMap(IBMExpansionCardMap):
    """Map IBM Director ServeRAID table to model."""

    maptype = "IBMStorageCntlrMap"
    modname = "ZenPacks.community.IBMMon.IBMStorageCntlr"

    snmpGetTableMaps = (
        GetTableMap('ibmServeRaidCntlrTable',
                    '1.3.6.1.4.1.2.6.167.2.1.2.1.1',
                    {
                        '.2': 'id',
                        '.3': 'setProductKey',
                        '.4': 'FWRev',
                        '.5': 'SWVer',
                        '.14': 'slot',
                        '.15': '_manuf',
                        '.16': 'status',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in IBMExpansionCardMap.oms:
            IBMExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('ibmServeRaidCntlrTable',{}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("ServerRAID%s" % om.id)
                om.slot = getattr(om, 'slot', 0)
                om.setProductKey = MultiArgs(getattr(om, 'setProductKey',
                                'IBM ServerRAID'), getattr(om, '_manuf', 'IBM'))
            except AttributeError:
                continue
            IBMExpansionCardMap.oms[device.id].append(om)
        return

