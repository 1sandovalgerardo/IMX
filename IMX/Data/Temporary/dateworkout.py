#!/usr/bin/env python

from dateutil import parser

a = parser.parse('01/01/2022').date()

print(a)
print(type(a))

print(a.date())
