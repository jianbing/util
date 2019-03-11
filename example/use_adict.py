#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from util.tool.adict import Adict

if __name__ == '__main__':
    t = {"name": "jianbing",
         "job": "tester",
         "skill": [{"python": 60}, {"java": 60}],
         }
    t2 = Adict.load_dict(t)
    print(t2)
    print(t2.name)
    print(t2.skill[0].python)
