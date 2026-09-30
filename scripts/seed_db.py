from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models import CafeTable, MenuItem, MenuImage, Addon

app = create_app()

MENU = [
    {
        "id": 1, "name": "Caramel Macchiato", "category": "coffee", "price": "4.50", "rating": "4.8", "reviews": 124,
        "image": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Rich espresso combined with vanilla syrup and marked with caramel drizzle over velvety steamed milk.",
        "addons": [("Extra Espresso Shot", "1.00"), ("Oat Milk Substitute", "0.75"), ("Extra Caramel Drizzle", "0.50")]
    },
    {
        "id": 2, "name": "Classic Butter Croissant", "category": "bakery", "price": "3.20", "rating": "4.9", "reviews": 98,
        "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Flaky, buttery French pastry baked golden brown hourly in-house using authentic imported European butter.",
        "addons": [("Add Strawberry Jam", "0.50"), ("Add Artisanal Butter", "0.60"), ("Warm It Up", "0.00")]
    },
    {
        "id": 3, "name": "Avocado Sourdough Toast", "category": "fastfood", "price": "7.50", "rating": "4.7", "reviews": 210,
        "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Mashed avocado, poached organic egg, chili flakes, and microgreens on toasted artisan sourdough.",
        "addons": [("Extra Poached Egg", "1.50"), ("Add Smoked Salmon", "3.00"), ("Extra Feta Cheese", "1.00")]
    },
    {
        "id": 4, "name": "Triple Chocolate Brownie", "category": "dessert", "price": "4.00", "rating": "5.0", "reviews": 156,
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Rich gooey chocolate brownie packed with melted chocolate chunks and baked to fudge perfection.",
        "addons": [("Add Vanilla Ice Cream Scoop", "1.50"), ("Hot Fudge Drizzle", "0.75")]
    },
    {
        "id": 5, "name": "Iced Spanish Latte", "category": "coffee", "price": "5.00", "rating": "4.9", "reviews": 89,
        "image": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Smooth signature espresso blended with sweetened condensed milk and served over crystal ice.",
        "addons": [("Less Sweet", "0.00"), ("Extra Ice", "0.00"), ("Oat Milk Substitute", "0.75")]
    },
    {
        "id": 6, "name": "Crispy Truffle Fries", "category": "fastfood", "price": "5.50", "rating": "4.6", "reviews": 74,
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Hand-cut golden fries tossed exquisitely in truffle oil, fresh parsley, and grated parmesan cheese.",
        "addons": [("Extra Truffle Mayo Dip", "0.75"), ("Extra Parmesan", "0.75")]
    },
    {
        "id": 7, "name": "Matcha Green Tea Latte", "category": "beverages", "price": "4.80", "rating": "4.7", "reviews": 112,
        "image": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "Ceremonial grade Japanese matcha whisked smooth with steamed milk and a hint of vanilla.",
        "addons": [("Almond Milk", "0.75"), ("Extra Matcha Shot", "1.25")]
    },
    {
        "id": 8, "name": "Berry Cheesecake Slice", "category": "dessert", "price": "5.20", "rating": "4.9", "reviews": 143,
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=600",
        "gallery": [
            "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1524351199678-941a58a3df50?auto=format&fit=crop&q=80&w=600"
        ],
        "desc": "New York style creamy baked cheesecake topped with fresh house-made mixed berry compote.",
        "addons": [("Extra Berry Compote", "0.75"), ("Whipped Cream", "0.50")]
    }
]

with app.app_context():
    db.create_all()

    for number in [f"{i:02d}" for i in range(1, 9)]:
        if not CafeTable.query.filter_by(table_number=number).first():
            db.session.add(CafeTable(table_number=number))

    for data in MENU:
        item = db.session.get(MenuItem, data["id"])
        if not item:
            item = MenuItem(
                id=data["id"], name=data["name"], category=data["category"],
                price=Decimal(data["price"]), rating=Decimal(data["rating"]),
                reviews=data["reviews"], image=data["image"], description=data["desc"]
            )
            db.session.add(item)
            db.session.flush()
        for index, image_url in enumerate(data["gallery"]):
            if not MenuImage.query.filter_by(menu_item_id=item.id, image_url=image_url).first():
                db.session.add(MenuImage(menu_item_id=item.id, image_url=image_url, sort_order=index))
        for name, price in data["addons"]:
            if not Addon.query.filter_by(menu_item_id=item.id, name=name).first():
                db.session.add(Addon(menu_item_id=item.id, name=name, price=Decimal(price)))

    db.session.commit()
    print("Aroma Cafe database seeded successfully.")
