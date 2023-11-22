#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:38:14 2020

@author: david.hufnagel
"""


inp = open("1C.fna")
out = open("1Cstrains.txt", "w")


for line in inp:
    if line.startswith(">"):
        