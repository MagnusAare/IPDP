import numpy as np
import matplotlib.pyplot as plt


def dataLoad(filename: str) -> np.ndarray():
    """Loads and filters data from a text file.
    The function will print the categories & indexes where errors where found.
    Input: string of text file name
    Output: Array of filtered data"""
    dataRaw = np.loadtxt(filename)
    conditions = [
        (10 > dataRaw[:, 0]) | (dataRaw[:, 0] < 60),  # Temperature
        dataRaw[:, 1] > 0,  # Growth Rate
        (dataRaw[:, 2] == 1)
        | (dataRaw[:, 2] == 2)
        | (dataRaw[:, 2] == 3)
        | (dataRaw[:, 2] == 4),  # Category
    ]
    errorTypes = ["Temperature", "Growth", "Categorization"]

    for i in range(3):
        print(
            f"{errorTypes[i]} errors found and removed at indexes: {np.where(np.invert(conditions[i]))[0]}"
        )

    data = dataRaw[conditions[0] & conditions[1] & conditions[2]]
    return data


def dataStatistics(data: np.ndarray, statistic: str):
    """Calculates chosen statistic, they following options are included:
    Mean & standard deviation of temperature and growth rate.
    Number of rows.
    Mean cold and hot growth rate.
    Input: Array of data, string of statistic.
    Output: value of statistic.
    """
    statDict = {
        "Mean Temperature": np.mean(data[:, 0]),
        "Mean Growth rate": np.mean(data[:, 1]),
        "Std Temperature": np.std(data[:, 0]),
        "Std Growth rate": np.std(data[:, 1]),
        "Rows": data.shape[0],
        "Mean Cold Growth rate": np.mean(data[data[:, 0] < 20][:, 1]),
        "Mean Hot Growth rate": np.mean(data[data[:, 0] > 50][:, 1]),
    }

    result = statDict[statistic]

    return result


def dataPlot(data: np.ndarray):
    """Creates two plots - One bar plot showcasing the number of each bacteria and one scatterplot showcasing the growth rate.
    Input: Array of data.
    Output: Two plots.
    """
    names = np.array(
        ["Salmonella", "Bacillus cereus", "Listeria", "Brochothrix\nthermosphacta"]
    )

    counts = np.zeros(4)
    color = np.array(["tab:blue", "tab:orange", "tab:green", "tab:red"])

    for i in range(1, 5):
        counts[i - 1] = np.count_nonzero(data[data[:, 2] == i])
    names, counts, color = names[counts != 0], counts[counts != 0], color[counts != 0]

    fig, ax = plt.subplots()

    ax.bar(names, counts, color=color)
    ax.set_title("Bar plot of bacteria types")
    ax.set_ylabel("Number of bacteria of given type")

    plt.show()

    fig, ax = plt.subplots()

    for i in range(len(counts)):
        ax.scatter(
            data[data[:, 2] == i + 1][:, 0],
            data[data[:, 2] == i + 1][:, 1],
            color=color[i],
        )

    ax.set_ylabel("Growth Rate")
    ax.set_xlabel("Temperature")
    ax.set_title("Growth rate of bacteria at different temperatures")
    ax.set_xlim(10, 60)
    ax.set_ylim(0)
    ax.legend(names)
    plt.show()


