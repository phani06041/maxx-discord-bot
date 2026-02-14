from crypto_utils import generate_key, encrypt_data

key = generate_key()

discord_token = "YOUR_DISCORD_BOT_TOKEN_HERE"

encrypted_token = encrypt_data(discord_token, key)

with open("secrets.enc", "wb") as f:
    f.write(encrypted_token)

print("SAVE THIS KEY IN .env FILE:")
print(key.decode())
