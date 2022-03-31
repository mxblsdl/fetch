import json

""" 
A set of functions for reading in the data json files. 
It should be noted that the json files are actually json-ld where each line is a separate json object.
The format of each function is the same, taking the file location argument and returning a list of dictionaries.
Certain fields in each file are simplified to better fit the dictionary output format.
"""


def load_brands(path: str) -> list:
    lines = []

    for line in open(path, "r"):
        lines.append(json.loads(line))

    # simplify nested list structure
    for l in range(len(lines)):
        lines[l]["_id"] = lines[l]["_id"]["$oid"]
        lines[l]["cpg"] = lines[l]["cpg"]["$id"]["$oid"]
    return lines


def load_receipts(path):
    """
    This function drops the rewardsReceiptItemList field which itself is a nested list of jsons.
    I decided to extract this into a separate table to show each item bought by a user.
    """
    lines = []
    for line in open(path, "r"):
        lines.append(json.loads(line))

    # simplify nested list structure
    # The .get method needs to be used here since not every item contains all the fields
    for l in range(len(lines)):
        lines[l]["_id"] = lines[l].get("_id").get("$oid")
        lines[l]["createDate"] = lines[l].get("createDate").get("$date")
        lines[l]["dateScanned"] = lines[l].get("dateScanned").get("$date")
        lines[l]["finishedDate"] = lines[l].get("finishedDate", {}).get("$date")
        lines[l]["modifyDate"] = lines[l].get("modifyDate", {}).get("$date")
        lines[l]["pointsAwardedDate"] = (
            lines[l].get("pointsAwardedDate", {}).get("$date")
        )
        lines[l]["purchaseDate"] = lines[l].get("purchaseDate", {}).get("$date")

    return lines


def load_users(path):
    lines = []
    for line in open(path, "r"):
        lines.append(json.loads(line))

    for l in range(len(lines)):
        lines[l]["_id"] = lines[l].get("_id").get("$oid")
        lines[l]["createdDate"] = lines[l].get("createdDate", {}).get("$date")
        lines[l]["lastLogin"] = lines[l].get("lastLogin", {}).get("$date")

    return lines


def load_items(path):
    """
    Function is a little more complicated than the others since there is a nested json object.
    There is probably a more elegent solution to this and could be refactored at a later date.
    """

    # Reload receipts file
    lines = []
    for line in open(path, "r"):
        lines.append(json.loads(line))

    # extract only the Id and item list
    for l in range(len(lines)):
        lines[l]["_id"] = lines[l].get("_id").get("$oid")
        lines[l]["rewardsReceiptItemList"] = lines[l].get("rewardsReceiptItemList", {})

    # create new list that will contain only the rewards receipts items
    new_items = []
    for l in range(len(lines)):
        res = dict(
            (k, lines[l][k]) for k in ["rewardsReceiptItemList"] if k in lines[l]
        )
        res = res.get("rewardsReceiptItemList", {})

        # append the ID to each rewards item
        for r in res:
            r["id"] = lines[l]["_id"]

            new_items.append(r)

    return new_items
