print(
    """Hello, world!
What is your name?"""
)

while True:
    user_name = input()
    if isinstance(user_name, str):
        # print(f"{user_name}")
        break
    else:
        print("Please enter your name, not a number or other things.")

print(f"Hello, {user_name}")
