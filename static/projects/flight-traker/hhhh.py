SHEETY_USERS_ENDPOINT = 'https://api.sheety.co/ac9cdf0bd90ae8a92a3148ad9e473309/flightDealsProject/users'
import requests
# sheety_response = requests.get(url=SHEETY_USERS_ENDPOINT)
# sheety_response.raise_for_status()
# destination_data = sheety_response.json()
# print(destination_data)

print("Welcome! Please provide the following information")
first_name = input("What's your first name? ")
last_name = input("What's your last name? ")
email = input("What's your email? ")
email_2 = input("Please renter your email: ")
n = 2

if email == email_2:
    row_id = n
    sheety_update = f"{SHEETY_USERS_ENDPOINT}/{row_id}"
    update_params = {
        "users": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }
    update_row = requests.put(url=sheety_update, json=update_params)
    update_row.raise_for_status()
