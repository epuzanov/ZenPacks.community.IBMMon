################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMComponent

IBMComponent is an abstraction

$Id: IBMComponent.py,v 1.1 2011/01/07 19:05:29 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenossSecurity import *

class IBMComponent(HWStatus):

    statusmap ={0: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                1: (DOT_YELLOW, SEV_WARNING, 'Warning'),
                2: (DOT_RED, SEV_CRITICAL, 'Critical'),
                }

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

