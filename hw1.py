# using regex to simplify reviews to only necessary words
import re

# library to visualize the data
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# https://seaborn.pydata.org/tutorial/axis_grids.html

# The file names of the training and testing files
training_file = "1643859451_1934268_train_new_20220201.txt"
testing_file = "1643859451_3370469_test_new_20220201.txt"
output_file = "hw1_output.txt"
stop_words_file = "stop_words.txt"

# dicts for "training" data that are mapped as such:    key:val -> word:count
positive_associated_words = {} # number of times the word appears in positive reviews
negative_associated_words = {} # number of times the word appears in negative reviews
# TODO merge the two dicts as one with a tuple as value for pos/neg

# list of words not to consider during training (stop words)
def gen_stop_words():
    stop_words_file_obj = open(stop_words_file, "r", encoding="utf-8")
    generated_stop_words = stop_words_file_obj.readlines()
    stop_words_file_obj.close()
    return generated_stop_words
print("started stop_words generation")
#stop_words = ["THE","A"]
stop_words = gen_stop_words()

# data visualization fields (for panda and seaborn libraries)
# column variables for the datatable (panda)
review_index = []
positive_count = []
negative_count = []
def add_record(x, y, z):
    review_index.append(x)
    positive_count.append(y)
    negative_count.append(z)


# Creates the dictionaries of positively/negatively "associated" words
# (associated being the words appeared in the corresponding review)
def create_plot():
    print("running create_plot()")

    # open training file
    train_file = open(training_file, "r", encoding="utf-8")
    
    # "training" portion
    # each iteration reads a new line and thus a new review
    while (1):
        line = train_file.readline()
        if (line == ""):
            break
        # sentiment is +1 or -1 so only sign matters
        sentiment = line[0]
        # removes contraction punctuation ' and truncates by removing sentiment and tab
        line = re.sub("\'","",line[3:])
        # removes html breaks and capitalizes all words
        line = re.sub("<br \/>","",line).upper()
        # list of words in the review
        unfiltered_review_words = re.findall(r"[a-zA-Z][a-zA-Z]+",line)
        # remove suppressed words
        review_words = [word for word in unfiltered_review_words if word not in stop_words]
        
        # iterates through each word and adds them to correlated dict
        for word in review_words:
            if (sentiment == "+"):
                if word in positive_associated_words:
                    positive_associated_words[word] += 1
                else:
                    positive_associated_words[word] = 1
            elif (sentiment == "-"):
                if word in negative_associated_words:
                    negative_associated_words[word] += 1
                else:
                    negative_associated_words[word] = 1
    
    # close training file
    train_file.close()
    
    print(f"finished create_plot() with {len(positive_associated_words)} positive words and {len(negative_associated_words)} negative words")



# scans test file and assigns sentiment to review based on training data
def run_test():
    print("running run_test()")
    
    # open test and output files
    test_file = open(testing_file, "r", encoding="utf-8")
    out_file = open(output_file, "w")
    # string to write in output file
    output_string = ""
    
    # testing portion
    while (1):
        line = test_file.readline()
        if (line == ""):
            break
        # removes contraction punctuation ' and removes html breaks then capitalizes all words
        line = re.sub("\'|(<br \/>)","",line).upper()
        # list of words in the review
        review_words = re.findall(r"[a-zA-Z][a-zA-Z]+",line)
        
        # main classification algorithm
        rating = []
        review_index = 0 # current iteration number (corresponds to review index)
        for word in review_words:
            pos_degree = 0
            neg_degree = 0
            entry_element = 0
            
            # get the word's positive and negative training data frequency list
            if word in positive_associated_words:
                pos_degree = positive_associated_words[word]
            if word in negative_associated_words:
                neg_degree = negative_associated_words[word]
            
            # quick data visualization (panda) record insertion
            add_record(review_index, pos_degree, neg_degree)
            
            # associate a ratio with the current word
            if pos_degree == neg_degree: # if the word is perfectly ambiguous
                ratio = 0
                rating.append(ratio)
                continue
            elif pos_degree > neg_degree: # if the word seems to have positive connotation
                if neg_degree == 0:
                    ratio = pos_degree
                else:
                    ratio = pos_degree / neg_degree
            elif neg_degree > pos_degree: # if the word seems to have negative connotation
                if pos_degree == 0:
                    ratio = neg_degree * (-1)
                else:
                    ratio = neg_degree / pos_degree * (-1)
            
            # Setting a threshold for considering the word
            threshold_ratio = 1.8 # there must be at least 2 times the considered connotation vs the opposite
            if ratio < threshold_ratio and ratio > threshold_ratio * (-1):
                entry_element = 0
            else:
                entry_element = ratio
            rating.append(entry_element)
            
            review_index += 1
            # End of iteration
        
        # Sums up the ratings of each word from the review
        summation = sum(rating)
        if summation >= 0:
            output_string += "+1\n"
        else:
            output_string += "-1\n"
    
    # writes test output to file
    out_file.write(output_string)
    
    # close test and output files
    test_file.close()
    out_file.close()
    
    print("finished run_test()")


# main function calls

# runs the training
create_plot()
# runs the test
run_test()



# -- Data Visualization Section --
print("Starting data visualization")

# open test and output files
test_file = open(testing_file, "r", encoding="utf-8")
# use panda library to create a long-form datatable
visual_testing_set = pd.DataFrame({"review_index": review_index, "positive_degree": positive_count, "negative_degree": negative_count})
# plot the datatable
#regression_graph = sns.regplot(x="negative_degree", y="positive_degree", data=visual_testing_set)
multiple_graph = sns.FacetGrid(visual_testing_set, col="review_index", margin_titles=True)
multiple_graph.map(sns.regplot, "negative_degree", "positive_degree")
plt.show() # show matlab graph window

