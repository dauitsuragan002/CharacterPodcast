# pip install characterai
# This module handles user authentication for CharacterAI using email-based sign-in.

from characterai import aiocai, sendCode, authUser

user_email = "example@gmail.com"
sendCode(user_email)
link = input("Please check your email for the sign-in link and paste it here: ")
token_user = authUser(link=link, email=user_email)

print(f"User token: {token_user}")
save_path = "user_token.txt"
with open(save_path, "w") as file:
    file.write(f'char_token="{token_user}"')
