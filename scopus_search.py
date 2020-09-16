import pandas as pd
import PySimpleGUI as sg
import math
import time
from tqdm import tqdm

def main(df):

    if {'ReadTimeStamp', 'Accepted', }.issubset(df.columns) == False:
        df['ReadTimeStamp'] = None
        df['Accepted'] = None
    
    abstract = False
    
    sg.change_look_and_feel('DarkAmber')    # Add a touch of color

    # All the stuff inside your window.
    txtTitle = sg.Text("", key="-TITLETEXT-", size=(75, 4),
                       justification="center", font='Bold 14', text_color="light grey")
    txtAbstract = sg.Text("", key="-ABSTRACTTEXT-", size=(75, 20),
                justification="center", font='Bold 14', text_color="grey")
    txtAuthors = sg.Text("", key="-AUTHORSTEXT-", size=(70, 1),
                justification="left", font='Bold 14', text_color="grey")
    txtYear = sg.Text("", key="-YEARTEXT-", size=(5, 1),
                justification="right", font='Bold 14', text_color="grey")
    btnPrevious = sg.Button('<', key="-PREVIOUS-")
    btnNext = sg.Button('>', key="-NEXT-")
    txtCurrentIndex = sg.Text("", key="-CURRENTINDEX-",
                              size=(5, 1), justification="right")
    txtTotalPapers = sg.Text(" / " + str(df.shape[0] - 1), key="-TOTALPAPERS")
    btnAccept = sg.Button('Accept', key="-ACCEPT-")
    btnReject = sg.Button('Reject', key="-REJECT-")
    txtStatus = sg.Text("Status: Unknown", key="-STATUSTEXT-", size=(15, 1),
                        text_color="grey", visible=True, justification="center")
    acceptedCount = sg.Text("", key="-ACCEPTEDCOUNTTEXT-", size=(4, 1), pad=(0, 0),
                            text_color="green", visible=True, justification="right")
    rejectedCount = sg.Text("", key="-REJECTEDCOUNTTEXT-", size=(4, 1), pad=(0, 0),
                            text_color="red", visible=True, justification="left")

    
    separatorLenght = 76 #95

    layout = [
                [txtTitle], 
                [txtAuthors, txtYear],
                [sg.Text('_'*separatorLenght, font='14', text_color="light grey")],
                [btnPrevious, txtCurrentIndex, txtTotalPapers, btnNext, btnAccept, btnReject, sg.Text("", size=(20, 0)), txtStatus, sg.Text("", size=(20, 0)), acceptedCount, rejectedCount]
            ]

    
    layoutWithAbstract = [
                [txtTitle], 
                [sg.Text('_'*separatorLenght, font='14', text_color="light grey")],
                [txtAbstract],
                [sg.Text('_'*separatorLenght, font='14', text_color="light grey")],
                [txtAuthors, txtYear],
                [sg.Text('_'*separatorLenght, font='14', text_color="light grey")],
                [btnPrevious, txtCurrentIndex, txtTotalPapers, btnNext, btnAccept, btnReject, sg.Text("", size=(20, 0)), txtStatus, sg.Text("", size=(20, 0)), acceptedCount, rejectedCount]
            ]

    # Create the Window
    if("Abstract" in df.columns):
        window = sg.Window('Read The Titles!', layoutWithAbstract, resizable=False)
        abstract = True
    else:
        window = sg.Window('Read The Titles!', layout, resizable=False)

    window.finalize()

    i = df["ReadTimeStamp"][::-1].idxmax()
    if(math.isnan(i)):
        i = -1

    if(i < (df.shape[0] - 1)):
        i = i + 1
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        row = df.iloc[i]
        window['-TITLETEXT-'].update(row['Title'])
        if(abstract):
            window['-ABSTRACTTEXT-'].update(row['Abstract'])
        window['-AUTHORSTEXT-'].update(row['Authors'])
        window['-YEARTEXT-'].update(row['Year'])

        window['-CURRENTINDEX-'].update(str(i))
        window['-ACCEPTEDCOUNTTEXT-'].update(
            str(len(pd.unique(df["Title"][(df["Accepted"] == True)]))))
        window['-REJECTEDCOUNTTEXT-'].update(
            str(len(pd.unique(df["Title"][(df["Accepted"] == False)]))))
        if(row["Accepted"] == True):
            window['-STATUSTEXT-'].update('Status: Accepted',
                                          text_color="green")
        elif(row["Accepted"] == False):
            window['-STATUSTEXT-'].update('Status: Rejected', text_color="red")
        else:
            window['-STATUSTEXT-'].update('Status: Unknown', text_color="grey")

        event, values = window.read()
        if event in (None, 'Cancel'):   # if user closes window or clicks cancel
            break
        elif event == "-PREVIOUS-":
            if(i > 0):
                i -= 1
            continue

        elif event == "-ACCEPT-":
            df.at[i, 'Accepted'] = True
            if(math.isnan(row["ReadTimeStamp"])):
                df.at[i, 'ReadTimeStamp'] = int(time.time())

        elif event == "-REJECT-":
            df.at[i, 'Accepted'] = False
            if(math.isnan(row["ReadTimeStamp"])):
                df.at[i, 'ReadTimeStamp'] = int(time.time())

        if(i < (df.shape[0] - 1)):
            i += 1

    window.close()

    df.to_csv(outputFile, index=False)

# Put the interesting titles back into the dataset
def mergeDatasets(df, class1df):
    oldClass1Articles = df[df["Accepted"] == True]
    newClass1Articles = class1df[class1df["Accepted"] == True]
    class1Articles = oldClass1Articles.append(newClass1Articles, ignore_index=True)

    class1Articles.to_csv("all_class_1_articles.csv", index=False)

def resetReadInfo():
    df['ReadTimeStamp'] = None
    df['Accepted'] = None
    df.to_csv(outputFile, index=False)

def getArticlesDOIs():
    acceptedArticles = df[df['Accepted'] == True]
    # If we need to convert the "Accepted" column to bool
    acceptedArticles = acceptedArticles.astype({'DOI': 'str'})

    articlesWithDOI = []
    articlesWithoutDOI = []
    for index, row in acceptedArticles.iterrows():
        # print(row['DOI'])
        if(row['DOI'] == 'nan'):
            articlesWithoutDOI.append(row)
        else:
            articlesWithDOI.append(row['DOI'])
    
    print(articlesWithDOI)
    print("accepted articles: %d, with DOI: %d, w/o DOI: %d"%(len(acceptedArticles), len(articlesWithDOI), len(articlesWithoutDOI)))
    

if __name__ == "__main__":
    inputFile = "scopus_search_results.csv"
    outputFile = "scopus_search_results.csv"
    # ##### OPENING FILES #####
    df = pd.read_csv(inputFile, encoding='UTF-8')
    
    main(df)