def get_prep_words(filename):
    set_of_prep_words = set()
    
    f = open(filename, 'r')
    for line in f:
        line_strip = line.strip('\n')
        line_strip = line.strip()
        line_lowercase = line_strip.lower()
        
        set_of_prep_words.add(line_lowercase)

    f.close()

    return set_of_prep_words

def remove_empty_spaces(list):
    c = list.count('')

    for i in range (0,c):
        list.remove('')

def is_salt_pepper(string):
    s = 'salt'
    bp = 'black pepper'
    p = 'pepper'
    
    return s in string and (bp in string or p in string)
       
        
         
def remove_prep_words(recipe_list, set_prep_words):
    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer() # used to get rid of plurals
    
    for r in recipe_list:

        ingredient_list = recipe_list[r]
        add_at_end = False

        for i in range(0, len(ingredient_list)):
            ingred = ingredient_list[i]

            #Convert to lowercase
            lower_ingred = ingred.lower()

            #for special case salt and pepper only
            if is_salt_pepper(lower_ingred):
                add_at_end = True
                ingredient_list[i] =''
            else:
                #Remove prep words at beginning of ingredient string, second step
                lower_ingred_split =lower_ingred.split()

                new_ingred = ''

                for word in lower_ingred_split:
                    no_punc_word = word.strip(',')
                    no_punc_word = no_punc_word.strip(')')
                    no_punc_word = no_punc_word.strip('(')
                    
                    if no_punc_word not in set_prep_words and not no_punc_word.isdigit():
                        #Remove plurals
                        lemmatized_word = wnl.lemmatize(no_punc_word)
                        if lemmatized_word not in set_prep_words: #once again, for good measure, in case missed variation
                            new_ingred = new_ingred +  lemmatized_word + '_'

                ingredient_list[i] = new_ingred.strip('_- ')

        if add_at_end:
            ingredient_list.append('salt')
            ingredient_list.append('black_pepper')

        remove_empty_spaces(ingredient_list)

