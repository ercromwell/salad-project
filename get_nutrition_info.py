from collections import defaultdict
import os
import csv
import pickle
import prep_removal_defs as pr
import recipe_info_defs as rid

#stored_recipes = 'salad_data'
files = os.listdir("salad_data")
print len(files)

recipe_list = defaultdict(list)
feature_list = defaultdict(list)
counter = 0
