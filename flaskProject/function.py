import random
import re
import string

# Check Mail
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    if re.fullmatch(regex, email):
        return True


# Generate a uniqe device seceret.
def generatescreat(length=15):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# def find_user():
#     cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST':
#         email = request.form['email']
#         cursor.execute('SELECT * FROM users WHERE emailid=%s', (email))
#         info = cursor.fetchone()
#         print(info)
#         if info is not None:
#             if check(email) == True:
#                 if info['emailid'] == email:
#                     flash('Email id already in use!')
#             else:
#                 flash('Enter valid emaid id ')
