"""
Everything the site shows about Gellar's lives in this file.
Update prices, hours and items here; app.py never needs to change.

Rules:
- price=None shows "Ask at the window" and can't be added to an order.
  Fill these in once you have the menu-board prices from the owner.
- out_of_stock=True greys an item out and hides its Add button.

Source for current prices: Gellar's Toast ordering page, October 2026.
"""

BUSINESS = {
    "name": "Gellar's Snack Bar",
    "sign_name": "Gellars",
    "tagline": "Ice cream, burgers and fried clams on Route 3A since 1926.",
    "address_line1": "506 State Road (Route 3A)",
    "address_line2": "Manomet, Plymouth, MA 02360",
    "cross_street": "At the corner of White Horse Road",
    "phone_display": "(508) 224-2772",
    "phone_tel": "+15082242772",
    "email": "gellarssnackbar506@gmail.com",
    "facebook": "https://www.facebook.com/GellarsSnackBar/",
    "toast_url": "https://order.toasttab.com/online/gellar-s-snack-bar-506-state-road",
    "map_query": "Gellar's Snack Bar, 506 State Rd, Plymouth, MA 02360",
    "founded": 1926,
}

# 24-hour clock, Eastern time. None means closed that day.
# TODO: confirm with the owner. Hours change with the season.
HOURS = {
    "Monday": None,
    "Tuesday": None,
    "Wednesday": None,
    "Thursday": ("11:00", "20:00"),
    "Friday": ("11:00", "20:00"),
    "Saturday": ("09:00", "20:00"),
    "Sunday": ("09:00", "20:00"),
}

# TODO: replace with the real flavor list from the owner.
# These are flavors customers have reported seeing recently.
FLAVORS_SPOTTED = [
    "Vanilla", "Chocolate", "Strawberry", "Banana",
    "Coconut", "Tiramisu", "Cookies & cream",
]


def item(name, price=None, desc="", out_of_stock=False):
    return {"name": name, "price": price, "desc": desc, "out_of_stock": out_of_stock}


SANDWICH_SIDES = "Served with coleslaw, Cape Cod chips and a house-made pickle spear."
BURGER_BASE = (
    "On a buttered, grilled brioche bun with your choice of lettuce, tomato, red onion, "
    "house-made pickle chips, ketchup, mayo, mustard and relish. Pickle spear and coleslaw on the side."
)

