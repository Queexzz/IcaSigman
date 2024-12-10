import pygame
import sys
import csv
import os
import locale

#__author__  = Richard whyte
#__version__ = 1.4
#__email__   = Richard.whyte@elev.ga.ntig.se

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (1000, 800) #Creates a window with the pixel size
window = pygame.display.set_mode(window_size) #sets the window size
pygame.display.set_caption('Product List') #What the tab is called

# Set up fonts
header_font = pygame.font.SysFont('arial', 28, bold=True) #sets up fonts trough system in the pygame
font = pygame.font.SysFont('arial', 24) 
button_font = pygame.font.SysFont('arial', 40, bold=True)

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8') #sets the currency and time to sweden

# Load the front page image
front_page_image = pygame.image.load("C:\\Users\\Richard.whyte\\Documents\\ICA B.jpg")
front_page_image = pygame.transform.scale(front_page_image, window_size) #Makes the images "fit" to the window size

# Load data from csv file
def load_data(filename):
    """Load products from a CSV file."""
    products = []
    try: #error handeling
        with open(filename, 'r', encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = {
                    "id": int(row['id']),
                    "name": row['name'],
                    "desc": row['desc'],
                    "price": float(row['price']),
                    "quantity": int(row['quantity'])
                }
                products.append(product)
    except Exception as error:
        print(error) #if something bad happens it will type out error
    return products

# Function to save products to a CSV file
def save_data(filepath, products):
    """Save products to a CSV file."""
    with open(filepath, mode='w', newline='', encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)
    print(f"Data successfully saved to {filepath}")

# Load product data from CSV file
products = load_data('Ica_data.csv')

# Colours
black = (0, 0, 0) #hex code
dark_gray = (50, 50, 50)
white = (255, 255, 255)

# Button setup
button_rect = pygame.Rect((window_size[0] // 2 - 100, window_size[1] // 2 - 50, 200, 100)) #location of the buttons on the window its set up on
button_add = pygame.Rect((window_size[0] // 2 - 10, window_size[1] - 150, 150, 100))
button_remove = pygame.Rect((window_size[0] // 2 - 350, window_size[1] - 150, 200, 100))
button_change = pygame.Rect((window_size[0] // 2 - 150, window_size[1] - 150, 150, 100))

# Function to create the front page
def render_front_page():
    window.blit(front_page_image, (0, 0)) #sets the image to the cords 0,0
    pygame.draw.rect(window, dark_gray, button_rect) #Background will be dark gray with button
    button_text = button_font.render("GO", True, white) #The button will be named GO and will be white
    text_rect = button_text.get_rect(center=button_rect.center) #Button gets reacted
    window.blit(button_text, text_rect) 
    pygame.display.flip()

# Function to create the product list
def render_product_list():
    window.fill((155, 161, 157))
    
    # Create and name button
    pygame.draw.rect(window, dark_gray, button_add)
    button_text = button_font.render("Add", True, white)
    text_rect = button_text.get_rect(center=button_add.center)
    window.blit(button_text, text_rect) #Button for a white "Add"

    pygame.draw.rect(window, dark_gray, button_remove)
    button_text = button_font.render("Remove", True, white)
    text_rect = button_text.get_rect(center=button_remove.center)
    window.blit(button_text, text_rect) #Button for a white "Remove"

    pygame.draw.rect(window, dark_gray, button_change)
    button_text = button_font.render("Change", True, white)
    text_rect = button_text.get_rect(center=button_change.center)
    window.blit(button_text, text_rect) #Button for a white "Change"

    # Create product list
    headers = [" Name", "Description", "Price (SEK)", "Quantity"] #Sets up the names
    header_x_positions = [20, 220, 650, 800] #Postion
    for i, header in enumerate(headers): #calculate the headers
        header_surface = header_font.render(header, True, dark_gray) #render it in gray
        window.blit(header_surface, (header_x_positions[i], 20)) #Positon it to 20
    pygame.draw.line(window, black, (20, 60), (980, 60), 2) #draw a black window at the cords
    y = 80
    #Clacualtes how many, what they are called, their desc, price and quantity then renders them out
    for product in products: 
        product_details = [
            product['name'],
            product['desc'],
            f"{product['price']:.2f}",
            f"{product['quantity']}"
        ]
        for i, detail in enumerate(product_details):
            detail_surface = font.render(detail, True, black)
            window.blit(detail_surface, (header_x_positions[i], y))
        y += 30
    pygame.display.flip()

# Function to add a product
def add_product():
    input_text = "" #text is added
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() #If you don't type it ends the programe
            if event.type == pygame.KEYDOWN: #if a key is pressed:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    name = input_text
                    desc = input("Enter product description: ") #Write a new description
                    price = float(input("Enter product price: ")) #New price
                    quantity = int(input("Enter product quantity: ")) #Quanitity
                    new_id = max(product['id'] for product in products) + 1 if products else 1 #Gives it a new ID
                    new_product = {
                        "id": new_id,
                        "name": name,
                        "desc": desc,
                        "price": price,
                        "quantity": quantity
                    } #Tells the product what is needed for it to be consireded a product and then saves it to Ica_data
                    products.append(new_product)
                    save_data('Ica_data.csv', products)
                    return
                else:
                    input_text += event.unicode
        window.fill((155, 161, 157))
        input_surface = font.render(input_text, True, black)
        window.blit(input_surface, (20, 100))
        pygame.display.flip()

# Function to remove a product
def remove_product():
    id = int(input("Enter product ID to remove: ")) #ID gets collected trough the ID in the CSV file
    for product in products: #For every product in the list do:
        if product["id"] == id: #If the ID exist do:
            products.remove(product) #Removes the product
            save_data('Ica_data.csv', products) #Saves the file
            return f"Product: {id} {product['name']} was removed"
    return f"Product with id {id} not found" #Returns the function with a text saying it worked

# Function to change a product
def change_product(): 
    id = int(input("Enter product ID to change: ")) #ID gets collected through the ID in the CSV file
    for product in products:
        if product["id"] == id: #If the product has an ID it will:
            product['name'] = input("Enter new name: ") #Ask you for a name
            product['desc'] = input("Enter new description: ") #Descrption of the product
            product['price'] = float(input("Enter new price: ")) # price for the product (Float is used becuase of decimals)
            product['quantity'] = int(input("Enter new quantity: ")) #How many things there are
            save_data('Ica_data.csv', products) #saves the newly created csv file into the old one
            return f"Product with id:{product['id']} was changed" #Returns the function so it's repeated
    return f"Product with id {id} not found"

# Main loop
on_front_page = True #If the front page is open it will continue the code under
running = True
while running: #When the code is run it will go trough this and loop until it's done
    for event in pygame.event.get(): #If the follwing corrisponds to something (==) it will go to the if/elif.
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if on_front_page and button_rect.collidepoint(event.pos):
                on_front_page = False #Closes the front page with the click of a button
            elif not on_front_page and button_add.collidepoint(event.pos):
                add_product() # If the front page is not active it will call uppon the "add_products() function"
            elif not on_front_page and button_remove.collidepoint(event.pos):
                remove_product() #If the front page is not active it will call uppon the "remove_products() function"
            elif not on_front_page and button_change.collidepoint(event.pos):
                change_product() #If the front page is not active it will call uppon the "change_products() function"

    if on_front_page:
        render_front_page() #If you are on the front page it will call the function to render it
    else:
        render_product_list() #otherwise call upon the render_product_list function

pygame.quit() # Closes pygame
sys.exit() #Closes system