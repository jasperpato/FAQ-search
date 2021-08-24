import difflib
import time

def spell_correction(thread):

    thread_list = thread.split()

    word_file = open("LiterallyEveryWord.txt", "r")

    word_list = word_file.readlines()

    word_file.close()

    for i in range(0, len(word_list)):

        word_list[i] = word_list[i].strip()

    null_list = [None]*len(word_list)

    word_dict = dict(zip(word_list, null_list))

    corrected_list = []

    for thread_word in thread_list:

        #print(thread_word)

        best_similarity = 0
        best_match = ""

        start = time.time()
        if thread_word in word_dict.keys():

            #print("in dict")
            best_similarity = 1
            best_match = thread_word

            corrected_list.append(best_match)

            end = time.time()
            print("dict search time: ", end-start)

            continue
        start = time.time()
        for word in word_dict:
            startse = time.time()
            curr_similarity = difflib.SequenceMatcher(None, thread_word, word).ratio()
            endse = time.time()

            if curr_similarity > best_similarity:

                best_similarity = curr_similarity
                best_match = word

        corrected_list.append(best_match)
        end = time.time()
        print("sequence funtion time: ", endse-startse)
        print("sequence time: ", end-start)

    return " ".join(corrected_list)

def main():

    input_text = "Just wondering how we are expected to report termination of background processes? Currently I have a simple implementation printing to stderr process blah has terminated but noticed bash initially gives a process number and prints it and the pid, eg:"

    start = time.time()
    
    output_text = spell_correction(input_text)

    end = time.time()

    print(output_text)

    print(end-start)



    
