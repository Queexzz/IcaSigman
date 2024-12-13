import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (1000, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Product List')

# Set up fonts
header_font = pygame.font.SysFont('Courier New', 28, bold=True)
font = pygame.font.SysFont('Courier New', 24)
button_font = pygame.font.SysFont('Courier New', 40, bold=True)

# Load images
front_page_image = pygame.image.load("C:\\Users\\Richard.whyte\\Documents\\ICA B.jpg")
front_page_image = pygame.transform.scale(front_page_image, window_size)  # Scale the image to fit the window

# Product data
products = [
    {"id": 1, "name": "Mjölk 1L", "desc": "Färsk mjölk från lokala gårdar.", "price": 20.00, "quantity": 200},
    {"id": 2, "name": "Bröd", "desc": "Färskt bröd bakat dagligen.", "price": 25.00, "quantity": 150},
    {"id": 3, "name": "Ägg 12-pack", "desc": "Ekologiska ägg från frigående höns.", "price": 40.00, "quantity": 120},
    {"id": 4, "name": "Smör 500g", "desc": "Kvalitetssmör för matlagning och bakning.", "price": 50.00, "quantity": 100},
    {"id": 5, "name": "Apelsiner 1kg", "desc": "Färska apelsiner, perfekt för juicing.", "price": 35.00, "quantity": 80},
    {"id": 6, "name": "Bananer 1kg", "desc": "Ekologiska bananer, rika på kalium.", "price": 30.00, "quantity": 150},
    {"id": 7, "name": "Kaffe 500g", "desc": "Mörkrostat kaffe med rik smak.", "price": 60.00, "quantity": 90},
    {"id": 8, "name": "Tandkräm", "desc": "Fluorid tandkräm för starka tänder.", "price": 30.00, "quantity": 200},
    {"id": 9, "name": "Tvättmedel 1kg", "desc": "Effektivt tvättmedel för alla typer av tvätt.", "price": 70.00, "quantity": 70},
    {"id": 10, "name": "Schampo", "desc": "Återfuktande schampo för alla hårtyper.", "price": 45.00, "quantity": 130},
    {"id": 11, "name": "Diskmedel", "desc": "Miljövänligt diskmedel för skinande disk.", "price": 40.00, "quantity": 110},
    {"id": 12, "name": "Toalettpapper 10-pack", "desc": "Mjukt och starkt toalettpapper.", "price": 60.00, "quantity": 60},
    {"id": 13, "name": "Potatis 2kg", "desc": "Svenska potatisar, perfekta för all matlagning.", "price": 45.00, "quantity": 100},
    {"id": 14, "name": "Tomater 1kg", "desc": "Färska tomater för sallader och matlagning.", "price": 40.00, "quantity": 90},
    {"id": 15, "name": "Kycklingbröst 1kg", "desc": "Kycklingbröst av hög kvalitet.", "price": 90.00, "quantity": 50}
]

# Colors
black = (0, 0, 0)
dark_gray = (50, 50, 50)
white = (255, 255, 255)

# Button setup
button_rect = pygame.Rect((window_size[0]//2 - 100, window_size[1]//2 - 50, 200, 100))
button_rect2 = pygame.Rect((window_size[0]//2 - 10, window_size[1] - 150, 150, 100))
button_rect3 = pygame.Rect((window_size[0]//2 - 350, window_size[1] - 150, 200, 100))
button_rect4 = pygame.Rect((window_size[0]//2 - 150, window_size[1] - 150, 150, 100))


# Function to render the front page
def render_front_page():
    window.blit(front_page_image, (0, 0))
    pygame.draw.rect(window, dark_gray, button_rect)
    button_text = button_font.render("GO", True, white)
    text_rect = button_text.get_rect(center=button_rect.center)
    window.blit(button_text, text_rect)
    pygame.display.flip()

# Function to render the product list
def render_product_list():
    window.fill((155, 161, 157))
    pygame.draw.rect(window, dark_gray, button_rect2)
    button_text = button_font.render("Add", True, white)
    text_rect = button_text.get_rect(center=button_rect2.center)
    window.blit(button_text, text_rect)

    pygame.draw.rect(window, dark_gray, button_rect3)
    button_text = button_font.render("Remove", True, white)
    text_rect = button_text.get_rect(center=button_rect3.center)
    window.blit(button_text, text_rect)

    pygame.draw.rect(window, dark_gray, button_rect4)
    button_text = button_font.render("Change", True, white)
    text_rect = button_text.get_rect(center=button_rect4.center)
    window.blit(button_text, text_rect)

    headers = ["Name", "Description", "Price (SEK)", "Quantity"]
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
            f"{product['price']}",
            f"{product['quantity']}"
        ]
        for i, detail in enumerate(product_details):
            detail_surface = font.render(detail, True, black)
            window.blit(detail_surface, (header_x_positions[i], y))
        y += 30
    pygame.display.flip()

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

    if on_front_page:
        render_front_page()
    else:
        render_product_list()

pygame.quit()
sys.exit()
