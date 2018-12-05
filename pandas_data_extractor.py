#import openpyxl
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import csv
import datetime
import win32com.client
from babel.numbers import format_decimal

def refresh_cc_sheets(path,input_file,countries):
    """
    Opens each file in the path tries to refresh the links and performs Refresh All in Excel
    """

# Open Excel
    
    Application = win32com.client.Dispatch("Excel.Application")
 
 # Show Excel. While this is not required, it can help with debugging
    Application.Visible = 0
    Application.DisplayAlerts=False
    Application.AskToUpdateLinks = False

    for  country in countries.values():
 # Open Your Workbook
        Workbook = Application.Workbooks.open(path + input_file + country + '.xlsx')
        try:
            Workbook.UpdateLink(Name=Workbook.LinkSources())

        except Exception as e:
            print(e)
        # Refesh All
        Workbook.RefreshAll()
        Application.CalculateUntilAsyncQueriesDone()
        print(country + ' - Done')
    # Saves the Workbook
        Workbook.Save()
        Workbook.Close()
    Application.Visible = 0
    Application.DisplayAlerts=True
    Application.AskToUpdateLinks = True
 # Closes Excel
    Application.Quit()

def extract_data():
    now=datetime.datetime.now()
    #cur_date=now.strftime("%Y%m%d")
    #dictionary for iterating between files 
    countries={2:"UK"}
    path='Z:\\800-Management\\830-Controlling\\833-Marketing\\Channel Controlling 2018\\'
    input_file='Channel Controlling 2018 '
    print('Started at: {}'.format(now.strftime("%H:%M")))

    #refresh_cc_sheets(path,input_file,countries)


    with open(path + 'DailyCostExtraction'+ '.csv', 'w', newline='') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['AffiliateGroup', 'Date', 'Cost', 'CountryId'])

    for c_id, country in countries.items():


        #open the workbook
        started=datetime.datetime.now().strftime("%H:%M")
        #wb = pd.read_excel(path + input_file + country + '.xlsx',  header=1) #openpyxl.load_workbook(path + input_file + country + '.xlsx',read_only=True, data_only=True)
        #wb = pd.ExcelFile(path + input_file + country + '.xlsx')
        with pd.ExcelFile(path + input_file + country + '.xlsx') as xls:
            print(xls.sheet_names)
            sheet = pd.read_excel(xls, xls.sheet_names[1], header=1)
            print("Column headings:")
            print(sheet.columns)
            xls.close()
        """

        sheets =  wb. #list of sheet names
        print(sheets)

        #removing summary, beispiel and data pivot sheets
        i=0
        while i <=1:
            sheets.pop(0)
            i+=1
        sheets.pop()
        
        #iterating between the sheets and extracting the data
        for sheet in sheets:
            print(sheet)
            #preparing lists for data that will be extracted from each sheet
            dates=[]
            costs=[]
            aff_group=[]
            country_id=[]
            data=[]
            sheet=wb[sheet]
            sheet_name=sheet[502][0].value
            # extracting only cost and date
            for row in sheet.iter_rows(min_row=3,max_row=408, min_col=1, max_col=7):
                datum = row[0].value
                cost = row[6].value
                #removing blank cells
                if datum == None:
                    continue
                if cost not in [None,0,'#N/A','#VALUE!','#REF!']:
                    #adding data to list
                    dates.append(datum.strftime("%Y-%m-%d"))
                    costs.append(format_decimal(cost, locale='de_DE')) #formating numbers in German style
                    aff_group.append(sheet_name)
                    country_id.append(c_id)
            #putting lists together into a list of tuples 
            data=list(zip(aff_group,dates,costs,country_id))
        
                #wiriting into the csv file
            with open(path + 'DailyCostExtraction'+ '.csv', 'a+', newline='') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for value in data:
                    filewriter.writerow(value)
            #log also the sheet names for debugging        
            #with open(path + 'log'+ '.csv', 'a+', newline='') as csvfile:
            #    filewriter = csv.writer(csvfile, delimiter=',',
            #                                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #   filewriter.writerow([sheet_name,'Done'])

        print('{}{} Done Started at:{} Ended at:{}'.format(input_file,country,started,datetime.datetime.now().strftime("%H:%M")))

"""   
        #wb.close
    now=datetime.datetime.now()
    print('Ended at: {}'.format(now.strftime("%H:%M")))

if __name__ == "__main__":
    extract_data()