import bcrypt

password = "123456"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
senhaNoBanco = hashed_password.decode('utf-8')  # Convert bytes to string

transformaSenhaDoBancoEmBytes = senhaNoBanco.encode('utf-8')

isHashedTrue = bcrypt.checkpw(password.encode(), transformaSenhaDoBancoEmBytes)
print(isHashedTrue) 