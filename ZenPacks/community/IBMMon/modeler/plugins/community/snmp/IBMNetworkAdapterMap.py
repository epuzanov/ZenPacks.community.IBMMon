################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMNetworkAdapterMap

IBMNetworkAdapterMap maps the ibmSystemLogicalNetworkAdapterTable table to cards
objects

$Id: IBMNetworkAdapterMap.py,v 1.0 2009/07/21 23:36:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from IBMExpansionCardMap import IBMExpansionCardMap

import re
MACPAT=re.compile(r'^(\w{2})(\w{2})(\w{2})(\w{2})(\w{2})(\w{2})$')

class IBMNetworkAdapterMap(SnmpPlugin):
    """Map IBM Director PCI table to model."""

    maptype = "IBMNetworkAdapterMap"
    modname = "ZenPacks.community.IBMMon.IBMNetworkAdapter"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('networkAdapterTable',
                    '.1.3.6.1.4.1.2.6.159.1.1.110.1.1',
                    {
                        '.1': 'id',
                        '.3': 'setProductKey',
                        '.7': 'macaddress',
                        '.8': 'speed',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in IBMExpansionCardMap.oms:
            IBMExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('networkAdapterTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex =  oid.strip('.')
                om.id = self.prepId(om.id)
                om.slot = 0
                if hasattr(om, 'setProductKey'):
                    om.setProductKey = MultiArgs(om.setProductKey,
                                            om.setProductKey.split()[0]) 
                r = MACPAT.search(getattr(om, 'macaddress', ''))
                if r: om.macaddress = ':'.join(r.groups())
                else: om.macaddress = ''
                om.speed = float(getattr(om, 'speed', 0)) * 1000000
                om.status = 0
            except AttributeError:
                continue
            IBMExpansionCardMap.oms[device.id].append(om)
        return
