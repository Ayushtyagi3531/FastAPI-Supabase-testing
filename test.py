from urllib.parse import quote

password = input("Enter database password: ")
print(quote(password, safe=""))