################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMCPU

IBMCPU is an abstraction of a CPU.

$Id: IBMCPU.py,v 1.1 2011/01/07 19:07:19 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.CPU import CPU

class IBMCPU(CPU):
    """CPU object"""

    core = 1

    _properties = CPU._properties + (
         {'id':'core', 'type':'int', 'mode':'w'},
    )

InitializeClass(IBMCPU)
