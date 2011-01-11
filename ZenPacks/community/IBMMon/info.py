################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of hardware components.

$Id: info.py,v 1.0 2011/01/11 01:02:51 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.IBMMon import interfaces


class IBMStorageCntlrInfo(ComponentInfo):
    implements(interfaces.IIBMStorageCntlrInfo)

    FWRev = ProxyProperty("FWRev")
    SWVer = ProxyProperty("SWVer")
    slot = ProxyProperty("slot")

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class IBMNetworkAdapterInfo(ComponentInfo):
    implements(interfaces.IIBMNetworkAdapterInfo)

    slot = ProxyProperty("slot")
    macaddress = ProxyProperty("macaddress")

    @property
    def speed(self):
        return self._object.speedString()

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class IBMLogicalDiskInfo(ComponentInfo):
    implements(interfaces.IIBMLogicalDiskInfo)

    description = ProxyProperty("description")
    diskType = ProxyProperty("diskType")
    writeCacheMode = ProxyProperty("writeCacheMode")

    @property
    def stripesize(self):
        return convToUnits(self._object.stripesize)

    @property
    def size(self):
        return convToUnits(self._object.size)

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()
