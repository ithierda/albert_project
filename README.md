# Find the best beneficiary for an accounting firm

## Overview
We have just set up our new accounting firm "Albecounting".
However, as students and young chartered accountants, we need advice.
So we want to find the best person to advise us, so we're creating a profile for him or her. So we're looking for a beneficiary.

## Data
We created our own database for this purpose from 2 sources: 
- Papers: to collect data on beneficiaries in accounting firms.
- LinkedIn: to retrieve their

By joining the 2 datasets, we obtained our final data, in order to find the beneficiary to advise us.

Here is a link to a google drive with the data : https://drive.google.com/drive/folders/1OU4Gj2SCetQyxOI3BPtzQPSEQ_rVa6zB?usp=sharing


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


