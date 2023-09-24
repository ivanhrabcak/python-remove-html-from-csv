import pandas as pd
from bs4 import BeautifulSoup
import re
import html

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&.{4};')
    cleantext = re.sub(cleanr, '', str(raw_html))
#     replacing the special characters
#     cleanr = re.compile ('\\n')
#     cleantext = re.sub(cleanr, ' ', cleantext)
    clean = re.sub('\s+',' ',cleantext)
    return html.unescape(clean) # replaces the special characters

def remove_html_escape(html):
    return BeautifulSoup(str(html), "lxml").text


file = input("Enter CSV File name (without '.csv' at the end): ")

# reading the file
try:
    d = pd.read_csv("%s.csv" % file )
except IOError:
    print ("Error: can\'t find file or read data")
else:
    print ("File read successfully")
    


a = pd.DataFrame(d)
print("File preview: \n",a.head(5))




def clean_column(col: str):
    try: 
        a[col][0:5]
    except:
        print("Error in fetching column. Please check the name '%s' from the table preview above" %col)
    else:
        print("Column read successfully: \n", a[col][0:5])


    a[col] = a[col].apply(cleanhtml)



    a[col] = a[col].apply(remove_html_escape)

for column in a.columns:
    clean_column(column)

# a.head(5)

# a['parity'] = a[col].str.len() - a['clean'].str.len() #using regex
# a['parity_bs'] = a[col].str.len() - a['clean_bs'].str.len() #using beautifulsoup


# a.tail(5)

print ("------------------------------------------------- \n HTML has been removed from your column contents \n------------------------------------------------- \n ")
print ("column 'clean' contins regex replacement of anything in between < > or &; or \\* \nin otherwords, it removes any html with the space character, no conversion of special characters to respective ASCII values.")
print ("column 'clean_bs' contains html removed with special characters replaced with their respective ASCII characters.")
print ("Parity columns show the difference in number of characters from the original html")

print ("Output table: \n %s" %a.head(5))



a.to_csv("%shtml_cleaned_output.csv"%file)
print("New file '%shtml_cleaned_output.csv' generated with cleaned columns. Check in the same direcotry"%file)

