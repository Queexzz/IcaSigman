import pygame
import sys
import csv
import os
import locale

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (1000, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Product List')

# Set up fonts
header_font = pygame.font.SysFont('arial', 28, bold=True)
font = pygame.font.SysFont('arial', 24)
button_font = pygame.font.SysFont('arial', 40, bold=True)

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

# Load the front page image
front_page_image = pygame.image.load("C:\\Users\\Richard.whyte\\Documents\\ICA B.jpg")
front_page_image = pygame.transform.scale(front_page_image, window_size)

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
                    "price": float(row['price']),
                    "quantity": int(row['quantity'])
                }
                products.append(product)
    except Exception as error:
        print(error)
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

# Colors
black = (0, 0, 0)
dark_gray = (50, 50, 50)
white = (255, 255, 255)

# Button setup
button_rect = pygame.Rect((window_size[0] // 2 - 100, window_size[1] // 2 - 50, 200, 100))
button_add = pygame.Rect((window_size[0] // 2 - 10, window_size[1] - 150, 150, 100))
button_remove = pygame.Rect((window_size[0] // 2 - 350, window_size[1] - 150, 200, 100))
button_change = pygame.Rect((window_size[0] // 2 - 150, window_size[1] - 150, 150, 100))

# Function to create the front page
def render_front_page():
    window.blit(front_page_image, (0, 0))
    pygame.draw.rect(window, dark_gray, button_rect)
    button_text = button_font.render("GO", True, white)
    text_rect = button_text.get_rect(center=button_rect.center)
    window.blit(button_text, text_rect)
    pygame.display.flip()

# Function to create the product list
def render_product_list():
    window.fill((155, 161, 157))
    
    # Create and name button
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

    # Create product list
    headers = [" Name", "Description", "Price (SEK)", "Quantity"]
    header_x_positions = [20, 220, 650, 800]
    for i, header in enumerate(headers):
        header_surface = header_font.render(header, True, dark_gray)
        window.blit(header_surface, (header_x_positions[i], 20))
    pygame.draw.line(window, black, (20, 60), (980, 60), 2)
    y = 80
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
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    name = input_text
                    desc = input("Enter product description: ")
                    price = float(input("Enter product price: "))
                    quantity = int(input("Enter product quantity: "))
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
                    return
                else:
                    input_text += event.unicode
        window.fill((155, 161, 157))
        input_surface = font.render(input_text, True, black)
        window.blit(input_surface, (20, 100))
        pygame.display.flip()

# Function to remove a product
def remove_product():
    id = int(input("Enter product ID to remove: "))
    for product in products:
        if product["id"] == id:
            products.remove(product)
            save_data('Ica_data.csv', products)
            return f"Product: {id} {product['name']} was removed"
    return f"Product with id {id} not found"

# Function to change a product
def change_product():
    id = int(input("Enter product ID to change: "))
    for product in products:
        if product["id"] == id:
            product['name'] = input("Enter new name: ")
            product['desc'] = input("Enter new description: ")
            product['price'] = float(input("Enter new price: "))
            product['quantity'] = int(input("Enter new quantity: "))
            save_data('Ica_data.csv', products)
            return f"Product with id:{product['id']} was changed"
    return f"Product with id {id} not found"

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
                add_product()
            elif not on_front_page and button_remove.collidepoint(event.pos):
                remove_product()
            elif not on_front_page and button_change.collidepoint(event.pos):
                change_product()

    if on_front_page:
        render_front_page()
    else:
        render_product_list()

pygame.quit()
sys.exit()