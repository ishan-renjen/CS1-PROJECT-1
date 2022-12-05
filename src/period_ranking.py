"""
cs141-7
Ishan Renjen, inr8842
Project - period_ranking.py
TASK 1 - creates tuples for quarterHPI and AnnualHPI objects with (region, index)
12/5/2022
"""

import index_tools as i

def quarter_data(data, year, qtr):
    """
    purpose:
        to create a list of tuples containing (region, index) corresponding to the given year and quarter

    parameters:
        data must be dictionary of key -> region, str | value -> list of QuarterHPI objects, [QuarterHPI, ...]

    returns:
        list of tuples following (region, index) corresponding to the given year and quarter

    prints nothing
    """
    quarter_dict = dict()
    tuple_list = list()
    quarter_list = []

    for i in data:
        data_list = data.get(i)

        for x in data_list:
            if x.year == str(year) and x.qtr == str(qtr):
                if i in quarter_dict:
                    quarter_dict[i] += [x.idx]
                else:
                    quarter_dict[i] = [x.idx]

    for key in quarter_dict:
        quarter_list.append([key, quarter_dict[key]])

    for item in range(len(quarter_list)):
        state = quarter_list[item][0]
        index_lst = quarter_list[item][1]
        for idx in index_lst:
            temp_tuple = tuple((state, float(idx)))
            tuple_list.append(temp_tuple)
        
    for mark in range(1, len(tuple_list)):
        j=mark
        while j>0 and tuple_list[j-1][1] > tuple_list[j][1]:
            tuple_list[j], tuple_list[j-1] = tuple_list[j-1], tuple_list[j]
            j-=1

    tuple_list = tuple_list[::-1]
    return tuple_list


def annual_data(data, year):
    """
    purpose:
        to create a list of tuples containing (region, index) corresponding to the given year

    parameters:
        data must be dictionary of key -> region, str | value -> list of AnnualHPI objects, [AnnualHPI, ...]

    returns:
        list of tuples following (region, index) corresponding to the given year

    prints nothing
    """
    annual_dict = dict()
    tuple_list = list()
    annual_list = []

    for i in data:
        data_list = data.get(i)

        for x in data_list:
            if x.year == str(year):
                if i in annual_dict:
                    annual_dict[i] += [x.idx]
                else:
                    annual_dict[i] = [x.idx]

    for key in annual_dict:
        annual_list.append([key, annual_dict[key]])

    for item in range(len(annual_list)):
        state = annual_list[item][0]
        index_lst = annual_list[item][1]
        for idx in index_lst:
            temp_tuple = tuple((state, float(idx)))
            tuple_list.append(temp_tuple)
        
    for mark in range(1, len(tuple_list)):
        j=mark
        while j>0 and tuple_list[j-1][1] > tuple_list[j][1]:
            tuple_list[j], tuple_list[j-1] = tuple_list[j-1], tuple_list[j]
            j-=1

    tuple_list = tuple_list[::-1]
    return tuple_list


def main_period():
    """
    main function
    contains all the function calls and main formatting
    returns nothing
    prints all function returns and formatting details
    """
    filename = input("Enter region-based house price index filename: ")
    year = input("Enter year of interest for house prices: ")

    if "ZIP5" not in filename:
        unsorted = i.read_state_house_price_data(filename)
    elif "ZIP5" in filename:
        unsorted = i.read_zip_house_price_data(filename)
    annualized_data = i.annualize(unsorted)
    sorted_data = annual_data(annualized_data, year)
    i.print_ranking(sorted_data, str(year)+" annual rankings:\n")


if __name__ == "__main__":
    """MAIN GUARD"""
    main_period()