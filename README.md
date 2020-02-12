# dodoom
A plain simple book recommendation system utilizing Jaccard similarity and Dice coefficient. dodoom uses the Book-Crossing dataset (http://www2.informatik.uni-freiburg.de/~cziegler/BX/). All data were downloaded in CSV format and then later imported into the `book.db` SQLite3 database.

# A snapshot of dodoom during execution

```console
user@user:~$ python dodoom.py
```

```
Generating profile for user_id: 178035
Calculating recommended books
Results overlap by 72.28% -- [0.7227689111]
Jaccard Similarity vs Golden Standard overlap by 82.95% -- [0.8294696592]
Dice Coefficient vs Golden Standard overlap by 72.28% -- [0.7227689111]
Writing data to file...
Done!

Generating profile for user_id: 210717
Calculating recommended books
Results overlap by 73.39% -- [0.7339227685]
Jaccard Similarity vs Golden Standard overlap by 83.37% -- [0.8336617643]
Dice Coefficient vs Golden Standard overlap by 73.39% -- [0.7339227685]
Writing data to file...
Done!

Generating profile for user_id: 223253
Calculating recommended books
Results overlap by 68.03% -- [0.6802875367]
Jaccard Similarity vs Golden Standard overlap by 81.16% -- [0.8115665324]
Dice Coefficient vs Golden Standard overlap by 68.03% -- [0.6802875367]
Writing data to file...
Done!

Generating profile for user_id: 187863
Calculating recommended books
Results overlap by 62.58% -- [0.6258163183]
Jaccard Similarity vs Golden Standard overlap by 71.13% -- [0.7113309781]
Dice Coefficient vs Golden Standard overlap by 62.58% -- [0.6258163183]
Writing data to file...
Done!

Generating profile for user_id: 182403
Calculating recommended books
Results overlap by 69.17% -- [0.6917236400]
Jaccard Similarity vs Golden Standard overlap by 85.55% -- [0.8555394846]
Dice Coefficient vs Golden Standard overlap by 73.17% -- [0.7316737647]
Writing data to file...
Done!
```
This code was written as part of a university assignment.
