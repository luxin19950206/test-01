#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:42:38 2019

@author: hengzong
"""

import numpy as np
print(np.sin(np.arange(10000000)))
%prun np.sin(np.arrange(10000000))