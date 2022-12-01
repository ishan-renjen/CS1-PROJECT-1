"""
Ishan Renjen
Project 1
CS141-7
timeline_plot.py
"""

import index_tools as i
import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy

def build_plottable_array(xyears, regiondata):
    array = []
    """
    sort through regiondata - 
        if it corresponds to a year in xyears then add it to a list - 
            if not present do the ma.maskedArray thing for the year
    """
    for year in range(len(xyears)):
        for object in regiondata:
            if regiondata[object].year == xyears[year]:
                array.append(regiondata[object])
        if xyears[year] != regiondata[object].year:
            ma.masked_array(xyears[year], None)

    print(array)


def filter_years(data, year0, year1):
    pass

def plotHPI(data, regionList):
    pass

def plot_whiskers(data, regionList):
    pass


xyears = [1999, 2000, 2002, 2003, 2004, 2007, 2010]
data_dict = i.annualize(i.read_state_house_price_data("data/HPI_AT_state.txt"))
regiondata = data_dict.get("NY")
build_plottable_array(xyears, regiondata)