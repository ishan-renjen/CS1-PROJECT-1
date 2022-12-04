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
    """
    iterate through xyears
        iterate through regiondata - 
            if it corresponds to a year in xyears 
                add it to a list - array
        if year not in array
            mask
    """
    # array = ma.array(xyears)
    years = dict()
    values = list()
    for i in regiondata:
        years[int(i.year)] = i.idx

    array = ma.empty_like(values)
    for year in xyears:
        if year in years:
            array = ma.append(array, float(years[year]))
        if year not in years:
            array = ma.append(array, None)

    return array


def filter_years(data, year0, year1):
    period_dict = dict()
    templist_years = list()
    for key in data:
        data_list = data.get(key)
        for item in data_list:
            templist_years.append(int(item.year))

        if year0 in templist_years and year1 in templist_years:
            for idx in range(len(templist_years)):
                if templist_years[idx] == year0:
                    pre = idx
                elif templist_years[idx] == year1:
                    post = idx

            data_list = data_list[pre:post+1]
            templist_years.clear()

            if key in period_dict:
                period_dict[key] += data_list
            else:
                period_dict[key] = data_list
        else:
            templist_years.clear()

    for key_lst in period_dict:
        lst_values = period_dict.get(key_lst)
        for mark in range(1, len(lst_values)):
            j=mark
            while j>0 and key_lst[j-1].year > key_lst[j].year:
                key_lst[j], key_lst[j-1] = key_lst[j-1], key_lst[j]
                j-=1

    return period_dict


def plotHPI(data, regionList):
    pass


def plot_whiskers(data, regionList):
    pass


def main():
    data = i.read_zip_house_price_data("data/HPI_AT_ZIP5.txt")
    yvalues = build_plottable_array([i for i in range(1999, 2012)], data["16034"])
    print(yvalues)

main()