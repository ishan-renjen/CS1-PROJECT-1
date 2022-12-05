"""
cs141-7
Ishan Renjen, inr8842
Project - trending.py
TASK 2 - creates tuples with (region, compound annual growth rate) over the given time period using AnnualHPI objects
12/5/2022
"""


import index_tools as i


def cagr(idxlist, periods):
    """
    purpose:
        computes compound annual growth rate

    parameters:
        idxlist must be a list of 2 values with index of 0 being object.index at year0, index of 1 being object.index at year1
        periods must be an int, range between year0 and year1

    returns:
        compound annual growth rate

    prints nothing
    """
    HPI0 = idxlist[0]
    HPI1 = idxlist[1]

    CAGR = (((HPI1/HPI0)**(1/periods))-1)*100

    return CAGR


def calculate_trends(data, year0, year1):
    """
    purpose:
        creates a list of tuples (region, compound annual growth rate)

    parameters:
        data must be dictionary with key -> region, str | value -> list of AnnualHPI objects

    returns list of tuples

    prints nothing
    """
    period_dict = dict()
    templist_years = list()
    # pre=0
    # post=0
    for key in data:
        data_list = data.get(key)
        for item in data_list:
            templist_years.append(int(item.year))

        if int(year0) in templist_years and int(year1) in templist_years:
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

    tuple_list = list()
    for key in period_dict:
        unsorted_list = period_dict.get(key)
        idxlist = [float(unsorted_list[0].idx), float(unsorted_list[-1].idx)]
        rate = cagr(idxlist, (int(year1)-int(year0)))
        tuple_list.append(tuple((key, rate)))

    for mark in range(1, len(tuple_list)):
        j=mark
        while j>0 and tuple_list[j-1][1] > tuple_list[j][1]:
            tuple_list[j], tuple_list[j-1] = tuple_list[j-1], tuple_list[j]
            j-=1

    tuple_list = tuple_list[::-1]

    return tuple_list


def main():
    """
    main function
    contains all the function calls and main formatting
    returns nothing
    prints all function returns and formatting details
    """
    filename = input("enter filename: ")
    start_year = int(input("enter starting year: "))
    end_year = int(input("enter end year: "))
    if "ZIP5" not in filename:
        data = i.read_state_house_price_data(filename)
    elif "ZIP5" in filename:
        data = i.read_zip_house_price_data(filename)
    annualized = i.annualize(data)
    sorted_data = calculate_trends(annualized, start_year, end_year)
    i.print_ranking(sorted_data, str(start_year)+"-"+str(end_year)+" Compound Annual Growth Rate\n")


if __name__ == "__main__":
    main()