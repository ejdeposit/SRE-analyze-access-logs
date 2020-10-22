import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

#def get_resource_class(path):
#    pathSplit = path.split('/')
#    if len(pathSplit) > 3:
#        return pathSplit[1]
#    else:
#        return 
    
def get_resource_type(path):
    pathSplit = path.split('/')
    length = len(pathSplit)
    if pathSplit[length - 1] == "":
        resourceType = 'dir'
    else: 
        pathSplit = pathSplit[length-1].split('.')
        #case 1: period
        if len(pathSplit) > 1:
            resourceType = pathSplit[1]
        else:
            pathSplit = pathSplit[0].split('?')
            resourceType = pathSplit[0]

    return resourceType   
    

logfilename = 'nasa_access_log_500k.csv'

print(f"reading file: {logfilename}")
df = pd.read_csv(logfilename, low_memory=False, parse_dates=['timestamp'])



# Question 1. What is the date range for this access log?

#print("\nQuestion 1:\n\tcalculate date range")
#mindate = min(df['timestamp']).date()
#maxdate = max(df['timestamp']).date()
#print (f"\tdate range: {mindate} to {maxdate}")

# Question 2. Display a pie chart of in which each pie slice 
# represents a response code and the size of the pie piece is 
# proportional to the number of responses with that code.

#print("\nQuestion 2: response code pie chart")
#vc = df['rcode'].value_counts()
#print(f"\nValue Counts for 'rcode':\n{vc}")
#vc.plot.pie(figsize=(10,10))
#plt.show()

#question 3
#- how many unique clients
print()
print("\nQuestion 3")
print('unique clients', len(df.clientloc.unique()))

#question 4
# - Which Client accessed this service the most?
print()
print("Question 4")
vc = df['clientloc'].value_counts()
print("top 5 clients")
print(vc.head(n=5))

#question 6
# - Which resource (path) was accessed the most?
print()
print("Question 6")
vc = df['path'].value_counts()
print("top path: ")
print(vc.head(n=11))

#question 7
# - The First element in the path indicates a resource class.  Lit all the accessed resource classes?
print()
print("Question 7")
df['resourceclass'] = df['path'].apply(lambda x: x.split('/')[1] if len(x.split('/')) >= 3 else np.nan )
vc = df['resourceclass'].value_counts()
print(vc)
#print(vc.head(n=20))


# 8. Display a histogram showing the frequency of access for each resource class.
#print("\nQuestion 8:")
vc.head(n=15).plot.bar()
plt.show()

#question 9 
# - Which day of the week ad the most requests 
print()
print("Question 9")
df['dayofweek'] = df['timestamp'].apply(lambda x: x.dayofweek)
vc = df['dayofweek'].value_counts()
print(vc)

#question 10 
#  - Which hour of the day did the site typicaly serve the most data
print()
print("Question 10")
df['hourofday'] = df['timestamp'].apply(lambda x: x.hour)
groupSum = df.groupby(['hourofday'])['rsize'].sum()
print(groupSum)

#question 11
#  - What was the availability of this site?" + 
# "Comute availability as the number of non-error responses divide by the total number of requests
#200 - ok
#redirect
#304 - not modified, no need to retransmit since client still has prev downloaded copy 
#302 - found (previously "moved temporaitly") redirect of some sort
#client errors
#404 - not found
#403 - forbidden
#server errors
#501 - not implemented
#500 - internal sever error
print()
print("Question 11")
#determine different reponse types
#vc = df['rcode'].value_counts()
#print("top reponse codes: ")
#print(vc)

#sum of the group
df['grouprcode'] = df['rcode'].apply(lambda x: str(x)[0:1:])
groupSums = df['grouprcode'].value_counts()
internalServerErrors = groupSums['5']
print('internal server errors: ', internalServerErrors)

#total number of responses
totalRequests = len(df.rcode)
print('number of responses:', totalRequests)

#sum/total number
print('availability = non-error requests / total requests =  ', (totalRequests - internalServerErrors) / totalRequests )

#question 12   
# - How many different ytpes of resources were servered
print()
print('Question 12')
#split by / if last element is empty then / else split on . and use last element of list
df['resourceType'] = df['path'].apply(get_resource_type)
vc = df['resourceType'].value_counts()
#print(vc)
print(vc.head(n=20))

#question 13
#: calculate how much data was served for that resource type
#For each of the resource types found in question 7, calculate how much data was served for that resource type.
#  Sum all of the rsize values for all of the requests for each resource type to compute this value.
print()
print('Question 13')
groupSum = df.groupby(['resourceclass'])['rsize'].sum()
print(groupSum)



#question 15 - pie chart

#question 16 - just question

#question 17 - time between requests



#vc.nlargest(5).plot.bar()
#plt.show()

#vc.nlargest(5).plot.bar(figsize=(10,10))
#plt.xticks(rotation=30, horizontalalignment="center")
#plt.show()

