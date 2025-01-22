from tkinter import *
import tkinter.messagebox
import requests
import csv

# Current coins used in convertor
headers = ['Currency','Price','Quantity','Cost(USD)','Exchange Rate USD:COIN']
coins = {'BTC':0,'ETH':0,'BNB':0,'XRP':0}
prices = {}

def convert():
    '''
    Inputs number of cryptocurrency needed to convert to USD
    '''
    if update_quantities():
        try:
            url = "http://api.coinlayer.com/live?access_key=e1e2ea064e285028a03b3e6e53b3318f"
            response = requests.get(url)
            response.raise_for_status()
            rates = response.json()['rates']
            prices = {}
            for coin, quantity in coins.items():
                if quantity > 0:
                    prices[coin] = rates[coin]
            write_to_csv(prices)
        except requests.exceptions.RequestException as e:
            tkinter.messagebox.showerror("Error", f"API request failed: {e}")
        except KeyError as e:
            tkinter.messagebox.showerror("Error", f"Currency not found in API response: {e}")
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def close():
    '''
    Closes the program if it is selected
    '''
    window.quit()

def update_quantities():
    '''
    Will update quantities and show an error message if needed
    '''
    try:
        coins['BTC'] = int(btcentry.get()) if btcentry.get().strip() else 0
        coins['ETH'] = int(ethentry.get()) if ethentry.get().strip() else 0
        coins['BNB'] = int(bnbentry.get()) if bnbentry.get().strip() else 0
        coins['XRP'] = int(xrpentry.get()) if xrpentry.get().strip() else 0
        return True
    except ValueError:
        tkinter.messagebox.showerror("Error","Sorry, the report could not be written. Check that only numeric values are entered.")
        return False

def write_to_csv(prices):
    '''
    Writes data to CSV file, this took forever
    '''
    total = 0
    with open('crypto_conversion.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for coin,value in prices.items():
            writer.writerow([coin,value,coins[coin],value*coins[coin],float(1/value)])
            total += value*coins[coin]
        writer.writerow(['--']*len(headers))
        writer.writerow(['Total','--','--',total,'--'])
    tkinter.messagebox.showinfo("Complete","The conversions were stored in crypto_conversion.csv")

# Window size and stuff
window = Tk()
window.title("Exchange Rate Calculator")
mainframe = Frame(window)
mainframe.pack(fill="both", expand=True)

# Code for BTC and ETH stuff on top row
toprow=Frame(mainframe,bg="bisque",padx=5,pady=5)
toprow.pack(fill="both", expand=True)
btclabel= Label(toprow,text="BTC:",bg='bisque')
btclabel.pack(side=LEFT)
btcentry=Entry(toprow)
btcentry.pack(side=LEFT)
ethlabel= Label(toprow,text="ETH:",bg='bisque')
ethlabel.pack(side=LEFT)
ethentry=Entry(toprow)
ethentry.pack(side=LEFT)
convertbutton = Button(toprow,text="Convert Currency", command=convert, bg="#98FB98",width=15,padx=5,pady=5)
convertbutton.pack(padx= 5, side=LEFT)

# Code for BNB and XRP stuff on bottom)
bottomrow=Frame(mainframe,bg="bisque",padx=5,pady=5)
bottomrow.pack(fill="both", expand=True)
bnblabel= Label(bottomrow,text="BNB:",bg='bisque')
bnblabel.pack(side=LEFT)
bnbentry=Entry(bottomrow)
bnbentry.pack(side=LEFT)
xrplabel= Label(bottomrow,text="XRP:",bg='bisque')
xrplabel.pack(side=LEFT)
xrpentry=Entry(bottomrow)
xrpentry.pack(side=LEFT)
closebutton = Button(bottomrow,text="Close Converter", command=close, bg="dark orange",width=15,padx=5,pady=5)
closebutton.pack(padx= 5, side=LEFT)
window.mainloop()