def dataFilter(data):
    done = False
    isValidTempLim = False
    isValidGrowthLim = False
    isValidCatLim = False
    filter = np.array([None] * 3)

    limitExplainer = (
        f"All data outside these limits will not be included in the dataset\n"
        f"(If these limits were set by mistake, the data will have to be reloaded)\n"
    )
    categoryExplainer = limitExplainer.replace("limits", "types")
    while not done:
        filterPrompt = (
            "Please choose which attribute you want to filter \n"
            "a. Temperature\n"
            "b. Growth rate\n"
            "c. Bacteria Type\n"
            'Or type "x" to exit when done\n'
        )
        f = input(filterPrompt)

        if f == "a":
            tempPrompt = (
                'Please enter your desired limits for temperature as two (2) numbers seperated by ","\n'
                '(Example: "10, 60")'
            )
            print(tempPrompt)
            while not isValidTempLim:
                try:
                    lim = np.array(input().split(","), dtype=float)
                    if lim.shape[0] != 2:
                        raise Exception
                    data = data[(lim[0] <= data[:, 0]) & (data[:, 0] <= lim[1])]
                    filter[0] = f"{lim[0]} <= Temp <= {lim[1]}"
                    print(
                        f"Temperature limits have been set to: {filter[0]}\n"
                        + limitExplainer
                    )
                    isValidTempLim = True

                except:
                    print("Not a valid input! >:(")
                    print(tempPrompt)

        if f == "b":
            growthPrompt = (
                'Please enter your desired limits for growth rate as two (2) non-negative numbers seperated by ","\n'
                '(Example: "0, 1")'
            )
            print(growthPrompt)
            while not isValidGrowthLim:
                try:
                    lim = np.array(input().split(","), dtype=float)
                    if lim.shape[0] != 2 or len(lim[lim < 0]) > 0:
                        raise Exception
                    filter[1] = f"{lim[0]} <= Growth rate <= {lim[1]}"
                    data = data[(data[:, 1] > lim[0]) & (data[:, 1] < lim[1])]
                    print(
                        f"Growth rate limits have been set to: {filter[1]}\n"
                        + limitExplainer
                    )
                    isValidGrowthLim = True
                except:
                    print("Not a valid input! >:(")
                    print(growthPrompt)

        if f == "c":
            catPrompt = (
                'Please enter your desired bacteria types to include as numbers seperated by "," corresponding'
                "to the following categories\n"
                "1. Salmonella enterica\n"
                "2. Bacillus cereus\n"
                "3. Listeria\n"
                "4. Brochothrix thermosphacta\n"
                '(Example: "1,2,3")'
            )
            print(catPrompt)
            while not isValidCatLim:
                tempdata = np.empty((0, 3))
                try:
                    lim = np.array(input().split(","), dtype=int)
                    if (
                        lim[(lim != 1) & (lim != 2) & (lim != 3) & (lim != 4)].shape[0]
                        != 0
                    ):
                        raise Exception
                    for c in lim:
                        tempdata = np.append(tempdata, data[data[:, 2] == c], axis=0)
                    filter[2] = f"Bacteria types: {lim}"
                    print(
                        f"Bacteria types have been set to {lim}\n" + categoryExplainer
                    )
                    data = tempdata
                    isValidCatLim = True
                except:
                    print("Not a valid input! >:(")
                    print(catPrompt)

        if f == "x":
            done = True

    return data, filter


def main():
    choice = None
    data = None
    filter = None
    print("Welcome to Bacteria Statistics (BS)")
    while choice != "x":
        if filter is not None:
            print("Active Filters are:\n")
            for f in filter[filter != None]:
                print(f)
        prompt = (
            "You have the following options \n"
            "1: Load data\n"
            "2: Filter data\n"
            "3: Show statistics for your data\n"
            "4: Generate figures\n"
            "x: Exit Program\n"
            "Please choose an option by entering the corresponding number :-P\n"
        )
        choice = input(prompt)

        if choice == "1":
            askedNicely = 0

            while data is None:
                try:
                    data = dataLoad(
                        input(
                            "Please enter a valid filename"
                            + " >:( " * askedNicely
                            + ":\n"
                        )
                    )
                except Exception as e:
                    askedNicely = 1
                    print("That is not a valid filename!")

        elif choice == "2":
            if data is not None:
                data, filter = dataFilter(data)

            else:
                print(
                    "No data is available to be filtered \n"
                    "Please load data via command 1 before proceeding\n"
                )

        elif choice == "3":
            if data is not None:
                done = False
                while not done:
                    statPrompt = (
                        "Which statistic do you want to generate?\n"
                        '"Mean Temperature": For the mean of the temperature data\n'
                        '"Std Temperature": For the standard deviation of the temperature data\n'
                        '"Std Growth rate": For the standard deviation of the growth rate data\n'
                        '"Rows": For the amount of rows/datapoints in the data\n'
                        '"Mean Cold Growth rate": For the mean growth rate of bacteria under 20 degrees\n'
                        '"Mean Hot Growth rate": For the mean growth rate of bacteria over 50 degrees\n'
                        'Or enter "x" to exit the Statistics Generator\n'
                    )
                    try:
                        stat = input(statPrompt)
                        if stat != "x":
                            print(stat + ":", dataStatistics(data, stat))
                        else:
                            done = True
                    except Exception as e:
                        print(stat + " is not a valid input")
            else:
                print(
                    "No data is available to be filtered \n"
                    "Please load data via command 1 before proceeding\n"
                )

        elif choice == "4":
            if data is not None:
                dataPlot(data)
            else:
                print(
                    "No data is available to be filtered \n"
                    "Please load data via command 1 before proceeding\n"
                )

        elif choice != "x":
            print(choice + "is not a valid input. Please listen. <3")
    print("Thank you for running BS <3")


main()
