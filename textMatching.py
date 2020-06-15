import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd
from tqdm import tqdm
from difflib import get_close_matches, SequenceMatcher
from fuzzywuzzy import process

from config import moodl, payment_system


def dbConnect(db):
    dbConnector = mysql.connector.connect(
        host=db["host"],
        user=db["user"],
        passwd=db["passwd"],
        database=db["database"]
    )
    return dbConnector


def sqlData(table, db):
    db_conn = dbConnect(db)
    cursor = db_conn.cursor()
    print("SELECT * FROM `%s` WHERE 1" % (table))
    cursor.execute("SELECT * FROM `%s` WHERE 1" % (table))
    rows = cursor.fetchall()
    db_conn.cursor().close()
    return rows


def removeDuplicates(table, idx):
    table = np.array(table)
    allIndices = list(table[:, idx])
    uniqueIndices = list(set(table[:, idx]))
    tableCleaned = []
    for user in uniqueIndices:
        tableCleaned.append(table[allIndices.index(user)])
    return tableCleaned


def saveToCsv(data, tableName):
    data = np.array(data)
    np.savetxt(tableName, data, delimiter=",")


# difflib
# def findClosest(data, reference):
#     data = np.array(data)
#     finalData = []
#     print("Finding Closest Matches")
#     for idx in tqdm(range(len(data))):
#         currRow = ["", "", "", "", "", "", "", "", ""]
#         # print("First Name: ", data[idx][0])
#         # print("Email Id: ", data[idx][1])
#         currRow[0] = data[idx][0]
#         currRow[1] = data[idx][1]
#         matches = get_close_matches(data[idx][1], reference)
#         idx = 2
#         for match in matches:
#             s = SequenceMatcher(None, data[idx][1], match)
#             currRow[idx] = match
#             idx += 1
#             currRow[idx] = s.ratio()
#             idx += 1
#             # print(match, ":", s.ratio(), ",")
#         if(len(matches)):
#             currRow[8] = matches[0]
#         finalData.append(currRow)
#         # print("#####################################")
#     return finalData


def findClosest(data, reference):
    data = np.array(data)
    finalData = []
    print("Finding Closest Matches")

    # splitting about "@" to remove domain from text matching. So focusing text matching just on username
    userName = [user.split("@")[0] for user in reference]

    for idx in tqdm(range(len(data))):
        currRow = ["", "", "", "", "", "", "", "", ""]
        # print("First Name: ", data[idx][0])
        # print("Email Id: ", data[idx][1])
        currRow[0] = data[idx][0]
        currRow[1] = data[idx][1]

        # Checking matches of username with Actual Name
        matches = process.extractBests(
            data[idx][0].split("@")[0], userName, limit=3)

        # if match score is less than 90 than we will proceed with username match against username
        if(matches[0][1] < 90):
            matches = process.extractBests(
                data[idx][1].split("@")[0], userName, limit=3)

        idx = 2
        for match in matches:
            currRow[idx] = reference[userName.index(match[0])]
            idx += 1
            currRow[idx] = match[1]
            idx += 1
        if(len(matches)):
            currRow[8] = reference[userName.index(matches[0][0])]
        finalData.append(currRow)
        # print("#####################################")
    return finalData


if __name__ == "__main__":
    moodlUserData = np.array(sqlData("mdl_user", moodl))

    # Removing users with invalid emails
    moodlUserData = [user for user in moodlUserData if ".com" in user[12]]

    # Removing duplicates and storing emails from moodl
    moodleEmails = list(set(np.array(moodlUserData)[:, 12]))

    # Payment Data
    paymentUserData = np.array(sqlData("user_details", payment_system))

    # Removing users with invalid emails
    paymentUserData = [user for user in paymentUserData if ".com" in user[2]]

    # Removing duplicates from table
    paymentUserData = removeDuplicates(paymentUserData, 2)

    matchedUsers = []
    unmatchedUsers = []
    print("Finding Perfect Matches")
    for idx in tqdm(range(len(paymentUserData))):
        if(paymentUserData[idx][2] in moodleEmails):
            # print("First Name: ", user[5])
            # print("Email Id: ", user[2])
            # print("#####################################")
            # Storing names and emails for matched user
            matchedUsers.append(
                [paymentUserData[idx][5], paymentUserData[idx][2]])
        else:
            # Storing names and emails for unmatched user
            unmatchedUsers.append(
                [paymentUserData[idx][5], paymentUserData[idx][2]])

    unmatchedUsers = findClosest(unmatchedUsers, moodleEmails)
    pd.DataFrame(matchedUsers, columns=["Name", "Email"]).to_csv(
        "MatchedUsers.csv", index=False)
    pd.DataFrame(unmatchedUsers, columns=["Name", "Email", "Match_1", "Score_1", "Match_2",
                                          "Score_2", "Match_3", "Score_3", "Best Match"]).to_csv("UnMatchedUsers.csv", index=False)
