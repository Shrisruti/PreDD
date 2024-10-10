from __future__ import division
import os
import math
import argparse
import sys
import itertools
#import zen
import numpy as np
import networkx as nx
from itertools import chain, combinations

import pandas as pd
from collections import Counter

# method 4 -- maximum coverage
def sruti_max_cover(universe, subsets):
    covered_key = set()
    covered_set = set()
    temp_set = set()
    current_set_len = 0
    print("Required len to cover the universe", round(coverage))

    for i in range(max_key_len):
        current_key_set = [
            key for key, val in subsets.items() if len(val) == max_key_len - i]
        print("first_for_loop")
        for j in range(len(current_key_set)):
            print("second_for_loop")
            current_set_len = len(covered_set)
            temp_set.update(subsets.get(current_key_set[j]))
            # covered_set.update(subsets.get(current_key_set[j]))
            print("updated temp_set")

            if len(temp_set) <= round(coverage):
                print("first_if for coverage")
                print("elements_covered_so_far for the present keys",
                      subsets.get(current_key_set[j]))
                print("len of covered_set", len(temp_set))

                if len(temp_set) > current_set_len:
                    print("second_if for updating key")
                    covered_key.add((current_key_set[j]))
                    print("updated key")
                    print("key", current_key_set[j])
                    covered_set.update(subsets.get(current_key_set[j]))

            else:
                print("else statement")
                print("updating the first key")
                covered_key.add(current_key_set[j])
                print("key", current_key_set[j])
                covered_set.update(subsets.get(current_key_set[j]))
                return covered_set, covered_key
        # break
    print("breaking")
    print("covered_set", len(covered_set), covered_set)
    print("covered_key", len(covered_key), covered_key)
    return covered_set, covered_key


# main function -- read in the inputs
if __name__ == "__main__":
    # read in the toppath mut, toppath deg and toppath weighted interaction files
    parser = argparse.ArgumentParser(
        description='This code outputs maximum set coverage for the given coverage cutoff', epilog='sruti')
    parser.add_argument('edgewtfile', type=str,
                        help='List of edges and weigths of the toppath')
    parser.add_argument('mutfile', type=str,
                        help='Mutated node list from the toppath')
    parser.add_argument('degfile', type=str,
                        help='DEG node list from the toppath')
    parser.add_argument('coverage_cutoff', type=int,
                        help='desired coverage cut-off. Eg: for 70% coverage, enter the value 70')
    args = parser.parse_args()

    toppath = open(args.edgewtfile, 'r')
    mut_file = open(args.mutfile, 'r')
    deg_file = open(args.degfile, 'r')
    coverage_cutoff = sys.argv[4]

    pat_name = sys.argv[1]
    pat_name1 = pat_name.split("_", 4)
    pat_name2 = pat_name1[0]
    print("Current patient: "), pat_name2
    print("Reading input arguments")
    print("The input coverage cutoff is: "), coverage_cutoff
    mutnodes = mut_file.read().splitlines()
    degnodes = deg_file.read().splitlines()
    G = nx.read_weighted_edgelist(
        toppath, nodetype=str, create_using=nx.DiGraph())

    # declare the subset dictionary
    mut_subsets = {}
    # fill in the dict keys w/o values
    for i in mutnodes:
        mut_subsets[i] = None

    # find the successor nodes of mutnodes, filter to keep only the degnodes
    # and update the dict
    for mut in mutnodes:
        #print "mut", mut
        mut_down = list(nx.dfs_postorder_nodes(G, source=mut, depth_limit=4))
        # retain only the degnodes
        mut_deg = [a for a in mut_down if a in degnodes]
        mut_subsets[mut] = mut_deg
    print("Created the mut_subsets dictionary")

    # the mut_subsets has a list of all captured degnodes --- use as Universe set
    # first flatten the list of lists and convert it to a set object
    universe = set([item for sublist in mut_subsets.values()
                   for item in sublist])
    coverage = (int(coverage_cutoff)/100)*len(universe)
    max_key_len = max([len(mut_subsets[ele]) for ele in mut_subsets])

    max_cover_out = sruti_max_cover(universe, mut_subsets)
    print("Calculated max_set for the desired coverage cutoff")
    print("\n")
    foutput1 = pat_name2+"_maxset.txt_"+coverage_cutoff
    with open(foutput1, 'w') as w1:
        w1.write(str(max_cover_out[0]))  # covered_set
        w1.write("\n")
        w1.write(str(max_cover_out[1]))  # covered_keys
        w1.write("\n")
        w1.close()
