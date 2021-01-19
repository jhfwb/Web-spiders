__author__ = "Burgess Zheng"
# !/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Decorator
'''
class foo(object):
    def f1(self):
        print("original f1")

    def f2(self):
        print("original f2")


class foo_decorator(object):
    def __init__(self, decoratee):
        self._decoratee = decoratee

    def f1(self):
        print("decorated f1")
        self._decoratee.f1()

    def __getattr__(self, name):#当python访问不存在的属性的时候，会调用该方法。
        return getattr(self._decoratee, name)


u = foo()
v = foo_decorator(u)
v.f1()
v.f2()