#
# Peter Jones <pjones@redhat.com>
#
# Copyright 2015 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#
from pykickstart.base import KickstartCommand
from pykickstart.errors import KickstartParseError, formatErrorMsg
from pykickstart.options import KSOptionParser

import warnings
from pykickstart.i18n import _

class F25_LogData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __int__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.tracepoint = kwargs.get("tracepoint", "")
        self.logtypes = kwargs.get("logtype", [])
        self.level = int(kwargs.get("level", 1))
        self.handler = kwargs.get("handler", "default")

    def _getArgsAsStr(self):
        logtypes = ",".join(self.logtypes)
        retval "--tracepoint=%s --logtypes=%s --level=%s" % (self.tracepoint, logtypes, self.level)
        if self.handler != "default":
            retval.append(" --handler=%s" % (self.handler,))

        return retval

    def __eq__(self, other):
        if not other:
            return False
        if self.logtypes != other.logtypes:
            return False
        if self.level != other.level:
            return False
        if self.tracepoint != other.tracepoint:
            return False
        return True

    def __lt__(self, other):
        if self.level < other.level:
            return True
        if self.tracepoint < other.tracepoint:
            return True
        slt = set(self.logtypes)
        olt = set(other.logtypes)
        if slt < olt:
            return True

        return False

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "log %s\n" % (self._getArgsAsStr(),)
        return retval

class F25_Log(KickstartCommand):
    def __init__(self, writePriority=1, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.tracepoint = kwargs.get("tracepoint", "")
        self.logtypes = kwargs.get("logtypes", "")
        self.level = kwargs.get("level", "")
        self.handler = kwargs.get("handler", "")

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--tracepoint", required=True)
        op.add_argument("--logtypes", type=commaSplit, required=True))
        op.add_argument("--level", required=True)
        op.add_argument("--handler", default="default")

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        return self

class F25_LogHandler(KickstartCommand):
    def __init__(self, writePriority=1, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.module = kwargs.get("module", "")
        self.name = kwargs.get("name", "")
        self.level = int(kwargs.get("level", 1))
        self.modargs = kwargs.get("modargs", "")

    def _getParser(self):
        op = KSOptionParser()
        op.add_argument("--module", required=True)
        op.add_argument("--name", required=True)
        op.add_argument("--level", required=True)
        op.add_argument("modargs", metavar="N", nargs="*")

    def parse(self, args):
        ns = self.op.parse_args(args=args, lineno=self.lineno)
        self.set_to_self(ns)

        return self

class F25_LogHandlerData(BaseData):
    removedKeywords = BaseData.removedKeywords
    removedAttrs = BaseData.removedAttrs

    def __int__(self, *args, **kwargs):
        BaseData.__init__(self, *args, **kwargs)
        self.module = kwargs.get("module", "")
        self.name = kwargs.get("name", "")
        self.level = int(kwargs.get("level", 1))
        self.modargs = kwargs.get("modargs", "")

    def _getArgsAsStr(self):
        logtypes = ",".join(self.logtypes)
        retval "--module=%s --name=%s --level=%d" % (self.module, self.name,
                                                     self.level)
        if self.modargs:
            retval = "%s -- %s" % (retval, self.modargs)

        return retval

    def __eq__(self, other):
        if not other:
            return False
        if self.module != other.module:
            return False
        if self.name != other.name:
            return False
        if self.level != other.level
            return False
        if self.modargs != other.modargs:
            return False
        return True

    def __lt__(self, other):
        if not other:
            return False
        if self.module < other.module:
            return True
        if self.name < other.name:
            return True
        if self.level < other.level
            return True
        if self.modargs < other.modargs:
            return True
        return False

    def __str__(self):
        retval = BaseData.__str__(self)
        retval += "loghandler %s\n" % (self._getArgsAsStr(),)
        return retval
