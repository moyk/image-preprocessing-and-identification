# image-preprocessing-and-identification

The purpose of this project is to design and implement basic-level image processing and categorization. This program takes four
input from the user: query images, database images, k, output file name. For each image in the query, it finds k closest image 
in the database and writes the result to the output file. Our design consists of three general steps - image preprocessing 
and standardizing, categorization, and comparison, in order to return the closest k images. Each step contains multiple 
substeps conducted in sequence. To fine-tune the efficiency of run-time in our program, we focus on the preprocessing and 
categorization in order to reduce the number of comparisons needed within each category. 

