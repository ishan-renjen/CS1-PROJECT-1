"""
Ishan Renjen
Project 1
CS141-7
timeline_plot.py
"""


import index_tools as i
import numpy.ma as ma
import matplotlib.pyplot as plt


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
            value_list.append(0)
            mask_list.append(True)
    final_array = ma.masked_array(value_list, mask_list)
    return final_array


def filter_years(data, year0, year1):
    year0 = int(year0)
    year1 = int(year1)
    filtered_dict = dict()

    for key in data:
        data_list = data[key]
        templist = []
        for item in data_list:
            if int(item.year) >= int(year0) and int(item.year) <= int(year1):
                templist.append(item)
        filtered_dict[key] = templist
    return filtered_dict


def plotHPI(data, regionList):
    year_set = set()
    for key in data:
        data_list = data.get(key)
        for item in data_list:
            year_set.add(int(item.year))

    year_list = sorted(list(year_set))

    plt.title('Home Price Indices: ' + str(year_list[0])  + " - " + str(year_list[-1]))
    plt.ylabel('Index')
    plt.xlabel("Year")
    for key in regionList:
        data_list = data[key]
        values = build_plottable_array(year_list, data_list)
        plt.plot(year_list, values, label=key, marker='*', linestyle='-')

    plt.legend()
    plt.show()


def plot_whiskers(data, regionList):
    plt.title('Home Price Index Comparison. Median is a line. Mean is a triangle.')
    plt.ylabel('Index')
    plt.xlabel("Region")

    year_set = set()
    value_list = list()
    for key in data:
        data_list = data.get(key)
        for item in data_list:
            year_set.add(int(item.year))

    year_list = sorted(list(year_set))

    for key in regionList:
        data_list = data[key]
        values = build_plottable_array(year_list, data_list)
        value_list.append(values)
    
    plt.boxplot(value_list, labels=regionList, showmeans=True)

    plt.show()


def main():
    filename = input("enter file: ")
    if "ZIP5" not in filename:
        unsorted = i.read_state_house_price_data(filename)
        unsorted = i.annualize(unsorted)
    elif "ZIP5" in filename:
        unsorted = i.read_zip_house_price_data(filename)
    
    start_year = int(input("enter start year: "))
    end_year = int(input("enter start year: "))
    regionlist = list()
    region = input("Enter next region for plots (<ENTER> to stop): ")
    while region != "":
        regionlist.append(region)
        region = input("Enter next region for plots (<ENTER> to stop): ")

    filtered = filter_years(unsorted, start_year, end_year)
    for region in regionlist:
        i.print_range(i.index_range(filtered, region), region)

    plotHPI(filtered, regionlist)
    print("close display window to continue")
    plot_whiskers(filtered, regionlist)
    print("close display window to continue")


main()