################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMPowerSupplyMap

IBMPowerSupplyMap maps the ibmPowerSupplyTable table to powersupplies objects

$Id: IBMPowerSupplyMap.py,v 1.1 2011/01/07 21:39:57 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMPowerSupplyMap(SnmpPlugin):
    """Map IBM Director Power Supplies table to model."""

    maptype = "IBMPowerSupplyMap"
    modname = "ZenPacks.community.IBMMon.IBMPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('powerSupplyTable',
                    '.1.3.6.1.4.1.2.6.159.1.1.130.1.1',
                    {
                        '.1': 'id',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, ps in tabledata.get('powerSupplyTable', {}).iteritems():
            try:
                om = self.objectMap(ps)
                om.snmpindex =  oid.strip('.')
                om.id = self.prepId(om.id)
            except AttributeError:
                continue
            rm.append(om)
        return rm
