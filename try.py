# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
import copy 
  

# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(filename) 
#         print(os.path.join(dirname, filename))


train = pd.read_csv (r'/kaggle/input/iqb2020/train.csv')
test = pd.read_csv (r'/kaggle/input/iqb2020/sample.csv')
sample = pd.read_csv (r'/kaggle/input/iqb2020/sample.csv')



sequences = train["Sequence"]
final_train = train["Lable"]
ID = train["ID"]


#Feature 1 - Composition (adding 20 columns)
composition = []
residues = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
for row in train.itertuples(): 
    sequence = row[3]
    length = len(sequence)
    temp = []
    for residue in residues:
        count = 0
        for i in sequence:
            if(i == residue):
                count+=1
        presence = count/length
        temp.append(presence*100)
    composition.append(temp)


for i in range(20):
    res = residues[i]
    temp = []
    for j in composition:
        temp.append(j[i])
    train[res] = temp
print("done1")

# Feature 2 - Dipeptide composition (adding 400 columns)

all_pairs = []
for i in range(20):
    res1 = residues[i]
    for j in range(20):
        res2 = residues[j]
        all_pairs.append(res1+"-"+res2)
        
dipep_data = []
for row in train.itertuples():
    sequence = row[3]
    length = len(sequence)
    pairs = {}
    for i in range(20):
        res1 = residues[i]
        for j in range(20):
            res2 = residues[j]
            pairs[res1+"-"+res2] = 0
    
    for i in range(length-1):
        pairs[sequence[i]+"-"+sequence[i+1]] += 1
    
    values = []
    for key,value in pairs.items():
        values.append((value/(length-1))*100)
    
    dipep_data.append(values)

for pair in range(400):
    temp = []
    for data in dipep_data:
        temp.append(data[pair])
    train[all_pairs[pair]] = temp
    
    
    
    
        
        
        



        
print("done2")

        

# Feature 5 - mass, charge, pi (adding 3 columns)
# charge and pi left
mass = {"A" : 89.1,"R" : 174.2,"N" : 132.1,"D" : 133.1,"C" : 121.2,"E" :147.1, "Q" : 146.2, "G" : 146.2,"H" : 155.2,"I" : 131.2,"L" : 131.2,"K" : 146.2,"M" : 149.2, "F" : 165.2 , "P": 115.1, "S" : 105.1,"T" : 119.1,"W" : 204.2, "Y" : 181.2, "V" : 117.1}

masses = []
for row in train.itertuples(): 
    sequence = row[3]
    temp = 0
    for i in sequence:
        temp+=mass[i]
    masses.append(temp)

train["mass"] = masses
print("done3")



# X_train, X_test, y_train, y_test = train_test_split(sequences,Lable)

# print(X_train)
# X_train= X_train.values.reshape(-1, 1)
# y_train= y_train.values.reshape(-1, 1)
# X_test= X_test.values.reshape(-1, 1)
# y_test= y_test.values.reshape(-1, 1)


# print(1)
# cls = svm.SVC(kernel="rbf")
# print(2)
# cls.fit(X_train,y_train)
# print(3)
# pred = cls.predict(X_test)

# print("accuracy:", metrics.accuracy_score(y_test,y_pred=pred))


# print("done")
# Any results you write to the current directory are saved as output.

# print("Hello")