# Imports
import pandas as pd
import requests
import os
import time
from datetime import datetime
import json

# Constants
BASE_URL = 'https://oauth.reddit.com/r/'
BATCH_SIZE = 100
NUM_BATCHES = 10

def main():
    # This function will authorize the user for use of the reddit API
    # Then asks what subreddit the user would like to collect data from
    # Using for-loop and pagination ('after') it will retrieve each page of post titles
    # Saves the scraped data to a csv and updates transaction log
    
    credentials = get_credentials()

    auth = requests.auth.HTTPBasicAuth(credentials['client_id'], credentials['client_secret'])

    data = {
        'grant_type': 'password',
        'username': credentials['username'],
        'password': credentials['password']
    }

    headers = {'User-Agent': 'dsb826/0.0.1'}
    
    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers)

    token = res.json()['access_token']

    headers['Authorization'] = f'bearer {token}'

    # Only going forward if we are authorized
    if requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).status_code == 200:
        
        subreddit = input('Which subreddit would you like to scrape today? ')
    
        params = {
                'limit': BATCH_SIZE,
                'after': None
            }
    
        batches = []
        for _ in range(NUM_BATCHES):
            batch, last = scrape_page(subreddit, headers, params)
            batches.append(batch)
            params['after'] = last
            
            time.sleep(2)
    
        new_df = pd.concat(batches, ignore_index = True)
    
        batch_size, total_size = write_data(new_df)
    
        update_transaction_log(batch_size, total_size)
    else:
        print('Sorry, authorization not valid.')
        

def update_transaction_log(batch_size, total_size):
    # Updates the transaction log with execution info
    # Creates a new log if one does not exist already
    
    if os.path.exists('../data/transaction_log.txt'):
        with open('../data/transaction_log.txt', 'a') as file:
            file.write(f"Execution Date: {datetime.now()} | "
                           f"Posts Retrieved: {batch_size} | "
                           f"Total Posts To Date: {total_size}\n")
        print('Transaction log updated.')
    else:
        with open ('../data/transaction_log.txt', 'w') as file:
            file.write('Log of Script Executions\n' + '='*50 + '\n')
            file.write(f"Execution Date: {datetime.now()} | "
                           f"Posts Retrieved: {batch_size} | "
                           f"Total Posts To Date: {total_size}\n")
        print('Transaction log created.')

def write_data(new_df):
    # This function removes potential duplicates before saving the newly scraped data to the main database
    # Returns the number of posts retrieved this run and the total number of posts saved to the dataframe since day one.
    if os.path.exists('../data/subreddit_data.csv'):
        existing_df = pd.read_csv('../data/subreddit_data.csv')
    else:
        existing_df = pd.DataFrame()

    combined_df = pd.concat([existing_df, new_df]).drop_duplicates(keep = 'first')

    combined_df.to_csv('../data/subreddit_data.csv', index = False)

    print('Database Updated!')

    return len(combined_df) - len(new_df), len(combined_df)

def scrape_page(subreddit, headers, params):
    # This function will retrieve the post titles and return them as a dataframe
    # It will also return the next page starting point for looping purposes
    
    res = requests.get(BASE_URL+subreddit+'/new', headers=headers, params=params)
    page = res.json()

    batch = []
    for post in page['data']['children']:
        post_info = {
            'title': post['data']['title'],
            'ID': post['data']['name'],
            'subreddit': post['data']['subreddit']
        }
        batch.append(post_info)


    return pd.DataFrame(batch), page['data']['after']

def get_credentials():
    # This function will return the authorization credentials as a dictionary
    # If the credentials were not supplied already it will write them to a new json file
    
    if os.path.exists('../data/reddit_credentials.json'):
        with open('../data/reddit_credentials.json', 'r') as file:
            credentials = json.load(file)
    else:

        client_id = input("Enter client ID: ")
        client_secret = input("Enter client secret number: ")
        user_agent = input("Enter name of application: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

        credentials = {
            'client_id': client_id,
            'client_secret': client_secret,
            'user_agent': user_agent,
            'username': username,
            'password': password
        }

        # writing credentials to json file
        with open('../data/reddit_credentials.json', 'w') as file:
            json.dump(credentials, file)

    return credentials

if __name__ == "__main__":
    main()
























