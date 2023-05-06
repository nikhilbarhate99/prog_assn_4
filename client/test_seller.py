from client.seller_client import SellerClient
import os

def print_response(response):
    for k, v in response.items():
        print(k, ':', v)


client = SellerClient()


print("=" * 60)
print('Which function do you want to call?')
print('1. Create Account')
print('2. Login')
print('3. Add item')
print("4. remove item")
print("5. change price")
print("6. get all items by seller")
print("7. get seller rating")
print("8. logout")
print("q for quit")
print("=" * 60)


while True:

    choice = input('Enter command: ')
    
    if choice == 'q':
        break
    
    elif choice == '1':
        username = input('Enter username: ')
        password = input('Enter password: ')
        name = input('Enter name: ')
        response=(client.create_account(username, password, name))
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)
    
    elif choice == '2':
        username = input('Enter username: ')
        password = input('Enter password: ')
        response=client.login(username, password)
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)

    
    elif choice == '3':
        username = input('Enter username: ')
        name = input('Enter product name: ')
        category=int(input('Enter product category: '))
        condition=input('Enter product condition: ')
        price=int(input('Enter product price: '))
        keyword1=input('Enter product keyword1: ')
        keyword2=input('Enter product keyword2: ')
        keyword3=input('Enter product keyword3: ')

        item = {"name": name, 

                "category" : category, 

                "condition" : condition, 

                "keywords" : (keyword1,keyword2,keyword3), 

                "price" : price

                }
        
        quantity = int(input('Enter quantity: '))
        response=client.add_item(username, item, quantity)
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)
    

    elif choice == '4':
        username = input('Enter username: ')
        prod_id = int(input('Enter prod_id: '))
        quantity = int(input('Enter quantity to remove: '))
        
        response=(client.remove_item(prod_id, quantity, username))
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '5':
        username = input('Enter username: ')
        prod_id = int(input('Enter prod_id: '))
        new_price = int(input('Enter new_price: '))
        response=(client.change_price( prod_id, new_price, username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    
    elif choice == '6':
        username = input('Enter username: ')
        
        response=(client.all_items_by_seller(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    
    elif choice == '8':
        username = input('Enter username: ')
        
        response=(client.logout(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)


    elif choice == '7':
        username = input('Enter seller username: ')
        
        response=(client.get_seller_rating(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    
    else:
        
        print('Invalid choice. Please try again.')