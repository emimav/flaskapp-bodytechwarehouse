import os
from flask import render_template, url_for, redirect, flash, session, request, jsonify
from myshop import app, db
from myshop.forms import RegisterForm, LoginForm, ContactUs, ReviewForm, BillingInfo
from myshop.models import User, Item, ReviewItem, Cart, CartItem, Order, OrderItem, Enquiry, BillingInformation
from flask_login import login_user, current_user, logout_user, login_required
import datetime

currentDT = datetime.datetime.now()

@app.route('/', defaults={'categoryId': 1})
@app.route("/<int:categoryId>")
def home(categoryId):
	products = None
	if categoryId == 7:
		products = Item.query.all()
	else:
		products = Item.query.filter_by(category_id=categoryId).all()
	return render_template('home.html', title='Home', products=products)


@app.route("/item/<item_id>", methods=['GET','POST'])
def item_details(item_id):
        itema = Item.query.filter_by(id=item_id).first()
        form = ReviewForm()
        if form.validate_on_submit():
            try:
                    name = current_user.first_name + ' ' + current_user.last_name
                    review = ReviewItem(user=name, item=item_id, content=form.content.data, rating=form.rating.data,timestamp=str(currentDT.strftime("%Y/%m/%d")))
                    db.session.add(review)
                    db.session.commit()			
                    flash(f"Your review has been successfully saved!")
                    return redirect(url_for('home'))
            except Exception as ex:
                    flash(f"Error {ex}")
                    return redirect(url_for('home'))

        return render_template('product_details.html', title=itema.title, item=itema, form=form)


@app.route("/item/<item_id>/add_to_cart")
def add_to_cart(item_id):
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(userId=current_user.id).first()   # check if the user has a cart, if the user doesn't
        if not cart:                                                  # have a cart, it gets created
            cart = Cart(userId=current_user.id)                       # if the user has a cart and a specific item existing
            db.session.add(cart)                                      # in the cart, this gets incremented
        cart_item = CartItem.query.filter_by(item=item_id, cart=cart.id).first()    # if there are no items, the item added
                                                                                    # to the cart gets incremented
        if not cart_item:
            cart_item = CartItem(item=item_id, cart=cart.id, quantity=1)
            db.session.add(cart_item)
            cart.cartItems.append(cart_item)

        else:
            for item in cart.cartItems:
                if item.id == cart_item.id:
                    item.quantity += 1
        db.session.commit()
        return redirect(request.referrer)
    else:
        return redirect(url_for("register"))

@app.route("/item/<item_id>/remove_from_cart")
@login_required
def remove_from_cart(item_id):
    cart = Cart.query.filter_by(userId=current_user.id).first()   # check if the user has a cart, if the user doesn't
    if cart:                                                  # have a cart, it gets created

        cart_item = CartItem.query.filter_by(item=item_id, cart=cart.id).first()    # if there are no items, the item added
                                                                                # to the cart gets incremented

        if cart_item:
            # If previous quantity was 1, delete cart_item
            if cart_item.quantity == 1:
                db.session.delete(cart_item)

            else:
                cart_item.quantity -= 1
            db.session.commit()

    return redirect(request.referrer)


@app.route("/cart", methods=['GET','POST'])

def get_user_cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(userId=current_user.id)
        sub = CartItem.query.filter(CartItem.cart==cart[0].id)
        price = 0
        return render_template("cart.html", products=sub, price=price)
    else:
        return redirect(url_for("register"))


@app.route("/billing", methods=['GET','POST'])
@login_required
def billing():
    form = BillingInfo()
    if form.validate_on_submit():
        info = BillingInfo(form.first_name.data, form.last_name.data, form.username.data, form.billing_addr.data,
                           form.credit_card_num.data, form.credit_card_expiry.data, form.bill_date)
        db.session.add(info)
        db.session.commit()
        flash("Your order has been processed. We will get in touch with you shortly")
        return redirect(url_for('home'))
    else:
        flash('Something went wrong. Please try again')
    return render_template("billing.html", form=form)



@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            if login_user(user):
                return redirect(url_for('home'))
        flash('Invalid email or password.')
    return render_template('login.html', title='Login', form=form)



@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Your registration has been submitted. You can now log in!")
        return redirect(url_for('login'))	
    else:
        flash('Invalid name or password')
          

    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactUs()
    if form.validate_on_submit():
        enquiry = Enquiry(name=form.name.data,
              content =form.content.data
        )
        db.session.add(enquiry)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('contactus.html', form=form)


@app.route('/view_enquiries')
@login_required
def view_enquiries():
    enquiries = Enquiry.query.all()
    return render_template('view_enquiries.html')



