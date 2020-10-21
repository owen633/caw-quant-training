### Required

#### 1. **Use Etherscan Python SDK** to get on-chain data
from etherscan.accounts import Account
from etherscan.blocks import Blocks
from etherscan.contracts import Contract
from etherscan.proxies import Proxies
from etherscan.stats import Stats
from etherscan.tokens import Tokens
from etherscan.transactions import Transactions
import pandas as pd
import json

with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

# Accounts
## Single address
address = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'
api = Account(address=address, api_key=key)

### get balance
single_bal = api.get_balance()
print(single_bal)

### get transactions
single_trans = api.get_transaction_page(page=1, offset=10)
formatted_st = pd.DataFrame.from_dict(single_trans)
formatted_st['timeStamp'] = pd.to_datetime(formatted_st['timeStamp'], unit='s')
print(formatted_st.head(5))

### get blocks mined
single_bm = api.get_blocks_mined_page(page=1, offset=10)
formatted_bm = pd.DataFrame.from_dict(single_bm)
formatted_bm['timeStamp'] = pd.to_datetime(formatted_bm['timeStamp'], unit='s')
print(formatted_bm.head(5))

## multiple address
addresses = ['0xbb9bc244d798123fde783fcc1c72d3bb8c189413', '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a']
api = Account(address=addresses, api_key=key)
### get balance
mutiple_bal = api.get_balance_multiple()
formatted_mb = pd.DataFrame.from_dict(mutiple_bal)
print(formatted_mb.head(5))

# Blocks
block = 2165403
api = Blocks(api_key=key)
### get reward
reward = api.get_block_reward(block)
print(reward)

# Contracts
address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
### get abi
api = Contract(address=address, api_key=key)
abi = api.get_abi()
print(abi)
### get sourcecode
sourcecode = api.get_sourcecode()
print(sourcecode[0]['SourceCode'])

# Proxies
### get most recent block
api = Proxies(api_key=key)
block = api.get_most_recent_block()
print(int(block, 16))
### get transaction by blocknumber
transaction = api.get_transaction_by_blocknumber_index(block_number='0x57b2cc',
                                                       index='0x2')
formatted_trans = pd.DataFrame([transaction])
print(formatted_trans)
# get uncle by blocknumber
uncles = api.get_uncle_by_blocknumber_index(block_number='0x210A9B',
                                            index='0x0')
formatted_uncle = pd.DataFrame([uncles])
print(formatted_uncle)

# Stats
api = Stats(api_key=key)
### get ether last price
last_price = api.get_ether_last_price()
formatted_lp = pd.DataFrame([last_price])
formatted_lp['ethbtc_timestamp'] = pd.to_datetime(formatted_lp['ethbtc_timestamp'], unit='s')
formatted_lp['ethusd_timestamp'] = pd.to_datetime(formatted_lp['ethusd_timestamp'], unit='s')
print(formatted_lp)
### get total ether supply
tot_ether = api.get_total_ether_supply()
print(tot_ether)

# Tokens
contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
api = Tokens(contract_address=contract_address, api_key=key)
### get token balance of an address
address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
token_bal = api.get_token_balance(address=address)
print(token_bal)
# get total supply of tokens
token_supp = api.get_total_supply()
print(token_supp)

# Transactions
TX_HASH = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'
api = Transactions(api_key=key)
### get status
status = api.get_status(tx_hash=TX_HASH)
print(status)
### get receipt status
TX_HASH = '0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76'
api = Transactions(api_key=key)
receipt_status = api.get_tx_receipt_status(tx_hash=TX_HASH)
print(receipt_status)




## 2. Explore CryptoControl data API
from crypto_news_api import CryptoControlAPI

api = CryptoControlAPI("c707fd08bf46e30a653fab28ff6eab1e")

proxyApi = CryptoControlAPI("c707fd08bf46e30a653fab28ff6eab1e", "http://cryptocontrol_proxy/api/v1/public")


# Get top news
tn = api.getTopNews()
formatted_tn = pd.DataFrame.from_dict(tn)
print(formatted_tn.head(5))

# get latest chinese news
cn = api.getLatestNews("cn")
formatted_cn = pd.DataFrame.from_dict(cn)
print(formatted_cn.head(5))

# get top bitcoin news
btcn = api.getTopNewsByCoin("bitcoin")
formatted_btcn = pd.DataFrame.from_dict(btcn)
print(formatted_btcn.head(5))

# get top bitcoin tweets
btct = api.getTopTweetsByCoin("bitcoin")
formatted_btct = pd.DataFrame.from_dict(btct)
print(formatted_btct.head(5))

# get top bitcoin reddit posts
btcr = api.getLatestRedditPostsByCoin("bitcoin")
formatted_btcr = pd.DataFrame.from_dict(btcr)
print(formatted_btcr.head(5))

# get reddit/tweets/articles in a single combined feed for bitcoin
comb = api.getTopFeedByCoin("bitcoin")
formatted_comb = pd.DataFrame.from_dict(comb)
print(formatted_comb.head(5))

# get latest reddit/tweets/articles (seperated) for Litecoin
lc = api.getLatestItemsByCoin("litecoin")
formatted_lc = pd.DataFrame.from_dict(lc)
print(formatted_lc.head(5))

# get details (subreddits, twitter handles, description, links) for ethereum
eth = api.getCoinDetails("ethereum")
formatted_eth = pd.DataFrame([eth])
print(formatted_eth)
