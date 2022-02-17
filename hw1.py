# using regex to simplify reviews to only necessary words
import re

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
stop_words = ["THE","A"]


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
        unfiltered_review_words = re.findall(r"[a-zA-Z]+",line)
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

# scans test file and gives sentiment to review based on training data
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
        unfiltered_review_words = re.findall(r"[a-zA-Z]+",line)
        # remove suppressed words
        review_words = [word for word in unfiltered_review_words if word not in stop_words]
        
        # main classification algorithm
        rating = []
        for word in review_words:
            pos_degree = 0
            neg_degree = 0
            entry_element = 0
            
            if word in positive_associated_words:
                pos_degree = positive_associated_words[word]
            else:
                ratio = pos_degree
                rating.append(ratio)
                continue
            if word in negative_associated_words:
                neg_degree = negative_associated_words[word]
            else:
                ratio = neg_degree * (-1)
                rating.append(ratio)
                continue
            
            if pos_degree == neg_degree:
                ratio = 0
                rating.append(ratio)
                continue
            elif pos_degree > neg_degree:
                ratio = pos_degree / neg_degree
            elif neg_degree > pos_degree :
                ratio = neg_degree / pos_degree * (-1)
            
            entry_element = ratio
            rating.append(entry_element)
        
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

# runs the training
create_plot()
# runs the test
run_test()
input("Press Enter to continue...")