MENU = [
    {
        "tab": "Ice cream",
        "intro": (
            "24 soft-serve flavors and about three dozen hard flavors from Richardson's "
            "in Middleton. Flavors rotate, so ask at the window for today's list."
        ),
        "sections": [
            {
                "title": "Cones & cups",
                "note": "One size, and it's a tall one.",
                "items": [
                    item("Soft serve, cone or cup", None, "Pick from 24 flavors, or twist two together."),
                    item("Hard ice cream, cone or cup", None, "Richardson's, made in Middleton, MA."),
                    item("Sprinkles or a topping", None),
                ],
            },
            {
                "title": "Frappes, floats & sundaes",
                "note": "",
                "items": [
                    item("Frappe", 10.00, "A thick 24 oz frappe made with your choice of ice cream, house-made syrup and whole milk."),
                    item("S'mores milkshake", None),
                    item("Root beer float", None),
                    item("Sundae", None, "Your choice of ice cream and toppings."),
                    item("Banana split", None),
                ],
            },
        ],
    },
    {
        "tab": "Burgers & grill",
        "intro": "Burgers are hand-packed by Perry's Market in Plymouth. Ask for one dragged through the garden and you get every topping.",
        "sections": [
            {
                "title": "Burgers",
                "note": "",
                "items": [
                    item("Hamburger", 12.00, "A 1/4 lb burger. " + BURGER_BASE),
                    item("Cheeseburger", 12.00, "A 1/4 lb burger with cheese. " + BURGER_BASE),
                    item("Bacon cheeseburger", 14.00, "A 1/4 lb burger with cheese and bacon. " + BURGER_BASE),
                    item("Double stack hamburger", 15.00, "Two 1/4 lb burgers with your choice of cheese and toppings."),
                    item("Double stack cheeseburger", 15.00, "Two 1/4 lb burgers with cheese and your choice of toppings."),
                    item("Veggie burger", 13.00, "A 4 oz southwest black bean and sweet potato patty on a grilled brioche bun with your choice of toppings."),
                ],
            },
            {
                "title": "Chicken",
                "note": "",
                "items": [
                    item("Fried chicken sandwich", 13.00, "Crispy fried chicken breast on a grilled brioche bun with your choice of toppings. " + SANDWICH_SIDES),
                    item("Grilled chicken sandwich", 13.00, "Grilled chicken breast on a grilled brioche bun with your choice of toppings. " + SANDWICH_SIDES),
                    item("Chicken bacon ranch sandwich", 15.00, "Crispy fried chicken, bacon and buttermilk ranch on a grilled brioche bun. " + SANDWICH_SIDES),
                    item("Chicken tenders with fries", 13.00, "Five crispy fried chicken tenders with French fries."),
                ],
            },
            {
                "title": "Hot dogs",
                "note": "",
                "items": [
                    item("Hot dog", 7.00, "Grilled, on a grilled buttered bun with ketchup, mustard, relish and onions as you like. " + SANDWICH_SIDES),
                    item("Double dog", 10.00, "Two grilled dogs on grilled buttered buns, toppings as you like. " + SANDWICH_SIDES),
                ],
            },
            {
                "title": "Sandwiches & clubs",
                "note": "Choose country white, whole wheat or sourdough.",
                "items": [
                    item("Grilled cheese", 7.00, SANDWICH_SIDES),
                    item("BLT", 10.00, SANDWICH_SIDES),
                    item("All white tuna", 11.00, "With your choice of lettuce, tomato, red onion and pickle chips. " + SANDWICH_SIDES),
                    item("Walnut cranberry chicken salad", 12.00, "With your choice of lettuce, tomato, red onion and pickle chips. " + SANDWICH_SIDES),
                    item("Angus roast beef", 13.00, "A 1/4 lb of roast beef with your choice of toppings. " + SANDWICH_SIDES),
                    item("Turkey club", 13.00, "Three slices of bread layered with turkey, bacon, lettuce, tomato and mayo. " + SANDWICH_SIDES),
                    item("Cheeseburger club", 16.00, "Three slices of bread layered with two cheeseburgers, bacon, lettuce, tomato and mayo. " + SANDWICH_SIDES),
                ],
            },
            {
                "title": "Friday night seafood",
                "note": "Fresh seafood on Friday nights while it lasts.",
                "items": [
                    item("Fish and chips", None),
                    item("Whole belly clam plate", None),
                    item("Clam strip plate", None),
                ],
            },
        ],
    },
    {
        "tab": "Breakfast & coffee",
        "intro": "Breakfast sandwiches start as soon as the window opens.",
        "sections": [
            {
                "title": "Egg sandwiches",
                "note": "",
                "items": [
                    item("Bacon, egg and cheese", 6.00),
                    item("Sausage, egg and cheese", 6.00),
                    item("Ham, egg and cheese", 6.00),
                    item("Egg and cheese", 6.00, "No meat."),
                ],
            },
            {
                "title": "Eggs & sides",
                "note": "",
                "items": [
                    item("Fried egg", 2.00),
                    item("Scrambled egg", 2.00),
                    item("Hash brown", 2.00),
                    item("Two slices of bacon", 2.00),
                    item("Sausage patty", 2.00),
                    item("English muffin", 1.50),
                    item("Bagel", 3.00),
                    item("Toast, two slices", 1.50, "Country white, whole wheat or sourdough."),
                ],
            },
            {
                "title": "Coffee, tea & cocoa",
                "note": "",
                "items": [
                    item("Hot coffee, 16 oz", 3.00),
                    item("Iced cold brew, 12 oz", 4.00),
                    item("Iced cold brew, 24 oz", 6.00),
                    item("Hot chocolate, 16 oz", 4.00),
                    item("Hot tea, 16 oz", 3.00),
                    item("Iced tea, 12 oz", 3.00),
                    item("Iced tea, 24 oz", 5.00),
                    item("Iced sweet tea, 12 oz", 4.00, out_of_stock=True),
                    item("Iced sweet tea, 24 oz", 6.00, out_of_stock=True),
                ],
            },
        ],
    },
    {
        "tab": "Sides & drinks",
        "intro": "The onion rings are the ones people drive over for.",
        "sections": [
            {
                "title": "From the fryer",
                "note": "",
                "items": [
                    item("French fries", 5.00),
                    item("Onion rings", 7.00),
                ],
            },
            {
                "title": "Extras",
                "note": "",
                "items": [
                    item("Coleslaw", 2.00),
                    item("Cape Cod potato chips", 1.15, "1 oz bag, sea salt original."),
                ],
            },
            {
                "title": "Drinks",
                "note": "",
                "items": [
                    item("House-made fruit lemonade, 12 oz", 5.00),
                    item("House-made fruit lemonade, 24 oz", 6.00),
                    item("Coke, 20 oz", 2.82),
                    item("Coke Zero, 20 oz", 2.00),
                    item("Dr Pepper, 20 oz", 2.82),
                    item("Ginger ale, 20 oz", 2.82),
                    item("Orange soda, 20 oz", 2.82),
                    item("Smartwater, 20 oz", 3.50),
                ],
            },
        ],
    },
]
