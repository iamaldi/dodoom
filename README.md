# dodoom
A plain simple book recommendation system utilizing Jaccard similarity and Dice coefficient. dodoom uses the Book-Crossing dataset (http://www2.informatik.uni-freiburg.de/~cziegler/BX/). All data were downloaded in CSV format and then later imported into the `book.db` SQLite3 database.

# A snapshot of dodoom during execution

```console
user@user:~$ python dodoom.py
```

```
Generating profile for user_id: 250398
Calculating recommended books
Results overlap by 69.71% -- [0.6970673218]
Jaccard Similarity vs Golden Standard overlap by 81.80% -- [0.8180051063]
Dice Coefficient vs Golden Standard overlap by 69.71% -- [0.6970673218]  
Writing data to file...
Done!

Generating profile for user_id: 216670
Calculating recommended books
Results overlap by 73.70% -- [0.7369798156]
Jaccard Similarity vs Golden Standard overlap by 83.51% -- [0.8351157890]
Dice Coefficient vs Golden Standard overlap by 73.70% -- [0.7369798156]
Writing data to file...
Done!

Generating profile for user_id: 187830
Calculating recommended books
Results overlap by 59.32% -- [0.5931951108]
Jaccard Similarity vs Golden Standard overlap by 66.56% -- [0.6655744469]
Dice Coefficient vs Golden Standard overlap by 60.83% -- [0.6082847686]
Writing data to file...
Done!

Generating profile for user_id: 190459
Calculating recommended books
Results overlap by 61.39% -- [0.6138761709]
Jaccard Similarity vs Golden Standard overlap by 70.57% -- [0.7056556228]
Dice Coefficient vs Golden Standard overlap by 61.39% -- [0.6138761709]
Writing data to file...
Done!

Generating profile for user_id: 197410
Calculating recommended books
Results overlap by 77.40% -- [0.7739733814]
Jaccard Similarity vs Golden Standard overlap by 84.85% -- [0.8484804875]
Dice Coefficient vs Golden Standard overlap by 77.40% -- [0.7740279325]
Writing data to file...
Done!

```

## Requirements

This code is written in Python 3 and requires the following dependencies:
```
pip install nltk
```

This code was written as part of a university assignment.
