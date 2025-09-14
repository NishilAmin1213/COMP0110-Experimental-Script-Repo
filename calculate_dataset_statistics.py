import os, pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from utils import *
from deprecated_terms import initial_deprecated_search_terms, secondary_deprecated_search_terms
# requires pip install matplotlib

def calc_length_and_keyword_stats(dataset, terms, map_terms=False):
    """
    Calculate length and keyword statistics for a dataset.
    :param dataset: Dataset (that has already been de-serialized)
    :param terms: Array of keyword terms used when building the dataset
    :param map_terms: Boolean to decide whether keyword terms need to be mapped to categories
    :return: Three dictionaries containing statistics
    """
    # Initialise variables for counts, to store lengths and for keyword based counts
    function_count = 0
    java_8_length_total = 0
    min_java_8_length = 9999
    max_java_8_length = 0
    java_8_lengths = []
    java_11_length_total = 0
    min_java_11_length = 9999
    max_java_11_length = 0
    java_11_lengths = []
    keyword_counts = {}

    # Iterate over each data item in the dataset
    for data_item in dataset:
        # Increment the function count
        function_count += 1

        # Get the length of the java 8 function
        java_8_length = data_item['java_8_function']['length']
        # Add this length to the java 8 length total
        java_8_length_total += java_8_length
        # Append this length to the java 8 lengths array
        java_8_lengths.append(java_8_length)
        # If the length is the maximum or minimum, then change the max or min value
        if java_8_length > max_java_8_length:
            max_java_8_length = java_8_length
        if java_8_length < min_java_8_length:
            min_java_8_length = java_8_length

        # Get the length of the java 11 function
        java_11_length = data_item['java_11_function']['length']
        # Add this length to the java 11 length total
        java_11_length_total += java_11_length
        # Append this length to the java 11 lengths array
        java_11_lengths.append(java_11_length)
        # If the length is the maximum or minimum, then change the max or min value
        if java_11_length > max_java_11_length:
            max_java_11_length = java_11_length
        if java_11_length < min_java_11_length:
            min_java_11_length = java_11_length

        # Iterate over keywords
        for keyword in terms:
            # Check if a keyword is in the java 8 string
            if keyword in data_item['java_8_function']['string']:
                # Map the keyword to a category (if the flag is set to True)
                if map_terms:
                    keyword = categorize(keyword)

                # Try and increment the value of the counter in the keyword_counts dict for the keyword key
                # If there is a key error, the keyword it not a key, so create the item and set the value to 1
                try:
                    keyword_counts[keyword] = keyword_counts[keyword] + 1
                except KeyError:
                    keyword_counts[keyword] = 1

    # Initialise a dictionary to store the statistics for the java functions and the keywords
    java_8_stats = {}
    java_11_stats = {}
    keyword_distribution = {}

    # Store java 8 statistics to a dictionary
    java_8_stats['average_length'] = java_8_length_total / function_count
    java_8_stats['maximum_length'] = max_java_8_length
    java_8_stats['minimum_length'] = min_java_8_length
    java_8_lengths.sort()
    java_8_stats['lengths'] = java_8_lengths

    # Store java 11 statistics to a dictionary
    java_11_stats['average_length'] = java_11_length_total / function_count
    java_11_stats['maximum_length'] = max_java_11_length
    java_11_stats['minimum_length'] = min_java_11_length
    java_11_lengths.sort()
    java_11_stats['lengths'] = java_11_lengths

    # Calculate keyword percentages and store them for each keyword
    # CHECK THIS - COULD BE INCORRECT LOGIC
    for keyword in keyword_counts.keys():
        percentage = ((keyword_counts[keyword] / function_count) * 100)
        keyword_distribution[keyword] = percentage

    # Output some statistics
    print("\nAverage Java 8 Function Length: " + str(java_8_stats['average_length']))
    print("Maximum Java 8 Function Length: " + str(java_8_stats['maximum_length']))
    print("Minimum Java 8 Function Length: " + str(java_8_stats['minimum_length']))

    print("\nAverage Java 11 Function Length: " + str(java_11_stats['average_length']))
    print("Maximum Java 11 Function Length: " + str(java_11_stats['maximum_length']))
    print("Minimum Java 11 Function Length: " + str(java_11_stats['minimum_length']))

    # Return the statistics
    return java_8_stats, java_11_stats, keyword_distribution


