#__author__  = Richard Whyte
#__version__ = 1.7
#__email__   = Richard.whyte@elev.ga.ntig.se

# IcaMaxi.PY: A database that should mimic a Swedish store brand ICA

import pygame
import sys
import csv
import locale
import os

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (1000, 800)  # Creates a window with the pixel size
window = pygame.display.set_mode(window_size)  # Sets the window size
pygame.display.set_caption('Product List')  # What the tab is called

# Set up fonts
header_font = pygame.font.SysFont('arial', 28, bold=True)  # Sets up fonts through system in pygame
font = pygame.font.SysFont('arial', 20)  #  font for layout
button_font = pygame.font.SysFont('arial', 30, bold=True)  #  button font for layout

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  # Sets the currency and time to Sweden

# Load the front page image
script_dir = os.path.dirname(__file__)  # Get the directory of the script
front_page_image_path = os.path.join(script_dir, 'ICA B.jpg')  # Create a path to the image file
front_page_image = pygame.image.load(front_page_image_path)
front_page_image = pygame.transform.scale(front_page_image, window_size)  # Makes the images "fit" to the window size

# Load data from CSV file
def load_data(filename):
    """Load products from a CSV file."""
    products = []
    try:
        with open(filename, 'r', encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = {
                    "id": int(row['id']),
                    "name": row['name'],
                    "desc": row['desc'],
                    "price": row['price'],  # Store price as string
                    "quantity": row['quantity']  # Store quantity as string
                }
                products.append(product)
    except Exception as error:
        print(error)  # If something bad happens it will type out error
    return products

# Function to save products to a CSV file
def save_data(filepath, products):
    """Save products to a CSV file."""
    try:
        with open(filepath, mode='w', newline='', encoding="UTF-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
            writer.writeheader()
            writer.writerows(products)
        print(f"Data successfully saved to {filepath}")
    except Exception as error:
        print(f"Error saving data: {error}")

# Load product data from CSV file
products = load_data('Ica_data.csv')

# Colours
black = (0, 0, 0)  # Hex code
dark_gray = (50, 50, 50)
white = (255, 255, 255)

# Button setup
button_rect = pygame.Rect((window_size[0] // 2 - 100, window_size[1] // 2 - 50, 200, 100))  # Location of the buttons on the window its set up on
button_add = pygame.Rect((window_size[0] // 2 - 250, window_size[1] - 100, 120, 60))
button_remove = pygame.Rect((window_size[0] // 2 - 50, window_size[1] - 100, 120, 60))
button_change = pygame.Rect((window_size[0] // 2 + 150, window_size[1] - 100, 120, 60))

# Function to create the front page
def render_front_page():
    window.blit(front_page_image, (0, 0))  # Sets the image to the cords 0,0
    pygame.draw.rect(window, dark_gray, button_rect)  # Background will be dark gray with button
    button_text = button_font.render("GO", True, white)  # The button will be named GO and will be white
    text_rect = button_text.get_rect(center=button_rect.center)  # Button gets reacted
    window.blit(button_text, text_rect)
    pygame.display.flip()

# Function to create the product list
def render_product_list():
    window.fill((155, 161, 157))

    # Create and name buttons
    pygame.draw.rect(window, dark_gray, button_add)
    button_text = button_font.render("Add", True, white)
    text_rect = button_text.get_rect(center=button_add.center)
    window.blit(button_text, text_rect)

    pygame.draw.rect(window, dark_gray, button_remove)
    button_text = button_font.render("Remove", True, white)
    text_rect = button_text.get_rect(center=button_remove.center)
    window.blit(button_text, text_rect)

    pygame.draw.rect(window, dark_gray, button_change)
    button_text = button_font.render("Change", True, white)
    text_rect = button_text.get_rect(center=button_change.center)
    window.blit(button_text, text_rect)

    # Create product list with headers
    headers = ["ID", "Name", "Description", "Price", "Quantity"]
    header_x_positions = [20, 100, 250, 650, 800]
    for i, header in enumerate(headers):
        header_surface = header_font.render(header, True, dark_gray)
        window.blit(header_surface, (header_x_positions[i], 20))
    pygame.draw.line(window, black, (20, 60), (980, 60), 2)
    
    y = 70
    row_spacing = 30  # Reduced row spacing for a more compact view
    for product in products:
        product_details = [
            str(product['id']),
            product['name'],
            product['desc'],
            product['price'],
            product['quantity']
        ]
        for i, detail in enumerate(product_details):
            detail_surface = font.render(detail, True, black)
            window.blit(detail_surface, (header_x_positions[i], y))
        y += row_spacing  # Move to the next row with reduced spacing
    pygame.display.flip()

# Function to add a product
def add_product():
    name = input("Enter product name: ")
    desc = input("Enter product description: ")
    price = input("Enter product price: ")  # Store price as string
    quantity = input("Enter product quantity: ")  # Store quantity as string

    new_id = max(product['id'] for product in products) + 1 if products else 1
    new_product = {
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    }
    products.append(new_product)
    save_data('Ica_data.csv', products)
    print(f"Product {name} added successfully.")

# Function to remove a product
def remove_product():
    id_input = input("Enter product ID to remove: ")
    try:
        id = int(id_input)
    except ValueError:
        print("Invalid input. Please enter a numeric value for the product ID.")
        return

    for product in products:
        if product["id"] == id:
            products.remove(product)
            save_data('Ica_data.csv', products)
            print(f"Product: {id} {product['name']} was removed")
            return
    print(f"Product with id {id} not found")

# Function to change a product
def change_product():
    id_input = input("Enter product ID to change: ")
    try:
        id = int(id_input)
    except ValueError:
        print("Invalid input. Please enter a numeric value for the product ID.")
        return

    for product in products:
        if product["id"] == id:
            product['name'] = input("Enter new name: ")
            product['desc'] = input("Enter new description: ")
            product['price'] = input("Enter new price: ")  # Store new price as string
            product['quantity'] = input("Enter new quantity: ")  # Store new quantity as string
            save_data('Ica_data.csv', products)
            print(f"Product with id: {product['id']} was changed")
            return
    print(f"Product with id {id} not found")

# Main loop
on_front_page = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if on_front_page and button_rect.collidepoint(event.pos):
                on_front_page = False
            elif not on_front_page and button_add.collidepoint(event.pos):
                print("Add product button clicked")
                add_product()
            elif not on_front_page and button_remove.collidepoint(event.pos):
                print("Remove product button clicked")
                remove_product()
            elif not on_front_page and button_change.collidepoint(event.pos):
                print("Change product button clicked")
                change_product()

    if on_front_page:
        render_front_page()
    else:
        render_product_list()

pygame.quit()
sys.exit()
