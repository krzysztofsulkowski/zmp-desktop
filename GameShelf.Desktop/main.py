from services.session import set_token
from services.auth_service import login, get_user_profile
from services.collection_service import get_my_collection

def main():
    email = input("Email: ")
    password = input("Password: ")

    token = login(email, password)

    if not token:
        print("Login failed")
        return

    set_token(token)

    user = get_user_profile()
    print("USER:")
    print(user)

    games = get_my_collection()

    print("GAMES:")
    for game in games:
        print(game)


if __name__ == "__main__":
    main()