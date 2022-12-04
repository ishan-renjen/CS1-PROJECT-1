"""
Ishan Renjen
CS141-7
Project 1 - Trending.py
"""

import index_tools as i

def cagr(idxlist, periods):
    HPI0 = idxlist[0]
    HPI1 = idxlist[1]

    CAGR = (((HPI1/HPI0)**(1/periods))-1)*100

    return CAGR

def calculate_trends(data, year0, year1):
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

    tuple_list = list()
    for key in period_dict:
        unsorted_list = period_dict.get(key)
        idxlist = [float(unsorted_list[0].idx), float(unsorted_list[-1].idx)]
        rate = cagr(idxlist, year1-year0)
        tuple_list.append(tuple((key, rate)))

    for mark in range(1, len(tuple_list)):
        j=mark
        while j>0 and tuple_list[j-1][1] > tuple_list[j][1]:
            tuple_list[j], tuple_list[j-1] = tuple_list[j-1], tuple_list[j]
            j-=1

    tuple_list = tuple_list[::-1]

    return tuple_list


def main():
    filename = "data/HPI_PO_state.txt"
    #input("enter filename: ")
    start_year = 2003
    #input("enter starting year: ")
    end_year = 2016
    #input("enter end year: ")
    data = i.read_zip_house_price_data(filename)
    annualized = i.annualize(data)
    sorted_data = calculate_trends(annualized, start_year, end_year)
    print(sorted_data)
    i.print_ranking(sorted_data, str(start_year)+"-"+str(end_year)+" Compound Annual Growth Rate\n")


if __name__ == "__main__":
    main()