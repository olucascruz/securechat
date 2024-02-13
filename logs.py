def login_log(data_request):
    # Create new pair keys log
    print("\n" + "---" * 10 + "LOG : User registered" + "---" * 10)
    print("\nUsername: ", data_request["username"])
    print("\nPublic Key Serialized:\n\n", data_request["public_key"])
    print("---" * 70 + "\n\n")

def register_log(data_request):
    print("\n" + "---" * 15 + "LOG : Server is receiving the public key because user create a new account" + "---" * 15)
    print("\nUsername: ", data_request["username"])
    print("---" * 40 + "\n\n")