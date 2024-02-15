# Adv DB Winter 2024 - 1

import random
import os
import csv

data_base = []  # Global binding for the Database contents
databaseUpdate = []

'''
transactions = [['id1',' attribute2', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''
transactions = [['1', 'Department', 'Music'], ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000']]


DB_Log = [] # <-- You WILL populate this as you go

def recovery_script(log:list):  #<--- Your CODE
    logItem = log[-1]
    attributeLoc = -1
    structKey = data_base[0]

    # Restore the database to stable and sound condition, by processing the DB log.
    print("Calling your recovery script with DB_Log as an argument.")
    print("Recovery in process ...\n")    
    
    for select in range(len(structKey)):        # Loop identifies attribute
        if logItem[1] == structKey[select]:
            attributeLoc = select
            break
        
    for index in range(1, len(data_base)):      # Loop traverses to row based on ID
        currentRow = data_base[index]
        if logItem[0] == currentRow[0]:         # Checks ID of last log failure in Database
            rowSelect = data_base[index]
            print("Transaction Failure: ",logItem)
            print("Database Row Before: ", currentRow)
            imageDB = logItem[2]
            rowSelect[attributeLoc] = imageDB[0]
            print("Database Row After:  ", currentRow, '\n')
            break   
    
    # for index in range(log):
    #     break

    pass

'''
# Log System Data Structure:
logDataStruct = ['id', 'attribute', ('valueBefore','valueAfter')]

Justification for data structure is due to simplicity of assignment, linear approach 
where index is used as a primary key (albeit, not good practice outside of this). 
'id' maintains a primary key to what row has been changed, 'attribute' to select said
attribute within the .csv file, and a tuple of the value before and after to log the change.
This tuple is a simplistic before and after image, but done here and now to streamline this
assignment that I left a little late.
'''
def transaction_processing(transactionNo:int): #<-- Your CODE
    transaction = transactions[transactionNo]
    attributeBefore = ''
    attributeLoc = -1
    structKey = data_base[0]
    
    
    for select in range(len(structKey)):      # Loop identifies attribute
        if transaction[1] == structKey[select]:
            attributeLoc = select
            break  

    for index in range(1, len(data_base)):      # Loop traverses to row based on ID
        currentRow = data_base[index]
        if transaction[0] == currentRow[0]:     # Checks ID of transaction in Database
            rowSelect = data_base[index]
            attributeBefore = rowSelect[attributeLoc]
            # print("Row before update: ", rowSelect)
            rowSelect[attributeLoc] = transaction[2]
            # print("Row after update: ", rowSelect)        
            break   
        
    logDS = [transaction[0], transaction[1], (attributeBefore, transaction[2])]
    DB_Log.append(logDS) # Log updated here

    '''
    1. Process transaction in the transaction queue.
    2. Updates DB_Log accordingly
    3. This function does NOT commit the updates, just execute them
    '''
    pass


def read_file(file_name:str)->list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists
    '''
    data = []
    #
    # one line at-a-time reading file
    #
    print(file_name)
    print(os.getcwd())
    with open(file_name, 'r') as reader:
    # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = line.strip().split(',')
            data.append(line)
             # get the next line
            line = reader.readline()

    size = len(data)
    print('The data entries BEFORE updates are presented below:') #output marker start
    for item in data:
        print(item)
    print(f"\nThere are {size} records in the database, including one header.\n")
    return data

def is_there_a_failure()->bool:
    '''
    Simulates randomly a failure, returning True or False, accordingly
    '''
    value = random.randint(0,1)
    if value == 1:
        result = True
    else:
        result = False
    return result

def main():
    number_of_transactions = len(transactions)
    must_recover = False
    global data_base
    data_base = read_file('Employees_DB_ADV.csv')
    #databaseUpdate = data_base
    failure = False #is_there_a_failure()   # Results in no change if first roll is True, changed default to False
    failing_transaction_index = None
    commit = False                          # Added to properly exit after committing all three transactions
    
    csv_file = 'Employees_UPDATED.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_base)     
    
    while not failure:                      # Results in infinite loop if all rolls are False
        # Process transaction

        for index in range(number_of_transactions):
            print(f"\nProcessing transaction No. {index+1}.")    #<--- Your CODE (Call function transaction_processing)
            transaction_processing(index)
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            if failure:
                must_recover = True
                failing_transaction_index = index + 1
                print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
                break
            else:
                csv_file = 'Employees_UPDATED.csv'
                with open(csv_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data_base)                
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
                
            if ((index) >= 2):
                commit = True
                 
        if (commit == True):
            # Handle Commit here

            break
                
    if must_recover:
        #Call your recovery script
        recovery_script(DB_Log) ### Call the recovery function to restore DB to sound state
    else:
        # All transactiones ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")

    print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:') #output marker end
    for item in data_base:
        print(item)

main()


