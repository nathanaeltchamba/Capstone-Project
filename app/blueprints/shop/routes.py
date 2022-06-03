from math import prod
from flask import render_template, current_app as app, flash, redirect, url_for
from flask_login import current_user, login_required
import stripe
from .models import Cart
from app import db

stripe.api_key = app.config.get('STRIPE_SK')

# Shop Routes
@app.route('/shop')
def shop():
    products = []
    for product in stripe.Product.list()['data']:

        price = stripe.Price.retrieve(product['default_price'])['unit_amount'] / 100

        product_dict = {
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price':f"{price:,.2f}",
            'image': product['images'][0],
        }
        products.append(product_dict)
    return render_template('shop/shop.html', products=products)

@app.route('/shop/cart/add/<product_id>')
@login_required
def shop_cart_add(product_id):
    user_cart = Cart.query.filter_by(user_id=current_user.get_id())

    cart_product = user_cart.filter_by(product_id=product_id).first()

    # if the user doesn't have a cart, create it
    if cart_product is None:
        cart = Cart(
            product_id=product_id,
            user_id=current_user.get_id(),
            quantity=1
        )
        db.session.add(cart)
        #if user has a cart and has the item already in it

    else:
        # if the same product is already found in the cart
        cart_product.quantity += 1
    db.session.commit()

    flash('Item added to cart', 'info')
    return redirect(url_for('shop'))

@app.route('/shop/<id>')
def shop_single(id):
    return render_template('shop/single.html')

@app.route('/shop/cart')
@login_required
def shop_cart():
    cart_items =[]
    for item in Cart.query.filter_by(user_id=current_user.get_id()).all():
        stripe_product = stripe.Product.retrieve(item.product_id)
        # stripe_description = stripe.Product.retrieve(stripe_product['description'])
        price = stripe.Price.retrieve(stripe_product['default_price'])['unit_amount'] / 100
        product_dict = {
            'info': stripe_product,
            # 'description': item.description,
            'price' : f"{price:,.2f}",
            'quantity': item.quantity
        }
        cart_items.append(product_dict)

    return render_template('shop/cart.html', cart=cart_items)
    # add these routes to the shop page later

@app.route('/shop/checkout', methods=['POST'])
@login_required
def shop_checkout():

    items = []
    user_cart = Cart.query.filter_by(user_id=current_user.get_id()).all()

    for item in user_cart:
        stripe_product = stripe.Product.retrieve(item.product_id)
        product_dict = {
            'price': stripe_product['default_price'],
            'quantity': item.quantity
        }
        items.append(product_dict)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:5000/shop/cart',
            cancel_url='http://127.0.0.1:5000/shop/cart',
        )
        
        # remove items from cart if it is successful transaction
        for item in user_cart:
            db.session.delete(item)
        db.session.commit()
        flash('Your payment was successful', 'success')
    except Exception as e:
        flash('Your payment was unsuccessful. Please try again', 'danger')
        return str(e)
    return redirect(checkout_session.url)
    # add these routes to the shop page later