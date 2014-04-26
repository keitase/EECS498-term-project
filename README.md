This is running once every 10 minutes at https://dashboard.heroku.com/apps/safe-journey-1452/resources

Right now it just stores the titles of the questions, and the id to prevent double-stores / to get more info later. We will probably need more than that eventually.


The data used within our implementations can be found in the data folder. They are labled according to the type of data they contain.

Naive Bayes Keyword Implementation:
===================================

To run: python evaluate.py

To change the threshold: alter threshold varaible at the top of the program
To change dataset: import different dataset and make sure the dataset is contained in the folder.

Machine Learning Implementation:
================================

To run: `python classify.py`

    python classify.py --help lists the command line options

The cutoff and dataset can be varied. You can print stuff in a gnuplot-friendly format, too. You can also cheat. Don't do that.
