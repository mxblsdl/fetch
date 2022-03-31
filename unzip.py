import os

"""
Unzip the downloaded content. Run once to prepare the json files.
"""

os.system("gzip -d receipts.json.gz")
os.system("gzip -d users.json.gz")
os.system("gzip -d brands.json.gz")
