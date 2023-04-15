from queries import *
from shroomdk import ShroomDK
import statistics
import matplotlib.pyplot as plt

sdk = ShroomDK("api-key")

deposits = sdk.query(V4_TOKEN_DEPOSIT).records
prices = sdk.query(TOKEN_PRICES).records


# Organize prices
# p
# L date
#    L mint

p = {}
for x in prices:
    if x["date"] in p:
        p[x["date"]][x["mint"]] = x["price"]
    else:
        p[x["date"]] = {x["mint"]: x["price"]}

############

sol = "So11111111111111111111111111111111111111112"  # WSOL token address
addr = "78b8f4cGCwmZ9ysPFMWLaLTkkaYnUjwMJYStWe5RTSSX"  # Mango deposit account address
arr = []

for tx in deposits:
    index = 0
    date = tx["date"]
    # Find account index
    for i, account in enumerate(tx["account_keys"]):
        if account["pubkey"] == addr:
            index = i
            break

    # SOL balance change
    pre_sol = tx["pre_balances"][i]
    post_sol = tx["post_balances"][i]
    delta_sol = post_sol - pre_sol

    # Token balance change
    pre_token = 0
    for acc in tx["pre_token_balances"]:
        if acc["owner"] == addr:
            mint = acc["mint"]
            info = acc["uiTokenAmount"]
            pre_token = info["uiAmount"]
            pre_token = 0 if pre_token == None else pre_token
            break

    post_token = 0
    for acc in tx["post_token_balances"]:
        if acc["owner"] == addr:
            info = acc["uiTokenAmount"]
            post_token = info["uiAmount"]
            break

    # USD values
    sol_price = p[date][sol]
    sol_value = delta_sol * sol_price

    delta_token = post_token - pre_token
    token_price = p[date][mint]
    token_value = delta_token * token_price

    # Ignore negative values
    if sol_value + token_value > 0:
        arr.append(sol_value + token_value)

arr.sort()

print(statistics.mean(arr))
print(statistics.median(arr))
print(max(arr))

under_1000 = [x for x in arr if x <= 1000]
over_20000 = [x for x in arr if x > 20000]

# Complete graph
# plt.hist(arr)
# plt.xlabel('Deposit Value in USD')
# plt.ylabel('Number of Deposits')
# plt.title('Frequency of Deposit Values in USD')
# plt.show()

# Over $20000 graph
# plt.hist(over_20000)
# plt.xlabel('Deposit Value in USD')
# plt.ylabel('Number of Deposits')
# plt.title('Frequency of Deposit Values in USD (> $20000)')
# plt.show()

# Over $1000 graph
# plt.hist(under_1000, bins=20)
# plt.xlabel('Deposit Value in USD')
# plt.ylabel('Number of Deposits')
# plt.title('Frequency of Deposit Values in USD (<= $1000)')
# plt.xticks([x*100 for x in range(10)])
# plt.show()
