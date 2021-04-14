from brownie import APIConsumer, accounts, chain,config, interface, network, Contract
import time

def main():
    dev = accounts.from_mnemonic(config["wallets"]["from_mnemonic"])
    APIConsumer.deploy(
        config["networks"][network.show_active()]["oracle"],
        config["networks"][network.show_active()]["jobId"],
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["link_token"],
        {"from": dev},
        publish_source=config["verify"],
    )
    api_contract = APIConsumer[len(APIConsumer) - 1]
    interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    ).transfer(api_contract, 1000000000000000000, {"from": dev})
    print("Funded {}".format(api_contract.address))

    api_contract.requestVolumeData({"from": dev})
    print("Reading data from {}".format(api_contract.address))
    if api_contract.volume() == 0:
        print("You may have to wait a minute and then call this again, unless on a local chain!")
        print("Waiting for a minute..")
        time.sleep(60)
    print(api_contract.volume())
