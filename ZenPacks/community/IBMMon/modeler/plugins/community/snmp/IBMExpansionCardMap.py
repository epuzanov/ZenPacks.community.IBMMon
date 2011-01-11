################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMExpansionCardMap

IBMExpansionCardMap maps table to cards objects

$Id: IBMExpansionCardMap.py,v 1.0 2011/01/05 00:13:35 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin,GetTableMap

class IBMExpansionCardMap(SnmpPlugin):
    """Map IBM Director PCI table to model."""

    relname = "cards"
    compname = "hw"

    oms = {}

    snmpGetTableMaps = (
        GetTableMap('statusTable',
                    '1.3.6.1.4.1.2.6.159.1.1.30.3.1',
                    {
                        '.2': 'status',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        if not device.id in self.oms:
            self.oms[device.id] = []
        rm = self.relMap()
        for om in self.oms[device.id]:
            rm.append(om)
        del self.oms[device.id]
        return rm
