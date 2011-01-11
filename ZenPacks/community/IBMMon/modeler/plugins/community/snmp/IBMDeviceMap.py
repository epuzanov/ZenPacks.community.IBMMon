################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMDeviceMap

IBMDeviceMap maps mib elements from IBM Director mib to get hw and os products.

$Id: IBMDeviceMap.py,v 1.1 2011/01/07 23:36:22 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMDeviceMap(SnmpPlugin):
    """Map mib elements from IBM Director mib to get hw and os products.
    """

    maptype = "IBMDeviceMap" 


    snmpGetTableMaps = (
        GetTableMap('sysTable',
                    '.1.3.6.1.4.1.2.6.159.1.1.60.1.1',
                    {
                        '.2': '_comp',
                        '.3': 'setHWSerialNumber',
                        '.4': '_manuf',
                        '.5': 'setHWProductKey',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        for comp in results[1].get('sysTable', {'0':{}}).values():
            if comp.get('_comp', '') != 'System': continue
            om = self.objectMap(comp)
            try:
                om.setHWProductKey = MultiArgs(om.setHWProductKey, om._manuf)
                return om
            except: return

