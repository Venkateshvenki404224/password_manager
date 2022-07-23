import requests
# import hashlib
#
# password = input("Enter the password to check! :")
# sha_password = hashlib.sha1(password.encode()).hexdigest()
# sha_prefix = sha_password[0:5]
# sha_postfix = sha_password[5:].upper()
#
# url = "https://api.pwnedpasswords.com/range/" + sha_prefix
# payload ={}
# headers ={}
# responce = requests.request("GET",url,headers=headers,data=payload)
# pwnd_dict={ }
# pwnd_list = responce.text.split("\r\n")
# for pwnd_pass in pwnd_list:
#     pwnd_hash = pwnd_pass.split(":")
#     pwnd_dict[pwnd_hash[0]] = pwnd_hash[1]
#
# if sha_postfix in pwnd_dict.keys():
#     print(f"Your password have been found {pwnd_dict[sha_postfix]} times")
# else:
#     print("You password is safe!")
#
#
