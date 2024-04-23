# Find the best beneficiary for an accounting firm

## Overview
We have just set up our new accounting firm "Albecounting".
However, as students and young chartered accountants, we need advice.
So we want to find the best person to advise us, so we're creating a profile for him or her. So we're looking for a beneficiary.

## Data
### Data content
We created our own database for this purpose from 3 sources:
- Directory of chartered accountants: to collect data on beneficiaries
- Papers: to collect data on accounting firms
- LinkedIn: to retrieve their training 

We retrieved data from our 3 sources using scrapping methods with the Selenium, Beautiful Soup and Request libraries.

Our aim was really to recover as much data as possible, as there was a real purpose behind it: to contact the beneficiaries. We have a lot of contact information etc.

By joining the 3 datasets, we obtained our final data, in order to find the beneficiary to advise us.

### Data Quality/Cleaning/Preparation
We had to deal with data problems. They were not "clean" and had several NaNs. We dealt with these cases.
We also had a typical case to deal with in the 'company size' column. We often found ourselves with data 'between 5 and 10 people'. For this, we set up an algorithm to keep only the numbers in the string (5-10) and average them out to 7.5 employees.

Here is a link to a google drive with the cleaned data : https://drive.google.com/drive/folders/1OU4Gj2SCetQyxOI3BPtzQPSEQ_rVa6zB?usp=sharing


## Features
(As a reminder: the "best beneficiary" is the one who offers us the best EBITDA ratio).

These are the features on which we're going to train our models: 
- address
- beneficiary age
- education
- company size
- number of chartered accountants

## Machine Learning

Based on these characteristics, we ran a classical linear regression to predict EBITDA. Then we made clusters without the EBITDA data, just with the beneficiary data. So we have a cluster center that models an average beneficiary (we have 3 clusters).
We'll now take the center of this cluster and predict the EBITDA, and we'll choose the highest EBITDA among the 3 clusters. This gives us our typical profit.
We'll then select from our original table with all the contacts, the set of beneficiaries that correspond to our typical beneficiary

Bonus: we have a list of these beneficiaries and can contact them.

## Installation
Provide step-by-step instructions on how to get a development environment running.

```bash
git clone https://github.com/username/projectname.git
cd projectname
pip install -r requirements.txt


