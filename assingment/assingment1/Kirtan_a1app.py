import Kirtan_a1
# if the source currency is not valid, quit
old=input('Enter original currency: ').upper()
new=input('Enter desired currency: ').upper()
amt=input('Enter original amount: ')
if(not(Kirtan_a1.is_currency(old))):
	print(old," is not a valid currency")
	quit()
# if the target currency is not valid, quit
if(not(Kirtan_a1.is_currency(new))):
	print(new," is not a valid currency")
	quit()

p=Kirtan_a1.exchange(old,new,amt) #Here we collecting the exchange value.
print(f'You can exchange {amt} {old} for {p} {new}.')