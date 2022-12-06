"""
cs141-7
Ishan Renjen, inr8842
Project - index_tools.py
TASK 0 - creates the functions and dataclasses that are used in later files
12/5/2022
"""

from dataclasses import dataclass


@dataclass
class QuarterHPI:
    """
    purpose: 
        an object representing one quarter of one year of the dataset
    attributes:
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
    purpose: 
        an object representing one year of the dataset
    attributes:
        year: an integer representing the year of the index value.
        index: a float representing the home price index
    """
    year: int
    idx: float


def read_state_house_price_data(filepath):
    """
    purpose:
        reads a state text file and turns it into a dictionary described below

    returns:
        dictionary mapping state abbreviation to lists of QuarterHPI Objects
            key = state abbreviation -> str
            value = list of quarterHPI Objects -> list -> [QuarterHPI, QuarterHPI, etc...]

    prints:
        warning message when data is unavailable
            -Message contains text "data unavailable"
            -prints the line content on the next line
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
                quarter = QuarterHPI(int(year), int(qtr), float(index))

                if state in state_dict:
                    state_dict[state].append(quarter)
                else:
                    state_dict[state] = [quarter]

    return state_dict


def read_zip_house_price_data(filepath):
    """
    purpose:
        reads a zip5 text file and turns it into a dictionary described below

    returns: 
        A dictionary mapping zip codes to lists of AnnualHPI objects
            1 zip code -> list of objects -> [AnnualHPI, AnnualHPI, ...] 

    prints: 
        a count of lines counted, lines uncounted 
            -there are unavailable or incomplete values.
    """
    zip_dict = dict()
    counted = 0
    uncounted = 0

    with open(filepath, "r") as f:
        file = f.readlines()

        if file[0][:4] == "Five":
            file = file[1:]

        for line in file:
            lst = line.strip().split("\t")
            zip = lst[0]
            year = lst[1]
            index = lst[3]

            if index == ".":
                uncounted += 1

            if index != ".":

                annual = AnnualHPI(int(year), float(index))

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
    purpose:
        creates a tuple of the low and high values of the inputted data range for the given region

    parameters: 
        dictionary -> key = region, str | value = list of HPI objects
            -can be quarter or annualHPI

    returns: 
        A tuple of the HPI objects - (low value, high value)

    no printed output
    """
    high = data[region][0]
    low = data[region][0]

    for x in data[region]:
        if float(x.idx) > float(high.idx):
            high = x
        elif float(x.idx) < float(low.idx):
            low = x

    return low, high


def print_range(data, region):
    """
    purpose:
        prints the tuple from index_range in a formatted manner

    parameters: 
        list/tuple of low and high values

    returns nothing

    prints: 
        Prints low and high values of the house price index for given region in the given format
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
    purpose:
        prints given data in a rank - top 10 and bottom 10

    parameters: 
        data is sorted, heading is str

    returns nothing

    prints:
        table of processed data
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
    purpose:
        takes QuarterHPI objects per year and combines them into AnnualHPI objects - useful for state files

    parameters: 
        dictionary -> key, str -> region | value, list of QuarterHPI objects per region

    returns: 
        dictionary -> key, str -> region | value, list of Annual objects per region

    prints nothing
    """
    new_value = list()
    annual_dict = dict()

    for key in data:
        value = data.get(key)

        for mark in range(1, len(value)):
            j = mark

            while j > 0 and value[j-1].year > value[j].year:
                value[j], value[j-1] = value[j-1], value[j]
                j -= 1

        while len(value) != 0:
            idx = 0
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
            sum_idx = 0

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
    """
    main function
    contains all the function calls and main formatting
    returns nothing
    prints all function returns and formatting details
    """
    filename = input("enter house price index file: ")
    if "data/" not in filename:
        filename = ("data/"+filename)

    if "state" in filename:
        unsorted = read_state_house_price_data(filename)
    else:
        unsorted = read_zip_house_price_data(filename)

    regionList = []
    region = input("enter state abbreviation or zip code: ")

    while region is not "":
        regionList.append(region)
        region = input("enter state abbreviation or zip code: ")

    for region in regionList:
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
    """MAIN GUARD"""
    main_index()
