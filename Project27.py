import re
import subprocess

# Andres Landeta(alandeta) 631427

# 2.7 version of the program

""" Finds the best matches for reviews in the folder revs. 
    It uses the UNIX commands grep and agrep to select possible matches
    Then it determines the best matches based on the lenght of the matches
    Finally it writes the output in a file results.txt """
def main():
    
    film_titles = open("film_titles.txt", "r")

    
    matches = {}

    # Check how many titles is the by counting the lines of the file with wc unix command
    number_of_titles = (int)(subprocess.check_output("wc -l film_titles.txt",
                                 shell=True).replace("film_titles.txt\n", ""))

    # To print the porcentage
    i = 0
    n = 0


    print "Wait for results, this may take a while..."

    for title in film_titles:
        # Delete all double quotes in the titles
        title = title.replace('"', "")
        # Delete end of the line and nonsense blank spaces
        title = title.strip()  
        # Escape all regular expressions simbols
        regex_title = re.escape(title)        
        
        try:
            # Add all exact matches 
            matches = exact_match_search(title, regex_title, matches)
            # Add all aproximate matches
            matches = approx_match_search(title, regex_title, matches)

        # grep return an error if there are not matches instead of a empty string        
        except subprocess.CalledProcessError as e:  
            pass

        # Print the porcentage every 1%    
        i += 1
        if(i*100.0/number_of_titles > n):           
            print str(n) + "%" 
            n += 1                
    print "100%"
    film_titles.close()
    print "Analysing the reviews..."
    for file_name in matches.keys():
        # Sort by lenght
        matches[file_name] = sorted(matches[file_name], key=len, reverse = True)
        matches[file_name] = matches[file_name][0]

    matches = film_goodness(matches)    

    newfile = write_in_file(matches)    
    print "100%"
    

    print "Ready! Check " + newfile + " on source folder"   

    




                   
""" Return the recommended number of edit for an approximate matches """                
def get_edit_num(title_length):
        # For all string shorter than 3 characters
        edit_num = 0                     
        
        if(title_length >= 3 and title_length < 5):
            edit_num = 1
        elif(title_length >= 5 and title_length < 20): 
            edit_num = 2
        elif(title_length >= 20 and title_length < 40): 
            edit_num = 3
        elif(title_length >= 40):
            edit_num = 4

        return edit_num    


""" Use UNIX command grep to search for exact matches of titles, put all matches in a 
    dictionary mapping file names with a list of possible best matches """

def exact_match_search(title, regex_title, dictionary):

    # Build the command
    command = 'grep -l -w -i "'+regex_title+'" revs/*'  

    # Put all lines of the output in a list of results
    results = subprocess.check_output(command, shell=True).splitlines()

    # Map the titles with the file name of the exact title matches
    for file_name in results:
        file_name = file_name.replace("revs/", "")
        if dictionary.has_key(file_name):
            dictionary[file_name] = dictionary[file_name] + [title]                    
        else:
            dictionary[file_name] = [title]  

    return dictionary

""" Use UNIX command agrep to search for approximate matches of titles, put all matches in a 
    dictionary mapping file names with a list of possible best matches """

def approx_match_search(title, regex_title, dictionary):
    # Get the recommended number of edits for the title size
    edit_num = get_edit_num(len(title))  

    # Look for matches for tittles larger than 2 characters          
    if(edit_num != 0):

        command = 'agrep -l -'+str(edit_num)+' "'+ regex_title + '" revs/*'

        # Put all lines of the output in a list of results
        results = subprocess.check_output(command, shell=True).splitlines()

        # Map the titles with the file name of the approximate title matches
        for file_name in results:

            file_name = file_name.replace("revs/", "")
            if dictionary.has_key(file_name):
                dictionary[file_name] = dictionary[file_name] + [title]                    
            else:
                dictionary[file_name] = [title] 

    return dictionary    

""" Writes the output of the program in a file on the source"""
def write_in_file(dictionary):

    newfile = "results.txt"
    results = open(newfile, "w+")
    for file_name in dictionary.keys():
        # Sort by lenght
        results.write(file_name + " -> " + dictionary[file_name][0] + ' | ' + dictionary[file_name][1] + '\n')  
    results.close()    

    return newfile    

def film_goodness(matches_dict):
    adjectives = open("adjectives.txt", "r")
    adj_dictionary = {}
    isodd = True
    lines = adjectives.readlines()
    standard_factor = 5.0

    i = 0
    n = 0    
    
    for line in lines:
        
        if (isodd):
            adjective = line.strip()
            weight = (int)(lines[lines.index(line) + 1].strip())
            adj_dictionary[adjective] = weight        
            isodd = False
        else:
            isodd = True  
    
    number_of_adjectives = len(adj_dictionary.keys())

    for match in matches_dict.keys():
        matches_dict[match] = [matches_dict[match], '0']        
        
    for adjective in adj_dictionary.keys():
        reg_adjective = re.escape(adjective)
        command = 'agrep -c -1 "'+reg_adjective+'" revs/*'
        try:            
            results = subprocess.check_output(command, shell=True)
            results = results.splitlines()
            for result in results:
                result = result.replace("revs/", "")
                result = result.replace(":", "")
                result = result.strip()
                new = result.split()
                if new[0] in matches_dict.keys():
                    matches_dict[new[0]][1] =  str((int)(matches_dict[new[0]][1]) + 
                                              (int)(new[1]) * adj_dictionary[adjective])


                            
        # grep return an error if there are not matches instead of a empty string
        except subprocess.CalledProcessError as e:  
            pass
            
        
        # Print the porcentage every 5%    
        i += 1
        if(i*100.0/number_of_adjectives > n):           
            print str(n) + "%" 
            n += 5

    for match in matches_dict.keys():
        goodness = int(matches_dict[match][1])
        if(goodness < -30):
            matches_dict[match][1] = "atrocious"
        elif(goodness > -30 and goodness < -15):
            matches_dict[match][1] = "terrible"       
        elif(goodness >= -15 and goodness < -5):
            matches_dict[match][1] = "poor"
        elif(goodness >= -5 and goodness < 0):
            matches_dict[match][1] = "bad"
        elif(goodness > 0 and goodness <= 5):
            matches_dict[match][1] = "good"
        elif(goodness > 5 and goodness <= 15):
            matches_dict[match][1] = "great"
        elif(goodness > 15 and goodness <= 30):
            matches_dict[match][1] = "amazing"  
        elif(goodness > 30):
            matches_dict[match][1] = "masterful"             
        else:
            matches_dict[match][1] = "neutral or undecidable" 

    adjectives.close()
    return matches_dict

main()