class OrderInformation():
    def __init__(self):
        self.itemList = []
        self.priceList = []
        self.totalPrice = 0

    def calcPrice(self):
        totalPrice = 0
        for price in self.priceList:
            totalPrice += price
        self.totalPrice = totalPrice

    def addItem(self,item,price):
        self.itemList.append(item)
        print("One item added to list")
        self.priceList.append(price)
        self.calcPrice()

    def searchItem(self,item):
        for i in range(len(self.itemList)):
            if (self.itemList[i] == item):
                return i
        return -1

    def removeItem(self,item):
        index = self.searchItem(item)
        if (index != -1):
            del self.itemList[index]
            print("Removed item:",item)
            del self.priceList[index]
            self.calcPrice()
        else :
            print("Item not found")

    def getTotal(self):
        return self.totalPrice

    def display(self):
        print("\nYour order is:")
        print("Item\t\tPrice")
        for i in range(len(self.itemList)):
            print(self.itemList[i],"        ",self.priceList[i])
        print("\t\tTotal amount:",self.totalPrice)

    def generateText(self):
        msg = "----Order Information----\nItems:\n"
        for item in self.itemList:
            msg += item + "\n"
        return msg
        
class PaymentInformation():
    def __init__(self):
        self.cardNumber = ""
        self.cvv = ""
        self.expiry = ""
        self.pay = 0

    def cardDetails(self,cardNumber,expiry,cvv):
        self.cardNumber = cardNumber
        self.expiry = expiry
        self.cvv = cvv

    def setPay(self,amount):
        self.pay = amount

    def display(self):
        print("Your card details are:")
        print("CardNumber:",self.cardNumber)
        print("Expiry:",self.expiry)
        print("Cvv:",self.cvv)
        print("Amount:",self.pay)

    def generateText(self):
        msg = "----Payment Information----\nCard Number:" + self.cardNumber + "\nExpiry Date:" + self.expiry + "\nCvv Number:" + self.cvv + "\nPayment Amount:" + str(self.pay)
        return msg

