"""
Originally from: http://github.com/jacobian/munin-plugins/blob/master/munin.py

Microframework for writing Munin plugins with Python.

Howto:

    * Subclass ``Plugin``.
    
    * Define at least ``fetch`` and ``config``, and possibly others (see
      below).
    
    * Add a main invocation to your script.

A simple example::

    import munin
    
    class Load(munin.Plugin):
        
        def fetch(self):
            load1, load5, load15 = open("/proc/loadavg").split(' ')[:3]
            return [
                ("load1.value", load1),
                ("load5.value", load5),
                ("load15.value", load15)
            ]
            
        def config(self):
            return [
                ("graph_title", "Load"),
                ("graph_args", "-l 0 --base 1000"),
                ("graph_vlabel", "Load"),
                ("load1.label", "1 min"),
                ("load5.label", "5 min"),
                ("load15.label", "15 min")
            ]

    if __name__ == '__main__':
        munin.run(Load)

For more complex uses, read the code. It's short.
"""

import os
import sys

class Plugin(object):
    
    def __init__(self):
        self.env = {}
        for var, default in self.__get_dynamic_attr("env_vars", None, {}).items():
            self.env[var] = os.environ.get(var, default)
        
    def __get_dynamic_attr(self, attname, arg, default=None):
        """
        Gets "something" from self, which could be an attribute or
        a callable with either 0 or 1 arguments (besides self).
        
        Stolen from django.contrib.syntication.feeds.Feed.
        """
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check func_code.co_argcount rather than try/excepting the
            # function and catching the TypeError, because something inside
            # the function may raise the TypeError. This technique is more
            # accurate.
            if hasattr(attr, 'func_code'):
                argcount = attr.func_code.co_argcount
            else:
                argcount = attr.__call__.func_code.co_argcount
            if argcount == 2: # one argument is 'self'
                return attr(arg)
            else:
                return attr()
        return attr
    
    def main(self, argv):
        if "_" in argv[0]: 
            _, arg = argv[0].rsplit("_", 1)
        else:
            arg = None
        args = argv[1:]
        
        if "suggest" in args and hasattr(self, "suggest"):
            for suggested in self.__get_dynamic_attr("suggest", arg):
                print suggested
            return 0
                
        if "autoconf" in args:
            if self.__get_dynamic_attr("autoconf", arg, True):
                print "yes"
                return 0
            else:
                print "no"
                return 1
                
        if "config" in args:
            for field, value in self.__get_dynamic_attr("config", arg, []):
                print "%s %s" % (field, value)
            return 0
        
        for field, value in self.__get_dynamic_attr("fetch", arg, []):
            print "%s %s" % (field, value)
        return 0
            
def run(plugin):
    if callable(plugin):
        plugin = plugin()
    sys.exit(plugin.main(sys.argv))
