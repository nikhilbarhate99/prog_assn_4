from buyer_client import BuyerClient
import os


def print_response(response):
    for k, v in response.items():
        print(k, ':', v)


client = BuyerClient()

print("=" * 60)
print('1. Create Account')
print('2. Login')
print('3. Add to Cart')
print("4. display cart")
print("5. clear cart")
print("6. remove cart")
print("7. search items")
print("8. get purchase history")
print("9. make purchase")
print("10. get seller rating")
print("11. logout")
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
        prod_id = int(input('Enter product ID: '))
        quantity = int(input('Enter quantity: '))
        response=client.add_to_cart(username, prod_id, quantity)
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)
    
    elif choice == '4':
        username = input('Enter username: ')
        
        response=(client.display_cart(username))
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)


    elif choice == '5':
        username = input('Enter username: ')
        
        response=(client.clear_cart(username))
        
        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '6':
        username = input('Enter username: ')
        prod_id = int(input('Enter prod_id: '))
        quantity = int(input('Enter quantity: '))
        response=(client.remove_cart(username, prod_id, quantity))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '7':
        username = input('Enter username: ')
        category = int(input('Enter category: '))
        keyword1 = input('Enter keyword 1: ')
        keyword2 = input('Enter keyword 2: ')
        keyword3 = input('Enter keyword 3: ')
        keywords=[keyword1,keyword2,keyword3]

        response=(client.search_items(category,keywords,username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '8':
        username = input('Enter username: ')
        
        response=(client.get_purchase_history(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '9':
        username = input('Enter username: ')
        creditcard = input('Enter creditcard number: ')
        
        response=(client.make_purchase(username, creditcard))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    elif choice == '11':
        username = input('Enter username: ')
        
        response=(client.logout(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)


    elif choice == '10':
        username = input('Enter seller username: ')
        
        response=(client.get_seller_rating(username))
        

        print("=" * 60)
        print_response(response)
        print("=" * 60)

    
    else:
        
        print('Invalid choice. Please try again.')