def plot_distribution_pie(keyword_distribution, text):
    """
    Function to plot a pie chart to visualise the distribution of deprecated keywords in the dataset
    :param keyword_distribution: dictionary with keywords as keys and the percentages as the value
    :param text: text for the figures filename
    :return: None
    """

    # Get the keys from the keyword_distribution (the labels)
    keys = keyword_distribution.keys()
    # Initialise arrays for values and legend strings
    vals = []
    legend = []

    # Populate the values and legend array
    for key in keys:
        vals.append(keyword_distribution[key])
        legend.append(key + " - " + str(round(keyword_distribution[key], 2)) + "%")

    # Create a figure
    plt.figure(figsize = (9, 5), dpi=150)
    # Shrink the pie radius
    plt.pie(vals, radius=0.75)
    # Include the legend
    plt.legend(legend, title="KEY", loc="upper right")
    # General Formatting
    plt.axis('equal')
    plt.tight_layout()
    # Save the plot to an svg file
    plt.savefig('Term Distribution - ' + text + '.svg')



def plot_boxplot(java_8_stats, java_11_stats, filename):
    """
    Function to plot two boxplots for the functions lengths across the dataset
    :param java_8_stats: Dictionary holding data about functions lengths in the dataset
    :param java_11_stats: Dictionary holding data about functions lengths in the dataset
    :param filename: filename to save the figure as
    :return: None
    """

    # Create a figure
    plt.figure(figsize=(9, 5), dpi=150)

    # Plot the box plots with optimised styling
    boxplt = plt.boxplot([java_8_stats['lengths'], java_11_stats['lengths']], patch_artist=True, vert=False, whis=1.5, showfliers=False)

    # Customize Boxplot Colours
    for patch in boxplt['boxes']:
        patch.set_facecolor('skyblue')
        patch.set_alpha(0.7)


    # Set Axes Labels
    plt.yticks([1, 2], ['Java 8', 'Java 11'])

    # Create Legend Items
    legend_elements = [
        Patch(facecolor='white', label='Java 8 IQR: ' + str(round(np.percentile(java_8_stats['lengths'], 75) - np.percentile(java_8_stats['lengths'], 25), 2)) + ',    Java 11 IQR: ' + str(round(np.percentile(java_11_stats['lengths'], 75) - np.percentile(java_11_stats['lengths'], 25), 2))),
        Patch(facecolor='white', label='Java 8 Median: ' + str(round(np.percentile(java_8_stats['lengths'], 50), 2)) + ',    Java 11 Median: ' + str(round(np.percentile(java_11_stats['lengths'], 50), 2))),
        Patch(facecolor='white', label='Java 8 Mean: ' + str(round(java_8_stats['average_length'], 2)) + ',    Java 11 Mean: ' + str(round(java_11_stats['average_length'], 2))),
        Patch(facecolor='white', label='Java 8 Range: ' + str(java_8_stats['maximum_length'] - java_8_stats['minimum_length']) + ',    Java 11 Range: ' + str(java_11_stats['maximum_length'] - java_11_stats['minimum_length'])),
    ]

    # Plot the Legend
    plt.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

    # Make the figure look better
    plt.tight_layout(w_pad=0.5, h_pad=0.5)

    # Save the figure as an SVG
    plt.savefig(filename + '.svg')


if __name__ == "__main__":
    # This file uses the dataset pkl files to output statistics about the dataset
    # It can also accept the result datasets as they also contain the same information

    # Process the secondary dataset
    print("Processing the Secondary Dataset")
    # Read the dataset from the pickle file
    secondary_dataset = read_dataset("secondary_dataset.pkl")
    # Output the total number of functions
    print("Total Number of Functions: " + str(len(secondary_dataset)))
    # Calculate the statistics using the calc_length_and_keyword_stats function
    java_8_stats, java_11_stats, keyword_distribution = calc_length_and_keyword_stats(secondary_dataset, secondary_deprecated_search_terms, map_terms=True)
    # Plot the keyword distribution pie chart
    plot_distribution_pie(keyword_distribution, "Secondary Dataset")
    # Plot the boxplot for function lengths
    plot_boxplot(java_8_stats, java_11_stats, "Function Length Boxplot - Secondary Dataset")

    # Process the full dataset
    print("\n\n\nProcessing the Full Dataset")
    # Read the same param and different param dataset pickle files
    same_param_functions = read_dataset("same_param_functions_dataset.pkl")
    different_param_functions = read_dataset("different_param_functions_dataset.pkl")
    # Combine the two datasets into one
    combined_dataset = same_param_functions + different_param_functions
    # Output the total number of functions across both datasets and for each dataset
    print("Total Number of Functions: " + str(len(combined_dataset)))
    print("Number of 'Same Parameter Length' Functions: " + str(len(same_param_functions)))
    print("Number of 'Different Parameter Length' Functions : " + str(len(different_param_functions)))

    # Get statistics using the calc_length_and_keyword_stats function
    java_8_stats, java_11_stats, keyword_distribution = calc_length_and_keyword_stats(combined_dataset, initial_deprecated_search_terms)
    # Plot the pie chart of keyword distribution
    plot_distribution_pie(keyword_distribution, "Full Dataset")
    # Plot the boxplot of function lengths
    plot_boxplot(java_8_stats, java_11_stats, "Function Length Boxplot - Full Dataset")




