#!/usr/bin/env python3
from trezorlib.client import TrezorClient
from trezorlib.transport import get_transport
from trezorlib.tools import parse_path
from binascii import hexlify
import requests

def main():
    # Use first connected device
    transport = get_transport()

    # Creates object for manipulating TREZOR
    client = TrezorClient(transport)

    # Print out TREZOR's features and settings
    print(client.features)

    # Get the first address of first BIP44 account
    # (should be the same address as shown in wallet.trezor.io)
    bip32_path = parse_path("44'/0'/0'/0/0")
    #address = client.apla_get_wallet([], False)
    #print('Apla address:', hexlify(address))
    public_key = client.apla_get_public_key([], True)
    print('Apla public key:', hexlify(bytearray(public_key)))
    
    signed_message = client.apla_sign_message(bip32_path, 
        "message to sign",
        "note",
         True
    )
    print("Apla signed message", signed_message.signature.hex())
    #exit(0)
    
    
    
    host = "testapla0.apla.io"
    httpPort = "7079"
    baseUrl = "https://" + host + ":" + httpPort + "/api/v2"
    respUid = requests.get(baseUrl + '/getuid')
    resultGetuid = respUid.json()
    print(resultGetuid)
    print("-------------------------------\n")
        
   
    signature_res = client.apla_sign_message(bip32_path, "LOGIN" + resultGetuid['uid'], "Are you sure you want to login?", True)
    pub_key = hexlify(bytearray(signature_res.public_key[1:]))
    signature = signature_res.signature.hex()
    print(signature)

    print("requesting /loging ...")
    fullToken = 'Bearer ' + resultGetuid['token']
    respLogin = requests.post(baseUrl +'/login', params={'pubkey': pub_key, 'signature': signature}, headers={'Authorization': fullToken})
    resultLogin = respLogin.json()
    print(resultLogin)
    print("-------------------------------\n")

    address = resultLogin["address"]
    jwtToken = 'Bearer ' + resultLogin["token"]
    token = resultLogin["token"]
    

    #signed_message = client.apla_sign_message(bip32_path, "Here is the message")
    #print("Apla signed message", hexlify(bytearray(signed_message.public_key)))
    #entropy = client.get_entropy(1)
    #print('Apla address:', entropy)

    #address = client.ethereum_get_address([], True)
    #print('Ethereum address:', hexlify(address))

    client.close()


if __name__ == '__main__':
    main()