#EZCoin
import time
import Wallet
import threading
import Miner
import Signatures
import TxBlock

wallets=[]
miners=[]
my_ip = 'localhost'
wallets.append((my_ip,5006))
miners.append((my_ip,5005))

tMS = None
tNF = None
tWS = None


def startMiner():
    global tMS, tNF
    try:
        my_pu = Signatures.loadPublic("public.key")
    except:
        pass #TODO
    tMS = threading.Thread(target=Miner.minerServer, args=((my_ip,5005),))
    tNF = threading.Thread(target=Miner.nonceFinder, args=(wallets, my_pu))
    tMS.start()
    tNF.start()
    return True
def startWallet():
    global tWS
    tWS = threading.Thread(target=Wallet.walletServer, args=((my_ip,5006),))
    tWS.start()
    Wallet.my_private, Wallet.my_public = Signatures.loadKeys("private.key","public.key")
    return True

def stopMiner():
    global tMS, tNF
    Miner.StopAll()
    time.sleep(2)
    if tMS: tMS.join()
    if tNF: tNF.join()
    return True
def stopWallet():
    global tWS
    Wallet.StopAll()
    time.sleep(2)
    if tWS: tWS.join()
    return True

def getBalance(pu_key):
    if not tWS:
        print("Can't get balance. Please start walletServer first.")
        return 0.0
    return Wallet.getBalance(pu_key)

def sendCoins(pu_recv, amt, tx_fee):
    Wallet.sendCoins(Wallet.my_public, amt+tx_fee, Wallet.my_private,
                     pu_recv, amt)
    return True

def makeNewKeys():
    Wallet.my_private, Wallet.my_public = Signatures.generate_keys()
    Signatures.savePublic(Wallet.my_public, "public.key")
    Signatures.savePrivate(Wallet.my_private, "private.key")
    return None






if __name__ == "__main__":
    startMiner()
    startWallet()
    other_public = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtgVDX501+HzGJxusVfOJ\n8V7VXUlCs1sDgIXxq2uc38fC3fO8GmYMVVeMZ34KAZ3HMBKwMKVbN1tIPVNBz22m\n54tP+3RS8xN2lDNByiSKIFsmtDMO7JpP/hl13Lj+IiVs3bI0n1uShlOIJ8QozEud\nlwkMz39xfrvX0NN6MYl/OibIkPW6cle8hwKWE6kxiUz4nLDB4i9YuRcjWsSSW/a/\n9oU4TZWk128O4BWnqru8XNyz2km4vsq5k07WCVSCqlpyF26v85sWqDTGCHXIeZre\nEKuKiZpgAVCjgHAbYkin1BGWRVXohPnEZECrZqoTjVVEl5wAdGXntjrsWIXaumG5\nhQIDAQAB\n-----END PUBLIC KEY-----\n'
    time.sleep(2)
    print(getBalance(Wallet.my_public))
    sendCoins( other_public, 1.0, 0.001 )
    time.sleep(20)
    print(getBalance(other_public))
    print(getBalance(Wallet.my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()

    print(ord(TxBlock.findLongestBlockchain(Miner.head_blocks).previousBlock.previousBlock.nonce[0]))
    print(ord(TxBlock.findLongestBlockchain(Miner.head_blocks).previousBlock.nonce[0]))
    print(ord(TxBlock.findLongestBlockchain(Miner.head_blocks).nonce[0]))
    
    
    
