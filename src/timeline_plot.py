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
    years = dict()
    for i in regiondata:
        years[int(i.year)] = i.idx

    value_list = []
    mask_list = []
    for year in xyears:
        if year in years:
            value_list.append(float(years[year]))
            mask_list.append(False)
        if year not in years:
            value_list.append(None)
            mask_list.append(True)
    final_array = ma.masked_array(value_list, mask_list)
    return final_array


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
            while j>0 and lst_values[j-1].year > lst_values[j].year:
                lst_values[j], lst_values[j-1] = lst_values[j-1], lst_values[j]
                j-=1

    return period_dict


def plotHPI(data, regionList):
    plt.title('Using masked arrays')
    plt.ylabel('Indices')
    plt.xlabel("Years")

    year_list = list()
    for obj in data[regionList[0]]:
        year_list.append(int(obj.year))

    for key in regionList:
        data_list = data.get(key)
        values = build_plottable_array(year_list, data_list)
        plt.plot(year_list, values, label=key)

    plt.legend()
    plt.show()


def plot_whiskers(data, regionList):
    plt.title('Using masked arrays')
    plt.ylabel('Indices')
    plt.xlabel("Years")

    year_list = list()
    for obj in data[regionList[0]]:
        year_list.append(int(obj.year))

    value_list = []
    for key in regionList:
        data_list = data.get(key)
        values = build_plottable_array(year_list, data_list)
        value_list.append(values)
    
    plt.boxplot(value_list, labels=regionList)

    plt.show()


def main():
    data = i.read_state_house_price_data("data/HPI_PO_state.txt")
    data = i.annualize(data)
    start_year = 1995
    end_year = 2005
    regionlist = list()
    region = input("Enter next region for plots (<ENTER> to stop): ")
    while region != "":
        regionlist.append(region)
        region = input("Enter next region for plots (<ENTER> to stop): ")

    filtered = filter_years(data, start_year, end_year)
    print(filtered)
    for region in regionlist:
        i.print_range(i.index_range(filtered, region), region)

    plotHPI(filtered, regionlist)
    print("close display window to continue")
    plot_whiskers(filtered, regionlist)
    print("close display window to continue")


main()