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
     
    newfile = write_in_file(matches)    

    print "Ready! Check " + newfile + " on source folder"   

    film_titles.close()




                   
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
    command = 'grep -l -w "'+regex_title+'" revs/*'  

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
        dictionary[file_name] = sorted(dictionary[file_name], key=len, reverse = True)
        results.write(file_name + " -> " + dictionary[file_name][0] + '\n')  
    return newfile    


main()