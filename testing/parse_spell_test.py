"""
This script randomly picks a letter in the post and either removes it or replaces 
it with another word.
This is used to test whether the spell correction works, or whether our search will
still be accurate even with mispellings
"""
import random
import string
def remove_one_letter(read_data):
    test_cases = random.sample(read_data, 10)
    modifyed_cases = []
    for case in test_cases:
        index = random.randrange(len(case)-1)
        result_str = ""
        for i in range(len(case)):
            if i != index:
                result_str = result_str + case[i] 
            else:
                result_str = result_str 
        modifyed_cases.append(result_str)
    return (modifyed_cases,test_cases)

def replace_one_letter(read_data):
    test_cases = random.sample(read_data, 10)
    modifyed_cases = []
    for case in test_cases:
        index = random.randrange(len(case)-1)
        result_str = ""
        for i in range(len(case)):
            if i != index:
                result_str = result_str + case[i] 
            else:
                result_str = result_str + random.choice(string.ascii_lowercase)
        modifyed_cases.append(result_str)
    return (modifyed_cases,test_cases)