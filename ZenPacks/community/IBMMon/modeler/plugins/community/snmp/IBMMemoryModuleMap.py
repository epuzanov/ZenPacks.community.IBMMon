################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009. 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMMemoryModuleMap

IBMMemoryModuleMap maps the PhysicalMemoryTable table to IBMMemoryModule objects

$Id: IBMMemoryModuleMap.py,v 1.1 2011/01/07 21:33:32 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMMemoryModuleMap(SnmpPlugin):
    """Map IBM Director Memory Module table to model."""

    maptype = "IBMMemoryModule"
    modname = "ZenPacks.community.IBMMon.IBMMemoryModule"
    relname = "memorymodules"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('memoryModulesTable',
                    '1.3.6.1.4.1.2.6.159.1.1.120.1.1',
                    {
                        '.1': 'slot',
                        '.2': '_active',
                        '.7': '_slottype',
                        '.8': '_technology',
                        '.10': '_speed',
                        '.11': 'size',
                        '.12': '_banck',
                        '.13': 'id',
                        '.14': '_manufacturer',
                        '.16': 'serialNumber',
                    }
        ),
    )

    slottypes = { 0: 'Unknown',
                    1: 'Other',
                    2: 'SIP',
                    3: 'DIP',
                    4: 'ZIP',
                    5: 'SOJ',
                    6: 'Proprietary',
                    7: 'SIMM',
                    8: 'DIMM',
                    9: 'TSOP',
                    10: 'PGA',
                    11: 'RIMM',
                    12: 'SODIMM',
                    13: 'SRIMM',
                    14: 'SMD',
                    15: 'SSMP',
                    16: 'QFP',
                    17: 'TQFP',
                    18: 'SOIC',
                    19: 'LCC',
                    20: 'PLCC',
                    21: 'BGA',
                    22: 'FPBGA',
                    23: 'LGA',
                    }

    technologies = { 0: 'Unknown',
                    1: 'Other',
                    2: 'DRAM',
                    3: 'Synchronous DRAM',
                    4: 'Cache DRAM',
                    5: 'EDO',
                    6: 'EDRAM',
                    7: 'VRAM',
                    8: 'SRAM',
                    9: 'RAM',
                    10: 'ROM',
                    11: 'Flash',
                    12: 'EEPROM',
                    13: 'FEPROM',
                    14: 'EPROM',
                    15: 'CDRAM',
                    16: '3DRAM',
                    17: 'SDRAM',
                    18: 'SGRAM',
                    19: 'RDAM',
                    20: 'DDR',
                    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, card in tabledata.get('memoryModulesTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex =  oid.strip('.')
                om.slot = om.slot.split()[-1]
                om.id = self.prepId('%s %s' % (getattr(om,'_banck','0'),
                                                getattr(om, 'id', om.slot)))
                om.size = getattr(om, 'size', 0)
                if om.size > 0:
                    model = []
                    if getattr(om, '_manufacturer', 'null') != 'null':
                        model.append(getattr(om, '_manufacturer', ''))
                        manuf = getattr(om, '_manufacturer', '')
                    else: manuf = 'Unknown'
                    if self.technologies.get(om._technology, '') != '':
                        model.append(self.technologies.get(om._technology, ''))
                    if 2 < int(getattr(om, '_slottype', 0)) < 24:
                        model.append(self.slottypes[int(om._slottype)])
                    model.append(convToUnits(om.size))
                    if getattr(om, '_frequency', 0) > 0:
                        model.append("%sMHz" % getattr(om, '_frequency', 0))
                    if getattr(om, '_speed', 'null') != 'null':
                        model.append("%sns" % getattr(om, '_speed', 0))
                    om.setProductKey = MultiArgs(" ".join(model), manuf)
                if getattr(om, '_active', 0) == 0: om.monitor = False
                om.status = 0
            except AttributeError:
                continue
            rm.append(om)
        return rm

