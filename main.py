from web3 import Web3
from time import sleep
import tomli
import pyfiglet

web3 = None
config_data = None


def send_ETH(private_key, from_address, to_address, amount):
    tx = {
        'type': '0x2',
        'nonce': web3.eth.get_transaction_count(from_address),
        'from': from_address,
        'to': to_address,
        'value': web3.to_wei(amount, 'ether') - 21000*web3.to_wei('38', 'gwei'),
        'gas': 21000,
        'maxFeePerGas': web3.to_wei('38', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('38', 'gwei'),
        'chainId': 1
    }
    print(web3.to_wei(amount, 'ether'))
    print(21000*web3.to_wei('38', 'gwei'))
    print(web3.to_wei(amount, 'ether') - 21000*web3.to_wei('38', 'gwei'))

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt['status'] == 1:
        print('ETH transferred successfully! Hash: {}'.format(str(web3.toHex(tx_hash))))
    else:
        print('There was an error transferring the ETH')


def fetch_balance(from_account):
    check_sum = web3.to_checksum_address(from_account)
    balance = web3.eth.get_balance(check_sum)
    ether_value = web3.from_wei(balance, 'ether')
    return ether_value


def eth_sweeper_bot():
    while True:

        for _, data in enumerate(config_data['wallets']):
            print(f"checking wallet {data['address']}")
            wallet_balance = fetch_balance(data['address'])
        if wallet_balance > 0:
            print("---  ETH wallet has balance!! ----")
            print(wallet_balance)
            print("--- Executing sweeper transaction ---")
            send_ETH(data['privateKey'], data['address'], config_data['config']['toWallet'], wallet_balance)
        # else:
        #    print("--- Empty wallet ---")
        sleep(0.10)


if __name__ == '__main__':
    try:
        with open("config/config.toml", "rb") as f:
            config_data = tomli.load(f)
    except tomli.TOMLDecodeError:
        print("Yep, toml definitely not valid.")

    print(pyfiglet.figlet_format("Sweepy!!"))
    web3 = Web3(Web3.HTTPProvider(config_data["config"]["infura"]))
    if web3.is_connected():
        print("--- Bot connected to blockchain successfully ---")
        eth_sweeper_bot()
