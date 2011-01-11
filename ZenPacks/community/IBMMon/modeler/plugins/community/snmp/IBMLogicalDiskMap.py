################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMLogicalDiskMap

IBMLogicalDiskMap maps the ibmServeRaidLogicalTable to disks objects

$Id: IBMLogicalDiskMap.py,v 1.0 2011/01/10 20:10:10 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMLogicalDiskMap(SnmpPlugin):
    """Map IBM ServerRAID Logical Disk table to model."""

    maptype = "IBMLogicalDiskMap"
    modname = "ZenPacks.community.IBMMon.IBMLogicalDisk"
    relname = "logicaldisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('ibmServeRaidCntlrTable',
                    '1.3.6.1.4.1.2.6.167.2.1.2.1.1',
                    {
                        '.2': '_cntlrId',
                        '.13': 'stripesize',
                    }
        ),
        GetTableMap('ibmServeRaidLogTable',
                    '1.3.6.1.4.1.2.6.167.2.1.2.3.1',
                    {
                        '.2': '_cntlrId',
                        '.3': 'description',
                        '.4': 'status',
                        '.5': 'size',
                        '.6': 'diskType',
                        '.7': 'writeCacheMode',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        cards = {}
        for card in tabledata.get('ibmServeRaidCntlrTable',{}).values():
            cards[card['_cntlrId']] = card['stripesize']
        for oid, disk in tabledata.get('ibmServeRaidLogTable',{}).iteritems():
            try:
                om = self.objectMap(disk)
                om.description = 'LogicalDisk%s'%om.description
                om.id = self.prepId(om.description)
                om.snmpindex = oid.strip('.')
                om.diskType = getattr(om, 'diskType', 'Unknown')
                om.stripesize = cards.get(getattr(om, '_cntlrId', 0),0) * 1024
                om.size = getattr(om, 'size', 0) * 1048576
                if getattr(om, 'writeCacheMode', 1):
                    om.writeCacheMode = 'write back'
                else:
                    om.writeCacheMode = 'write through'
            except AttributeError:
                continue
            rm.append(om)
        return rm
