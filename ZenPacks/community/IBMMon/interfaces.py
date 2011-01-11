################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.0 2011/01/11 00:57:50 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IIBMStorageCntlrInfo(IComponentInfo):
    """
    Info adapter for IBMStorageCntlr components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    FWRev = schema.Text(title=u"Firmware Revision", readonly=True,
                                                                group='Details')
    SWVer = schema.Text(title=u"BIOS Version", readonly=True, group='Details')

class IIBMNetworkAdapterInfo(IComponentInfo):
    """
    Info adapter for IBMNetworkAdapter components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    macaddress = schema.Text(title=u"MAC Address", readonly=True,
                                group='Network Settings')
    speed = schema.Text(title=u"Speed", readonly=True,
                                group='Network Settings')

class IIBMLogicalDiskInfo(IComponentInfo):
    """
    Info adapter for IBMLogicalDisk components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    description = schema.Text(title=u"OS Name", readonly=True,
                                group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    stripesize = schema.Text(title=u"Stripe Size",readonly=True,group='Details')
    size = schema.Text(title=u"Size", readonly=True, group='Details')
    writeCacheMode = schema.Text(title=u"Write Cache Mode", readonly=True,
                                                                group='Details')
