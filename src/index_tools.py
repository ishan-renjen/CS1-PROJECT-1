"""
cs141-7
Ishan Renjen
Project - index_tools.py
TASK 0 - pg.7-12
"""

from dataclasses import dataclass

@dataclass
class QuarterHPI:
    """
    P. 7
    year: an integer representing the year of the index value.
    qtr: an integer representing the quarter of the year.
    index: a float representing the home price index
    """
    year: int
    qtr: int
    idx: float


@dataclass
class AnnualHPI:
    """
    p. 7
    year: an integer representing the year of the index value.
    index: a float representing the home price index
    """
    year: int
    idx: float


def read_state_house_price_data(filepath):
    """
    P. 7-8
    return dictionary mapping state abbreviation to lists of QuarterHPI Objects
        key = state abbreviation
        value = list of quarterHPI Objects

    Printed Output: warning message when data is unavailable. Message contains 
    text "data unavailable", then prints the line content on the next line - see
    example on pg. 8
    """
    state_dict = dict()
    with open(filepath, "r") as f:
        file = f.readlines()
        if file[0][:5] == "state":
            file = file[1:]
        for line in file:
            lst = line.strip().split("\t")
            state = lst[0]
            year = lst[1]
            qtr = lst[2]
            index = lst[3]

            if index == ".":
                print("data unavailable: \n" + str(lst) + "\n")
            else:
                quarter = QuarterHPI(year, qtr, index)

                if state in state_dict:
                    state_dict[state].append(quarter)
                else:
                    state_dict[state] = [quarter]

    return state_dict


def read_zip_house_price_data(filepath):
    """
    P. 8-9
    returns: A dictionary mapping zip codes to lists of AnnualHPI objects. For every zip
    code, there is exactly one list of AnnualHPI objects. 

    Printed Output: a count of lines read and lines uncounted due to unavailable or
    incomplete values.
    """
    zip_dict = dict()
    counted = 0
    uncounted = 0
    with open(filepath, "r") as f:
        file = f.readlines()
        file.pop(0)
        for line in file:
            lst = line.strip().split("\t")
            zip = lst[0]
            year = lst[1]
            index = lst[3]

            if index == ".":
                uncounted += 1

            if index != ".":

                annual = AnnualHPI(year, index)

                if zip in zip_dict:
                    zip_dict[zip] += [annual]
                    counted += 1
                else:
                    zip_dict[zip] = [annual]
                    counted += 1
                    
    print("counted: ", counted, " uncounted: ", uncounted)
    return zip_dict


def index_range(data, region):
    """
    P. 9
    parameters: A dictionary mapping regions to lists of *HPI4 objects and a region name. The
    objects may be either QuarterHPI or AnnualHPI objects.

    returns: A tuple of the *HPI objects that are respectively the low and high index values
    of the dataset.

    no printed output
    """
    high = data[region][0]
    low = data[region][0]
    for hpi in data[region]:
        if float(hpi.idx) < float(low.idx):
            low = hpi
        elif float(hpi.idx) > float(high.idx):
            high = hpi
    
    return low, high


def print_range(data, region):
    """
    P. 9
    parameters: A dictionary mapping regions to lists of *HPI objects and a region name

    returns NoneType

    printed output: Prints the low and high values (range) of the house price index for
    the given region. See the examples for the output format desired
    """
    print("\nRegion: " + str(region))
    if (type(data[0]) == QuarterHPI) == True:
        print("Low: year/quarter/index: " +
            str(data[0].year) + "/" + str(data[0].qtr) + "/" + str(data[0].idx), sep="")
        print("High: year/quarter/index: " +
            str(data[1].year) + "/" + str(data[1].qtr) + "/" + str(data[-1].idx))
    else:
        print("Low: year/index: " +
            str(data[0].year) + "/" + str(data[0].idx), sep="")
        print("High: year/index: " +
            str(data[1].year) + "/" + str(data[1].idx))

def print_ranking(data, heading="Ranking"):
    """
    P. 10
    parameters: The data is a sorted list of objects, and the heading is a text message whose
    default value is “Ranking”.

    returns NoneType

    prints table of processed data
    """
    length = len(data)

    print(heading,
          "\nThe Top 10\n",
          "1: " + str(data[0]), "\n",
          "2: " + str(data[1]), "\n",
          "3: " + str(data[2]), "\n",
          "4: " + str(data[3]), "\n",
          "5: " + str(data[4]), "\n",
          "6: " + str(data[5]), "\n",
          "7: " + str(data[6]), "\n",
          "8: " + str(data[7]), "\n",
          "9: " + str(data[8]), "\n",
          "10: " + str(data[9]), "\n",

          "\nThe Bottom 10\n",
          
          str(length-9) + ": " + str(data[-10]), "\n",
          str(length-8) + ": " + str(data[-9]), "\n",
          str(length-7) + ": " + str(data[-8]), "\n",
          str(length-6) + ": " + str(data[-7]), "\n",
          str(length-5) + ": " + str(data[-6]), "\n",
          str(length-4) + ": " + str(data[-5]), "\n",
          str(length-3) + ": " + str(data[-4]), "\n",
          str(length-2) + ": " + str(data[-3]), "\n",
          str(length-1) + ": " + str(data[-2]), "\n",
          str(length) + ": " + str(data[-1]))


def annualize(data):
    """
    P. 11
    parameters: A dictionary mapping regions to lists of QuarterHPI objects.

    returns: A dictionary mapping regions to lists of AnnualHPI objects. 

    no printed output
    """
    new_value = list()
    annual_dict = dict()
    for key in data:
        value = data.get(key)
        
        for mark in range(1, len(value)):
            j=mark

            while j>0 and value[j-1].year > value[j].year:
                value[j], value[j-1] = value[j-1], value[j]
                j-=1

        while len(value) != 0:
            idx=0
            year = value[0].year
            new_value = []
            while idx < len(value):
                if year == value[idx].year:
                    new_value.append(value[idx])
                    idx += 1
                else:
                    break
            value = value[idx:]
        
            templist = []
            sum_idx=0

            for item in new_value:
                templist.append(float(item.idx))

            sum_idx = sum(templist)

            mean = sum_idx/len(new_value)
            annual = AnnualHPI(year, mean)

            if key in annual_dict:
                annual_dict[key] += [annual]
            else:
                annual_dict[key] = [annual]
    
    return annual_dict


def main_index():
    filename = input("enter house price index file: ")
    region = input("enter state abbreviation or zip code: ")

    if len(region) == 2:
        unsorted = read_state_house_price_data(filename)
    else:
        unsorted = read_zip_house_price_data(filename)

    print(unsorted)

    print("==================================================\n")

    data = index_range(unsorted, region)
    print_range(data, region)

    annualized_data = annualize(unsorted)
    data = index_range(annualized_data, region)
    print_range(data, region)

    print("annualized index values for " + str(region)+"\n")
    region_data = annualized_data.get(region)
    for item in region_data:
        print(item)


if __name__ == "__main__":
    main_index()