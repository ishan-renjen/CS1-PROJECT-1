"""
cs141-7
Ishan Renjen, inr8842
Project - timeline_plot.py
TASK 3 - uses numpy, matplotlib, and index_tools.py to graph the data in a line graph and box plot, masking over missing data
12/5/2022
"""


import index_tools as i
import numpy.ma as ma
import matplotlib.pyplot as plt


def build_plottable_array(xyears, regiondata):
    """
    purpose:
        masks over the missing data points to create a plottable array

    parameters:
        xyears must be a list of years to check for
        regiondata is a list of AnnualHPI objects

    returns:
        plottable numpy masked array

    prints nothing
    """
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
    """
    purpose:
        removes years from given data that are not in the range year1-year0

    parameters:
        year1 and year0 must be real numbers
        data -> dictionary with key -> region, str | value -> list of AnnualHPI objects

    returns:
        dictionary with extra years removed

    prints nothing
    """
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


def plot_HPI(data, regionList):
    """
    purpose:
        plots the data from filter_years in a line graph

    parameters:
        regionlist -> list of regions from inputs in main, regions -> str
        data -> dictionary with key -> region, str | value -> list of AnnualHPI objects within the entered year range

    returns:
        nothing

    outputs:
        line graph with x as years and y as index for the given regions

    prints: 
        nothing
    """
    year_set = set()
    for key in data:
        data_list = data.get(key)
        for item in data_list:
            year_set.add(int(item.year))

    year_list = sorted(list(year_set))

    plt.title('Home Price Indices: ' +
              str(year_list[0]) + " - " + str(year_list[-1]))
    plt.ylabel('Index')
    plt.xlabel("Year")
    for key in regionList:
        data_list = data[key]
        values = build_plottable_array(year_list, data_list)
        plt.plot(year_list, values, label=key, marker='*', linestyle='-')

    plt.legend()
    plt.show()


def plot_whiskers(data, regionList):
    """
    purpose:
        plots the data from filter_years in a box plot

    parameters:
        regionlist -> list of regions from inputs in main, regions -> str
        data -> dictionary with key -> region, str | value -> list of AnnualHPI objects within the entered year range

    returns:
        nothing

    outputs:
        box plot with x as regions and y as index for the given regions, line is median and triangle is mean

    prints: 
        nothing
    """
    plt.title('Home Price Index Comparison. Median is a line. Mean is a triangle.')
    plt.ylabel('Index')
    plt.xlabel("Region")

    value_list = list()

    for key in regionList:
        data_list = data[key]
        value_idx = []
        for i in data_list:
            value_idx.append(i.idx)
        value_list.append(value_idx)
    plt.boxplot(value_list, labels=regionList, showmeans=True)

    plt.show()


def main_timeline():
    """
    main function
    contains all the function calls and main formatting
    returns nothing
    prints all function returns and formatting details
    """
    filename = input("enter file: ")
    if "data/" not in filename:
        filename = ("data/"+filename)
    if "state" in filename:
        unsorted_quarter = i.read_state_house_price_data(filename)
        unsorted = i.annualize(unsorted_quarter)
    else:
        unsorted = i.read_zip_house_price_data(filename)

    start_year = int(input("enter start year: "))
    end_year = int(input("enter start year: "))
    regionlist = list()
    region = input("Enter next region for plots (<ENTER> to stop): ")
    while region != "":
        regionlist.append(region)
        region = input("Enter next region for plots (<ENTER> to stop): ")

    filtered = filter_years(unsorted, start_year, end_year)

    if "state" in filename:
        for region in regionlist:
            i.print_range(i.index_range(unsorted_quarter, region), region)

    plot_HPI(filtered, regionlist)
    print("close display window to continue")
    plot_whiskers(filtered, regionlist)
    print("close display window to continue")


if __name__ == "__main__":
    """MAIN GUARD"""
    main_timeline()
