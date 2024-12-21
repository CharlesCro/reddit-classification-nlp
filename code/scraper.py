# Standard libraries
import os
import time
from datetime import datetime
import json

# Non-standard libraries
import pandas as pd
import requests

# Constants
BASE_URL = 'https://oauth.reddit.com/r/'
BATCH_SIZE = 100
NUM_BATCHES = 10

def main():
    '''
    Authenticate with the Reddit API, scrape subreddit data, and update records.

    This function performs the following tasks:
    1. Authenticates with the Reddit API using credentials.
    2. Prompts the user for a subreddit to scrape.
    3. Scrapes data from the specified subreddit in multiple batches.
    4. Writes the scraped data to a file and updates the transaction log.

    Steps:
    - Retrieves OAuth2 token for Reddit API.
    - Validates authorization before proceeding.
    - Iteratively fetches subreddit data and processes it.
    - Updates and logs results.

    Raises:
        Exception: If authorization with the Reddit API fails.
    '''
    
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
    
        new_batch_titles = pd.concat(batches, ignore_index = True)
    
        batch_size, total_size = write_data(new_batch_titles)
    
        update_transaction_log(batch_size, total_size)
    else:
        print('Sorry, authorization not valid.')
        

def update_transaction_log(batch_size, total_size):
    '''
    Update or create a transaction log for the script execution.

    This function logs the details of each script execution, including the
    execution date, the number of posts retrieved in the current batch,
    and the total number of posts retrieved to date. If the transaction log
    file does not exist, it creates a new one.

    Parameters:
        batch_size (int): The number of posts retrieved in the current execution.
        total_size (int): The cumulative total of posts retrieved to date.

    Returns:
        None
    '''

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

def write_data(new_batch_titles, file_name = 'subreddit_data.csv'):
    '''
    Update or create a CSV file with subreddit post titles.

    This function appends new subreddit post titles to an existing dataset,
    removes duplicates, and writes the updated data to a CSV file.

    Parameters:
        new_batch_titles (DataFrame): A pandas DataFrame containing new subreddit post titles.
        file_name (str): The name of the file to update or create. Defaults to 'subreddit_data.csv'.

    Returns:
        tuple: A tuple containing:
            - (int) The number of duplicate posts removed.
            - (int) The total number of posts in the updated dataset.
    '''

    if os.path.exists('../data/subreddit_data.csv'):
        stored_titles = pd.read_csv('../data/subreddit_data.csv')
    else:
        stored_titles = pd.DataFrame()

    updated_titles = pd.concat([stored_titles, new_batch_titles]).drop_duplicates(keep = 'first')

    updated_titles.to_csv(f'../data/{file_name}', index = False)

    print('Database Updated!')

    return len(updated_titles) - len(new_batch_titles), len(updated_titles)

def scrape_page(subreddit, headers, params):
    '''
    Retrieve and parse subreddit posts from Reddit's API.

    This function fetches the latest posts from a specified subreddit, extracts
    relevant information (title, ID, subreddit name), and returns it as a pandas
    DataFrame. It also returns the `after` token for pagination.

    Parameters:
        subreddit (str): The name of the subreddit to scrape.
        headers (dict): The HTTP headers for the API request, including authentication.
        params (dict): Parameters for the API request, including pagination info.

    Returns:
        tuple: A tuple containing:
            - (DataFrame) A pandas DataFrame of the post data (title, ID, subreddit).
            - (str or None) The `after` token for the next page of results, or None if there are no more results.
    '''
    
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
    '''
    Retrieve Reddit API credentials from a file or user input.

    This function checks if a file containing Reddit API credentials exists.
    If the file exists, it loads and returns the credentials. If the file
    does not exist, it prompts the user to input the required credentials
    (client ID, client secret, user agent, username, and password), and then
    saves them to a JSON file for future use.

    Returns:
        dict: A dictionary containing the Reddit API credentials:
            - 'client_id': The Reddit client ID.
            - 'client_secret': The Reddit client secret.
            - 'user_agent': The application user agent string.
            - 'username': The Reddit username.
            - 'password': The Reddit password.
    '''
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
























