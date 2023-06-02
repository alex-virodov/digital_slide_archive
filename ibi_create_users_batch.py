import argparse
import traceback

import girder_client
import pandas as pd
from ibi_generate_random_password import generate_random_password

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", required=True, type=str, help="API key")
    parser.add_argument("--api_url", default='https://dsa.ai.uky.edu/api/v1', type=str, help="API url")
    parser.add_argument('--csv', default='ibi_create_users_batch.csv')
    parser.add_argument('--name_prefix', default='')
    args = parser.parse_args()
    print(f'{args=}')

    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)

    users = pd.read_csv(args.csv)
    # print(users)

    for i, row in users.iterrows():
        # print(f'{row=}')
        dsa_login = row['First'].lower() + '.' + row['Last'].lower()
        dsa_email = row['email']
        dsa_first = args.name_prefix + row['First']
        dsa_last = row['Last']
        dsa_password = generate_random_password(password_length=24)
        print(f'======\n{dsa_login=} {dsa_email=} {dsa_first=} {dsa_last=} {dsa_password=}')
        try:
            result = gc.post('/user', parameters={
                'login': dsa_login,
                'email': dsa_email,
                'firstName': dsa_first,
                'lastName': dsa_last,
                'password': dsa_password,
            })
            print(f'{result=}')
        except Exception as e:
            print(traceback.format_exc())




if __name__ == '__main__':
    main()