This is a replication pack for the purpose of replication the experimental work. It includes the following files:
## 30_issues_data.csv
Contains a list of the thirty issues including the issue keys, titles, descriptions, details expert estimates, and logged times. The details field is a compound field. It consists of issue comments, project overview, and issue dictionary. It first starts with developer comments ([comments]), issue project([project_info]), and then issue dictionary ([terms_def]). Each line under [comments] and [terms_def] represent a record that contains two attributes of information and author and comment for the lines under [comments], and term and definition for lines under [terms_def]. The separator between to two attributes is “\$*$”

## crowd_estimates.csv
Contains a list of crowd estimates that includes issue key, round number, round kappa, crowd estimate, crowd justification, auto quality class.

## issues_and_estimates_data.xlsx
Is an MS Excel file that contains above files (30_issues_data.csv, crowd_estimates.csv) as sheets.

## cpp_replication_python_functions.py
Is a python file that contains two functions that are used to compute round Kappa, and aggregate crowd estimates.

## direct_url_to_all_issues.csv
This file contains direct URLs to the selected and used issues in our experiments. May be needed for additional verification purposes.

# JOSSE Dataset
The above 30 issues were selected from JOSSE dataset whcih can be accessed from the following repositry:
https://github.com/ml-see/josse
