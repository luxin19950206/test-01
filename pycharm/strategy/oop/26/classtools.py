# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：Assorted class utitles and tools
p672
"""


class AttrDisplay:
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
            return ','.join(attrs)

    def __str__(self):
        return '[%s,%s]' % (self.__class__.__name__, self.gatherAttrs())


if __name__ == '__main__':
    class TopTest(AttrDisplay):
        count = 0

        def __init__(self):
            self.attr1 = TopTest.count
            self.attr2 = TopTest.count + 1
            TopTest.count += 2


    class SubTest(TopTest):
        pass


    X, Y = TopTest(), SubTest()
    print(x)
    print(y)
