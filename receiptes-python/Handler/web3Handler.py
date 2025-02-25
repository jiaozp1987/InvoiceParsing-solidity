import json
from datetime import datetime

from eth_account import Account
from web3 import Web3


class we3Handler:
    def __init__(self):


        self.senderAddress = "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720"
        self.senderKey = 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6
        contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        self.chainID = 31337
        web3.eth.defaultAccount = Account.from_key(self.senderKey)
        abi = json.loads(
            '[{"type":"constructor","inputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"addInvoice","inputs":[{"name":"params","type":"string[11]","internalType":"string[11]"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"invoiceExisted","inputs":[{"name":"id","type":"string","internalType":"string"}],"outputs":[{"name":"invoiceResult","type":"tuple","internalType":"struct InvoiceLib.invoiceDomain","components":[{"name":"id","type":"string","internalType":"string"},{"name":"fileName","type":"string","internalType":"string"},{"name":"fromName","type":"string","internalType":"string"},{"name":"fromID","type":"string","internalType":"string"},{"name":"toName","type":"string","internalType":"string"},{"name":"toID","type":"string","internalType":"string"},{"name":"typeName","type":"string","internalType":"string"},{"name":"typeID","type":"string","internalType":"string"},{"name":"sumPrice","type":"string","internalType":"string"},{"name":"invoiceDate","type":"string","internalType":"string"},{"name":"createDate","type":"string","internalType":"string"},{"name":"isRepeat","type":"bool","internalType":"bool"}]}],"stateMutability":"view"},{"type":"function","name":"invoices","inputs":[{"name":"","type":"string","internalType":"string"}],"outputs":[{"name":"id","type":"string","internalType":"string"},{"name":"fileName","type":"string","internalType":"string"},{"name":"fromName","type":"string","internalType":"string"},{"name":"fromID","type":"string","internalType":"string"},{"name":"toName","type":"string","internalType":"string"},{"name":"toID","type":"string","internalType":"string"},{"name":"typeName","type":"string","internalType":"string"},{"name":"typeID","type":"string","internalType":"string"},{"name":"sumPrice","type":"string","internalType":"string"},{"name":"invoiceDate","type":"string","internalType":"string"},{"name":"createDate","type":"string","internalType":"string"},{"name":"isRepeat","type":"bool","internalType":"bool"}],"stateMutability":"view"}]')
        self.contract = web3.eth.contract(address=contractAddress, abi=abi)
        self.web3 = web3

    def invoiceExisted(self, id):
        invoice = self.contract.functions.invoiceExisted(id).call()
        return invoice

    def _tx(self, function):
        # 构建交易
        nonce = self.web3.eth.get_transaction_count(self.senderAddress)
        txn = function.build_transaction({
            'chainId': self.chainID,
            'gas': 300000,  # 根据合约方法的复杂性设置 Gas 限制
            'gasPrice': self.web3.to_wei('30', 'gwei'),  # 设置 Gas 价格
            'nonce': nonce,
        })

        # 签名交易
        signed_txn = self.web3.eth.account.sign_transaction(txn, self.senderKey)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt)
        return receipt

    def addInvoice(self, invoice):
        invoiceItem = list()
        invoiceItem.append(invoice.id)
        invoiceItem.append(invoice.fileName)
        invoiceItem.append(invoice.formName)
        invoiceItem.append(invoice.formID)
        invoiceItem.append(invoice.toName)
        invoiceItem.append(invoice.toID)
        invoiceItem.append(invoice.typeName)
        invoiceItem.append(invoice.typeID)
        invoiceItem.append(invoice.sumPrice)
        invoiceItem.append(invoice.invoiceDate)
        invoiceItem.append(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))


        # 调用合约方法
        function = self.contract.functions.addInvoice(invoiceItem)
        return self._tx(function)


