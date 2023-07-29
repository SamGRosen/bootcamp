import json
import os


HEADERS = ["person", "age", "job", "favorite_color"]

# Create a variable to store data from all files
my_data = [
    # ("amy", 20, "waiter", "blue") example entry
]

path_to_folder = "./example_files/"

# Function to remove comments in line
def remove_comments(line):
    no_whitespace = line.strip()  #  => "## this is a comment"
    if "##" in no_whitespace:
        comment_starts_at_index = no_whitespace.index("##")
        filtered = no_whitespace[:comment_starts_at_index]
        return filtered.strip()  # In case there are spaces around the comment
    return no_whitespace


# Test it
print("test 1", remove_comments("  ## this is a comment  "))
print("test 2", remove_comments("person,age,job,favorite_color"))
print("test 3", remove_comments("person,age,job,favorite_color## comments   "))

# Split delimited file (either by commas or tabs) into data entries
def get_delimited_entries(file_as_str, delimiter):
    to_return = []
    lines = file_as_str.split("\n")
    for line in lines[1:]:  # Skip header
        if line:  # Skip blank lines from end of file if it exists
            to_return.append(line.split(delimiter))

    return to_return


# For every file my friend has
for file_path in os.listdir(path_to_folder):
    # Read it in as a string
    file = open(f"{path_to_folder}/{file_path}")
    file_as_lines = file.readlines()
    file.close()

    # Looks like
    # [
    #    "person,age,job,favorite_color\n",
    #    "amy,20,waiter,blue\n",
    #    "barry,30,engineer,grey\n",
    #    "## we have only adults in the dataset\n",
    #    "carl,25,None,purple ## None means unemployed\n",
    #    "## this person did not understand the survey dan,29,superhero,pineapple"
    # ]

    # Remove all comments in each line then remove all empty lines
    file_with_no_comments = ""
    for line in file_as_lines:
        comments_removed = remove_comments(line)
        if comments_removed:  # Not an empty line
            file_with_no_comments += comments_removed + "\n"

    # If it is a .csv or .tsv, seperate the commas or tabs and store it
    if file_path.endswith(".csv"):
        my_data.extend(get_delimited_entries(file_with_no_comments, ","))
    elif file_path.endswith(".tsv"):
        my_data.extend(get_delimited_entries(file_with_no_comments, "\t"))
    elif file_path.endswith(".json"):  # If it is a .json read the .json and store it
        as_dict = json.loads(file_with_no_comments)
        for entry in as_dict["data"]:
            #  Need to cast to str since json.loads will correctly load numbers as integers
            my_data.append([str(entry[header]) for header in HEADERS])
    else:
        print(f"Could not read file: {file_path}")

# Turn the variable that is storing all the data into a .csv

as_csv = ",".join(HEADERS) + "\n"
for entry in my_data:
    as_csv += ",".join(entry) + "\n"

with open("./output.csv", "w") as output_file:
    output_file.write(as_csv)
