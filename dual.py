'''
   ////////////////////////////////////
///                                    ///
///Security of E-Based Systems Project ///
///                                    ///
///                                    ///
   ////////////////////////////////////
'''
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from base64 import b64decode,b64encode
import binascii
from orderinformation import OrderInformation as OI
from orderinformation import PaymentInformation as PI


'''Helper Functions'''
def bin2hex(binStr):
    return binascii.hexlify(binStr)

def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)


'''Class to create dual signature'''
class RequestMessage():

    '''Initialize everything'''
    def __init__(self,PI,OI):
        '''Calculating hash of payment information'''
        self.PI = PI
        HPI = SHA1.new(data=self.PI.encode())
        self.PIMD = HPI.hexdigest()

        '''Calculatig hash of order information'''
        self.OI = OI
        HOI = SHA1.new(data = self.OI.encode())
        self.OIMD = HOI.hexdigest()

        '''Calculate POMD and hashed POMD'''
        POMD = ""
        POMD += self.PIMD + self.OIMD
        self.POMD = POMD.encode()
        self.HPOMD = SHA1.new(data = self.POMD)
        self.HPOMD = self.HPOMD.hexdigest()

    '''Function to encrypt POMD us
    ing user's private key and generate DS'''
    def encryptPOMD(self):
        userKey = RSA.import_key(open("userprivate.pem").read(),passphrase = "passphrase-used-by-user")
        cipher_rsa = PKCS1_OAEP.new(userKey)
        data = self.POMD
        self.ds = cipher_rsa.encrypt(data)
        print("Computed dual signature:")
        self.ds = bin2hex(self.ds).decode()
        print(self.ds)
##        Encrypt signature in various forms:
##        Base64:
##        emsg64 = b64encode(self.ds)
##        print ("Secret message:",emsg64)
##        Hex:
##        emsghex = bin2hex(self.ds)    
##        print ("Secret message:",emsghex)

    '''Function to create the digital envelope'''
    def digitalEnvelope(self):
        file_out = open("digitalenvelope.bin","wb")
        '''Generate random session key'''
        session_key = get_random_bytes(16)
        cipher_aes = AES.new(session_key,AES.MODE_EAX)
        '''Data to send to bank'''
        data = self.PI + "\n"
        data += "----Dual Signature----\n" + self.ds + "\n"
        data += "----OIMD----\n" + self.OIMD
        data = data.encode()

        print(data)
        ciphertext,tag = cipher_aes.encrypt_and_digest(data)
        bankKey = RSA.import_key(open("bankpublic.pem").read())
        cipher_rsa = PKCS1_OAEP.new(bankKey)
        print("\n\nCiphertext in digital envelope:\n",bin2hex(ciphertext).decode())
        '''Encrypt session key using bank's public key'''
        encrypted_session_key = cipher_rsa.encrypt(session_key)
        [ file_out.write(x) for x in (encrypted_session_key, cipher_aes.nonce, tag, ciphertext) ]
        print("Digital envelope created")

    '''Function to create request document'''
    def completeRequest(self):
        file_out = open("requestmessage.txt","w")
        '''Data to send to merchant'''
        data = self.OI + "\n"
        data += "----Dual Signature---\n" + self.ds + "\n"
        data += "----PIMD----\n" + self.PIMD
        [ file_out.write(x) for x in (data)]

'''Function used by bank to read the contents of the file'''
def verifyBank():
    file_in = open("digitalenvelope.bin", "rb")
    private_key = RSA.import_key(open("bankprivate.pem").read(),passphrase = "passphrase-used-by-bank")

    enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    '''Decrypt the session key with the private RSA key'''
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    '''Decrypt the data with the AES session key'''
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print("\n\nData recieved by bank:")
    print(data.decode("utf-8"))

'''Function used by merchant to read the contents of the file'''
def verifyMerchant() :
    file_in = open("requestmessage.txt","r")
    data = file_in.read()
    print("\n\nData recieved by merchant:")
    print(data)


def main():
    items = ["Apples","Oranges","Mangoes","Grapes","Guavas"]
    prices = [80,50,150,40,30]
    ch = -1
    order = OI()
    payment = PI()
    while(ch!=4):
        print("Choose an operation:\n1.Add item\n2.Remove item\n3.Display Order\n4.Proceed to pay")
        ch = int(input())
        if (ch == 1):
            print("\t\t\t\t----Available items----")
            print("Id\t\tProduct\t\tPrice")
            for i in range(len(items)):
                print(i+1,"\t\t",items[i],"\t\t",prices[i])
            ch2 = input("Enter item name to add:")
            found = False
            for i in range(len(items)):
                if ch2 == items[i]:
                    order.addItem(items[i],prices[i])
                    found = True
            if not found:
                print("No item with that name available")
        elif (ch == 2):
            order.display()
            ch2 = input("Enter item name to remove:")
            order.removeItem(ch2)
        elif (ch == 3):
            order.display()
        elif (ch != 4):
            print("Invalid option.Try again")
    order.display()
    ch3 = "no"
    while (ch3 != "yes"):
        cardNo = input("Enter your card number:")
        expiry = input("Enter expiry date in MM/YY format:")
        cvv = input("Enter your cvv:")
        payment.cardDetails(cardNo,expiry,cvv)
        payment.setPay(order.getTotal())
        payment.display()
        ch3 = input("Are your details correct?(yes/no)")
        print(ch3)

    print("\n\nGenerating dual signature")
    orderMsg = order.generateText()
    paymentMsg = payment.generateText()
    a = RequestMessage(paymentMsg,orderMsg)
    a.encryptPOMD()
    a.digitalEnvelope()
    a.completeRequest()
    verifyBank()
    verifyMerchant()
main()
