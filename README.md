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

We recovered data from our 3 sources using scrapping methods with the Selenium library.

By joining the 3 datasets, we obtained our final data, in order to find the beneficiary to advise us.

### Data Quality/Cleaning/Preparation


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

Based on these characteristics, we'll create clusters according to this, and then predict the ebitda ratio of each cluster using machine learning.
We then keep the best cluster and obtain the best type of beneficiary to advise us.

Bonus: we have a list of these beneficiaries and can contact them.

## Installation
Provide step-by-step instructions on how to get a development environment running.

```bash
git clone https://github.com/username/projectname.git
cd projectname
pip install -r requirements.txt


