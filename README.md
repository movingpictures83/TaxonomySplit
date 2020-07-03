# TaxonomySplit
# Language: Python
# Input: CSV
# Output: Prefix
# Tested with: PluMA 1.1, Python 3.6


PluMA plugin that takes a CSV file of taxa abundances (unnormalized)
and splits it into multiple CSV files, one at each level of the taxonomic tree.

These files will be named (prefix).kingdom.csv, (prefix).phylum.csv, etc.
down to the lowest classification level used in the input CSV file.
