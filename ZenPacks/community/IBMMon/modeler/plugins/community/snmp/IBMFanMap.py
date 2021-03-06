################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMFanMap

IBMFanMap maps the iBMPSGTachometerTable table to fab objects

$Id: IBMFanMap.py,v 1.1 2011/01/11 19:04:50 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMFanMap(SnmpPlugin):
    """Map IBM Director Fans table to model."""

    maptype = "IBMFanMap"
    modname = "ZenPacks.community.IBMMon.IBMFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('fanTable',
                    '1.3.6.1.4.1.2.6.159.1.1.80.5.1',
                    {
                        '.1': 'id',
                        '.12': 'threshold',
                        '.17': 'type',
                    }
        ),
    )


    types ={0: 'Unknown', 
            1: 'System Fan',
            2: 'PowerSupply Fan',
            3: 'CPU Fan',
            }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, fan in tabledata.get('fanTable', {}).iteritems():
            try:
                om = self.objectMap(fan)
                om.snmpindex =  oid.strip('.')
                om.id = self.prepId(om.id)
                om.type = self.types.get(int(getattr(om, 'type', 2)),
                                        'Unknown (%s)' % getattr(om, 'type', 2))
                om.status = 0
            except AttributeError:
                continue
            rm.append(om)
        return rm
