from fastapi import APIRouter, Depends, HTTPException, status, Path
import requests
import json
url = 'https://sandbox.belvo.com'
secretId = 'd6475ee0-c456-43a0-bf6b-de19476239e2'
secretPassword = 'W5n#Uy8GKuFFDdWNQaKe#2@@LOdNJyHRkF9-IBZUnEYTqzZ99UQ2CU@*Mxzvkqh4'

router = APIRouter()


@router.get("/banks")
async def get_banks():
    response = requests.get(url + '/api/institutions/?page=1', auth=(secretId, secretPassword))
    print(response)
    try:
        data = response.json()
        return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error: {e.msg}")
        raise HTTPException(status_code=401, detail=f"Error: {e.msg}")


@router.get("/banks/{bank_id}")
async def get_bank_by_id(bank_id: int = Path(gt=0)):
    response = requests.get(url + '/api/institutions/' + str(bank_id), auth=(secretId, secretPassword))
    print(response)
    try:
        data = response.json()
        return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error: {e.msg}")
        raise HTTPException(status_code=401, detail=f"Error: {e.msg}")


@router.get("/bank/{bank_name}")
async def get_accounts_by_bank(bank_name: str):
    response = requests.get(url + '/api/links/?page=1', auth=(secretId, secretPassword))
    account_id = None
    print(bank_name)
    try:
        data = response.json()
        for account in data['results']:
            if account['institution'] == bank_name:
                account_id = account['id']
                break
        if account_id is None:
            raise ValueError(f"No account with name '{bank_name}' found.")
        params = {"link": account_id, "token": "1234ab", "save_data": True}
        accounts_response = requests.post(url + '/api/accounts/', auth=(secretId, secretPassword), json=params)
        account_data = accounts_response.json()
        return account_data
    except json.decoder.JSONDecodeError as e:
        print(f"Error: {e.msg}")
        raise HTTPException(status_code=401, detail=f"Error: {e.msg}")


@router.get("/transactions/{bank_link}/{account_id}")
async def get_transactions_by_id(bank_link: str, account_id: str):
    response = requests.get(url + '/api/transactions/?page=1&link=' + str(bank_link) + '&accountaccount=' + str(account_id), auth=(secretId, secretPassword))
    print(response)
    try:
        data = response.json()
        return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error: {e.msg}")
        raise HTTPException(status_code=401, detail=f"Error: {e.msg}")

