import sqlite3
from helpers import load_brands, load_items, load_receipts, load_users


con = sqlite3.connect("fetch.db")
cursor = con.cursor()

# Create Brands table
cursor.execute(
    """
drop table if exists Brands
"""
)

cursor.execute(
    """create table if not exists Brands (
id Text PRIMARY KEY, 
brandCode Text,
barcode Integer, 
category Text,
categoryCode Text,
cpg Text,
name Text,
topBrand Text
)"""
)

lines = load_brands("./data/brands.json")
for i in range(len(lines)):
    cursor.execute(
        "insert into Brands values (?, ?, ?, ?, ?, ?, ?, ?);",
        [
            lines[i].get("_id"),
            lines[i].get("brandCode"),
            lines[i].get("barcode"),
            lines[i].get("category"),
            lines[i].get("categoryCode"),
            lines[i].get("cpg"),
            lines[i].get("name"),
            lines[i].get("topBrand"),
        ],
    )

# Create Users Table
cursor.execute(
    """
drop table if exists Users
"""
)

cursor.execute(
    """
create table if not exists Users (
id Text PRIMARY KEY,
state Text,
createdDate Text,
lastLogin Text,
role Text,
signUpSource Text,
active Text
)
"""
)

lines = load_users("./data/users.json")

# The users data has many duplicates which violate the primary key uniqueness
res_lines = set(frozenset(d.items()) for d in lines)
res_lines = [dict(s) for s in res_lines]

for i in range(len(res_lines)):
    cursor.execute(
        "insert into Users values (?, ?, ?, ?, ?, ?, ?);",
        [
            res_lines[i].get("_id"),
            res_lines[i].get("state"),
            res_lines[i].get("createdDate"),
            res_lines[i].get("lastLogin"),
            res_lines[i].get("role"),
            res_lines[i].get("signUpSource"),
            res_lines[i].get("active"),
        ],
    )


# Create Receipts Table
cursor.execute(
    """
drop table if exists Receipts
"""
)

cursor.execute(
    """
create table if not exists Receipts (
id Text PRIMARY KEY,
bonusPointsEarned Text,
bonusPointsEarnedReason Text,
createDate Text,
dateScanned Text,
finishedDate Text,
modifyDate Text,
pointsAwardedDate Text,
pointsEarned Text,
purchaseDate Text,
purchasedItemCount Text,
rewardsReceiptItemList Text,
rewardsReceiptStatus Text,
totalSpent Text,
userId Text,
FOREIGN KEY (userId) REFERENCES Users(id)
)
"""
)

lines = load_receipts("./data/receipts.json")
for i in range(len(lines)):
    cursor.execute(
        "insert into Receipts values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        [
            lines[i].get("_id"),
            lines[i].get("bonusPointsEarned"),
            lines[i].get("bonusPointsEarnedReason"),
            lines[i].get("createDate"),
            lines[i].get("dateScanned"),
            lines[i].get("finishedDate"),
            lines[i].get("modifyDate"),
            lines[i].get("pointsAwardedDate"),
            lines[i].get("pointsEarned"),
            lines[i].get("purchaseDate"),
            lines[i].get("purchasedItemCount"),
            lines[i].get("rewardsReceiptItemList"),
            lines[i].get("rewardsReceiptStatus"),
            lines[i].get("totalSpent"),
            lines[i].get("userId"),
        ],
    )


# Create an items table
cursor.execute(
    """
drop table if exists Items
"""
)

cursor.execute(
    """
create table if not exists Items (
barcode Text,
brandCode Text,
description Text,
finalPrice Text,
itemPrice Text,
needsFetchReview Text,
needsFetchReviewReason Text,
partnerItemId Text,
preventTargetGapPoints Text,
pointsNotAwardedReason Text,
pointsEarned Text,
pointsPayerId Text,
quantityPurchased Text,
rewardsGroup Text,
rewardsProductPartnerId Text,
targetPrice Text,
userFlaggedNewItem Text,
userFlaggedBarcode Text,
userFlaggedDescription Text,
userFlaggedPrice Text,
userFlaggedQuantity Text,
id Text,
FOREIGN KEY (brandCode) REFERENCES Brands(brandCode),
FOREIGN KEY (id) REFERENCES Receipts(id)
)
"""
)

lines = load_items("./data/receipts.json")
for i in range(len(lines)):
    cursor.execute(
        "insert into Items values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        [
            lines[i].get("barcode"),
            lines[i].get("brandCode"),
            lines[i].get("description"),
            lines[i].get("finalPrice"),
            lines[i].get("itemPrice"),
            lines[i].get("needsFetchReview"),
            lines[i].get("needsFetchReviewReason"),
            lines[i].get("partnerItemId"),
            lines[i].get("preventTargetGapPoints"),
            lines[i].get("pointsNotAwardedReason"),
            lines[i].get("pointsEarned"),
            lines[i].get("pointsPayerId"),
            lines[i].get("quantityPurchased"),
            lines[i].get("rewardsGroup"),
            lines[i].get("rewardsProductPartnerId"),
            lines[i].get("targetPrice"),
            lines[i].get("userFlaggedDescription"),
            lines[i].get("userFlaggedBarcode"),
            lines[i].get("userFlaggedNewItem"),
            lines[i].get("userFlaggedPrice"),
            lines[i].get("userFlaggedQuantity"),
            lines[i].get("id"),
        ],
    )


con.commit()
