################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMHardDiskMap

IBMHardDiskMap maps the ibmServeRaidPhysDeviceTable to disks objects

$Id: IBMHardDiskMap.py,v 1.0 2011/01/10 20:02:03 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMHardDiskMap(SnmpPlugin):
    """Map IBM Director Hard Disk table to model."""

    maptype = "IBMHardDiskMap"
    modname = "ZenPacks.community.IBMMon.IBMHardDisk"
    relname = "harddisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('ibmServeRaidPhysTable',
                    '1.3.6.1.4.1.2.6.167.2.1.2.2.1',
                    {
                        '.4': 'bay',
                        '.5': 'setProductKey',
                        '.6': 'size',
                        '.7': 'status',
                        '.9': '_deviceType',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, disk in tabledata.get('ibmServeRaidPhysTable', {}).iteritems():
            if disk.get('_deviceType', 1) != 1: continue
            try:
                om = self.objectMap(disk)
                om.bay = getattr(om, 'bay', 0)
                om.description = "HardDisk%s" % om.bay
                om.id = self.prepId(om.description)
                model = getattr(om, 'setProductKey', 'Unknown Hard Disk')
                om.setProductKey = MultiArgs(model, model.split()[0])
                om.size = getattr(om, 'size', 0) * 1048576
                om.diskType = 'Unknown'
            except AttributeError:
                continue
            rm.append(om)
        return rm
