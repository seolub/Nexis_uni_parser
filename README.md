# Nexis_uni_parser
Parser for Nexis Uni documents

## Description
This repository provides functions to parse DOCX files retrieved from Nexis Uni. It parses the following information:
- Date
- Author
- Title
- Body Text
- Newspaper

Additionaly, it returns the sentiment probabilities (neutral, positive, negative) from the article body text.

### How it works

News article from Nexis Uni are downloaded in a format (DOCX, RTF, or PDF) that is not ideal for quantitative analyses. Files can contain up to 100 news articles like the following one:

#### Example of article
![example_nexis](https://user-images.githubusercontent.com/89941958/180215674-1fb58d44-fad9-42fb-b2b9-4dba76966756.jpg)

Two DOCX examples can be find in the */data* folder:
- */data/example1.csv*
- */data/example2.csv*

The function *etl_all_docs* in *nexis_uni.py* takes a folder path, reads all .DOCX files and parses all the relevant information described in the description. The data is returned in a csv file. 

Example:
We want to read all DOCX files in the folder *~/data* and  store the resulting csv as *parsed_articles.csv* in the same folder. We can execute the following code:
```
path_input = "~/data"
file_path_output = "~/data/parsed_articles.csv"

etl_all_docs(path_input, file_path_output)
```

### Potential Issues 
- Please note that there might be some issues with dates formatting and additional work might be needed. Different media outlets provide different date formats.
- Sentiment classification is only available in Spanish at the moment but the code can be changed easily to other languages.



