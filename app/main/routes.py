from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from flask import jsonify, render_template, request
from flask_login import current_user
from sqlalchemy import desc
from ..extensions import db
from ..models import (
    Addon, BillRequest, CafeTable, Feedback, MenuItem, MenuImage,
    Order, OrderItem, OrderItemAddon, WaiterRequest
)
from . import main_bp

TAX_RATE = Decimal("0.05")

def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def get_table(table_number):
    table_number = str(table_number or "04").strip().lstrip("#")
    table = CafeTable.query.filter_by(table_number=table_number, is_active=True).first()
    return table

@main_bp.get("/")
def index():
    return render_template("main/index.html")

@main_bp.get("/api/menu")
def menu():
    category = request.args.get("category")
    query = MenuItem.query
    if category and category != "all":
        query = query.filter_by(category=category)
    items = query.order_by(MenuItem.id).all()
    return jsonify([
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": float(item.price),
            "rating": float(item.rating or 0),
            "reviews": item.reviews or 0,
            "image": item.image,
            "gallery": [g.image_url for g in sorted(item.gallery, key=lambda x: x.sort_order)],
            "desc": item.description,
            "addons": [
                {"id": a.id, "name": a.name, "price": float(a.price)}
                for a in item.addons
            ],
        }
        for item in items
    ])

@main_bp.post("/api/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    table = get_table(data.get("table"))
    if not table:
        return jsonify({"error": "Invalid or inactive table."}), 400

    raw_items = data.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        return jsonify({"error": "Order must contain at least one item."}), 400

    order_items_payload = []
    subtotal = Decimal("0.00")

    for raw in raw_items:
        try:
            item_id = int(raw["id"])
            quantity = int(raw.get("qty", 1))
        except (KeyError, TypeError, ValueError):
            return jsonify({"error": "Invalid item or quantity."}), 400

        if quantity < 1 or quantity > 50:
            return jsonify({"error": "Quantity must be between 1 and 50."}), 400

        item = db.session.get(MenuItem, item_id)
        if not item:
            return jsonify({"error": f"Menu item {item_id} does not exist."}), 400

        addon_names = raw.get("addons", [])
        if not isinstance(addon_names, list):
            addon_names = []

        selected_addons = []
        addon_total = Decimal("0.00")
        for addon_name in addon_names:
            addon = Addon.query.filter_by(menu_item_id=item.id, name=str(addon_name)).first()
            if not addon:
                return jsonify({"error": f"Invalid add-on for {item.name}: {addon_name}"}), 400
            selected_addons.append(addon)
            addon_total += Decimal(str(addon.price))

        unit_price = money(Decimal(str(item.price)) + addon_total)
        line_total = money(unit_price * quantity)
        subtotal += line_total

        order_items_payload.append((item, quantity, unit_price, selected_addons, str(raw.get("instructions", ""))[:500]))

    subtotal = money(subtotal)
    tax = money(subtotal * TAX_RATE)
    total = money(subtotal + tax)

    order = Order(
        order_number=f"AROMA-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{datetime.utcnow().microsecond // 1000:03d}",
        table_id=table.id,
        user_id=current_user.id if current_user.is_authenticated else None,
        status="pending",
        subtotal=subtotal,
        tax=tax,
        total=total,
    )
    db.session.add(order)
    db.session.flush()

    for item, quantity, unit_price, selected_addons, instructions in order_items_payload:
        oi = OrderItem(
            order_id=order.id,
            menu_item_id=item.id,
            item_name=item.name,
            unit_price=unit_price,
            quantity=quantity,
            instructions=instructions,
        )
        db.session.add(oi)
        db.session.flush()
        for addon in selected_addons:
            db.session.add(OrderItemAddon(
                order_item_id=oi.id,
                addon_id=addon.id,
                addon_name=addon.name,
                addon_price=addon.price,
            ))

    db.session.commit()

    return jsonify({
        "message": "Order dispatched to kitchen.",
        "order_id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "subtotal": float(subtotal),
        "tax": float(tax),
        "total": float(total),
    }), 201

@main_bp.get("/api/orders/<int:order_id>")
def order_status(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"error": "Order not found."}), 404
    return jsonify({
        "order_id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "total": float(order.total),
        "created_at": order.created_at.isoformat(),
    })

@main_bp.post("/api/waiter-requests")
def waiter_request():
    data = request.get_json(silent=True) or {}
    table = get_table(data.get("table"))
    if not table:
        return jsonify({"error": "Invalid or inactive table."}), 400
    req = WaiterRequest(table_id=table.id)
    db.session.add(req)
    db.session.commit()
    return jsonify({"message": f"Waiter requested for table #{table.table_number}.", "request_id": req.id}), 201

@main_bp.post("/api/bill-requests")
def bill_request():
    data = request.get_json(silent=True) or {}
    table = get_table(data.get("table"))
    if not table:
        return jsonify({"error": "Invalid or inactive table."}), 400
    req = BillRequest(table_id=table.id)
    db.session.add(req)
    db.session.commit()
    return jsonify({"message": f"Bill requested for table #{table.table_number}.", "request_id": req.id}), 201

@main_bp.post("/api/feedback")
def feedback():
    data = request.get_json(silent=True) or {}
    table = get_table(data.get("table"))
    try:
        rating = int(data.get("rating"))
    except (TypeError, ValueError):
        rating = 0
    if not table or rating not in range(1, 6):
        return jsonify({"error": "Valid table and rating from 1 to 5 are required."}), 400

    entry = Feedback(
        table_id=table.id,
        rating=rating,
        message=str(data.get("message", ""))[:2000],
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Feedback received.", "feedback_id": entry.id}), 201
