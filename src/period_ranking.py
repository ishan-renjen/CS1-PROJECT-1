"""
ishan renjen
CS141 Project 1
TASK 1 - period ranking.py
START ON PG. 13
"""

import index_tools as i

def quarter_data(data, year, qtr):
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
    filename = "data/HPI_PO_state.txt"
    #input("Enter region-based house price index filename: ")
    year = 1998
    #input("Enter year of interest for house prices: ")

    if "ZIP5" not in filename:
        unsorted = i.read_state_house_price_data(filename)
        #need to annualize it
    elif "ZIP5" in filename:
        unsorted = i.read_zip_house_price_data(filename)
    annualized_data = i.annualize(unsorted)
    sorted_data = annual_data(annualized_data, year)
    i.print_ranking(sorted_data, str(year)+" annual rankings:\n")


main_period()