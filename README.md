# dodoom
A plain simple book recommendation system utilizing Jaccard similarity and Dice coefficient. dodoom uses the Book-Crossing dataset (http://www2.informatik.uni-freiburg.de/~cziegler/BX/). All data were downloaded in CSV format and then later imported into the `book.db` SQLite3 database.

# A snapshot of dodoom during execution

```console
user@user:~$ python dodoom.py
```

```
Generating profile for user_id: 257198
Calculating recommended books
Results overlap by 75.18% -- [0.7517741403]
Jaccard Similarity vs Golden Standard overlap by 83.89% -- [0.8389391745]
Dice Coefficient vs Golden Standard overlap by 75.18% -- [0.7517741403]
Writing data to file...
Done!

Generating profile for user_id: 183952
Calculating recommended books
Results overlap by 69.16% -- [0.6915675737]
Jaccard Similarity vs Golden Standard overlap by 81.43% -- [0.8143051055]
Dice Coefficient vs Golden Standard overlap by 69.16% -- [0.6915675737]
Writing data to file...
Done!

Generating profile for user_id: 241980
Calculating recommended books
Results overlap by 73.11% -- [0.7310737515]
Jaccard Similarity vs Golden Standard overlap by 83.18% -- [0.8317534776]
Dice Coefficient vs Golden Standard overlap by 73.11% -- [0.7310737515]
Writing data to file...
Done!

Generating profile for user_id: 251140
Calculating recommended books
Results overlap by 67.07% -- [0.6706715361]
Jaccard Similarity vs Golden Standard overlap by 80.49% -- [0.8048551255]
Dice Coefficient vs Golden Standard overlap by 67.07% -- [0.6706715361]
Writing data to file...
Done!

Generating profile for user_id: 224146
Calculating recommended books
Results overlap by 66.64% -- [0.6664370027]
Jaccard Similarity vs Golden Standard overlap by 80.51% -- [0.8050906068]
Dice Coefficient vs Golden Standard overlap by 66.64% -- [0.6664370027]
Writing data to file...
Done!

```
This code was written as part of a university assignment.
