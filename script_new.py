import json
# nfa_dict will store the json data from the file input.json
from typing import Set, Dict, List, Any, Union

with open('input.json', 'r') as file:
    nfa_dict = json.load(file)

# The format of the input is described by printing the key and value
for key, val in nfa_dict.items():
    print(key, "=>", val)

# dfa is the dictionary which will store the output of this program and finally stored in the output.json
dfa: Dict[str, Union[Union[List[Any], List[List[Union[Union[int, Set[Any]], Any]]]], Any]] = dict()

# filling the values of states, letters, start-state in the corresponding dfa
dfa["states"] = 2**nfa_dict["states"]
dfa["letters"] = nfa_dict["letters"]
dfa["start"] = nfa_dict["start"]

# Final states can't be directly assigned to the corresponding dfa, Hence an empty list is used,
# which is filled using the algorithm below
dfa["final"] = []

# Calculating final states in the dfa
for i in range(0, dfa["states"]):
    ok = False
    for states in nfa_dict["final"]:
        ok = ok or (i >> states)
    if ok:
        dfa["final"].append(i)

# Checking the status of the dfa dictionary can be done by printing the dfa

# dfa_prime will be used for storing the set of states to which a state (in DFA) will go on consuming a symbol
dfa_prime = {}

# we use a tuple for storing the state number and symbol because it is immutable and hence can be used as keys
# for the dictionary

# Initialisation of dfa_prime
for i in range(0, dfa["states"]):
    for symbols in dfa["letters"]:
        tup = (i, symbols)
        dfa_prime[tup] = set()

# Construction of dfa_prime
for blocks in nfa_dict["t_func"]:
    for i in range(0, dfa["states"]):
        ok = (i >> blocks[0]) & 1
        if ok:
            tup = (i, blocks[1])
            set_of_states = set(blocks[2])
            print(set_of_states)
            dfa_prime[tup] |= set_of_states

# The elements of sets are combined using the bit-masking to convert it into a integer value(new_state)
for key, val in dfa_prime.items():
    new_state = 0
    for element_of_set in val:
        new_state += pow(2, element_of_set)
    dfa_prime[key] = new_state

# t_func_list is used for storing the output generated in dfa_prime in the format-specified by input.json
t_func_list = []

for key, val in dfa_prime.items():
    new_list = list()
    new_list.append(key[0])
    new_list.append(key[1])
    new_list.append(val)
    t_func_list.append(new_list)

# finally the "t_func" key of the dfa dictionary is also complete
dfa["t_func"] = t_func_list

# we use dumps() which takes a python dictionary and converts it into a json file
result_string = json.dumps(dfa)

# printing the output to the output.json
with open('output.json', 'w') as output:
    json.dump(dfa, output)
print(result_string)

