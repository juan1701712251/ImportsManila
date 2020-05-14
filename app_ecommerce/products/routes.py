from flask import (render_template, url_for, flash, request,
                   redirect, Blueprint)
from flask_login import login_required
from app_ecommerce.categories.utils import get_categories_allowed
from app_ecommerce.products.utils import save_picture, delete_image_file
from app_ecommerce.products.forms import ProductsForm
from app_ecommerce.models import Product, Category
from app_ecommerce import db,quote

products = Blueprint('products',__name__)

@products.route('/products/new',methods=['GET','POST'])
@login_required
def new_product():
    form = ProductsForm()
    form.category.choices = get_categories_allowed()
    if form.validate_on_submit():
        #print(form.image1.data)
        #print(form.image2.data)
        #print(form.image3.data)
        img1 = None
        img2 = None
        img3 = None
        if form.image1.data:
            img1 = save_picture(form.image1.data,'product_pics')
        if form.image2.data:
            img2 = save_picture(form.image2.data,'product_pics')
        if form.image3.data:
            img3 = save_picture(form.image3.data,'product_pics')
        cate = Category.query.get(form.category.data)
        product = Product(name=form.name.data,
                          description=form.description.data,
                          weight=form.weight.data,
                          price=form.price.data,
                          cate=cate,
                          image_file1=img1,
                          image_file2=img2,
                          image_file3=img3,
                          spent= 1 if form.spent.data == True or form.spent.data == "True" else 0)
        db.session.add(product)
        db.session.commit()
        flash(f'Your product has been created','success')
        return redirect(url_for('main.home'))

    return render_template('create_product.html', title='New Product', form=form, legend='New Product')

@products.route('/product/<int:product_id>/update',methods=['GET','POST'])
@login_required
def update_product(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductsForm()
    form.category.choices = get_categories_allowed()
    if form.validate_on_submit():
        img1 = p.image_file1
        img2 = p.image_file2
        img3 = p.image_file3
        if form.image1.data:
            delete_image_file(img1)
            img1 = save_picture(form.image1.data,'product_pics')
        if form.image2.data:
            delete_image_file(img2)
            img2 = save_picture(form.image2.data,'product_pics')
        if form.image3.data:
            delete_image_file(img3)
            img3 = save_picture(form.image3.data,'product_pics')
        cate = Category.query.get(form.category.data)

        #Actualizamos los datos
        p.name=form.name.data
        p.description=form.description.data
        p.weight=form.weight.data
        p.price=form.price.data
        p.cate=cate
        p.image_file1=img1
        p.image_file2=img2
        p.image_file3=img3
        p.spent = 1 if form.spent.data == True or form.spent.data == "True" else 0

        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('main.home'))

    elif request.method == 'GET':
        form.name.data = p.name
        form.description.data = p.description
        form.weight.data = p.weight
        form.price.data = p.price
        form.spent.data = "True" if p.spent else "False"


    return render_template('create_product.html', title='Update Product', form=form, legend='Update Product')

@products.route('/product/<int:product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title='Product',quote=quote,product=product)

@products.route('/product/<int:product_id>/delete_product',methods=['POST'])
@login_required
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash(f'Your product has been deleted','info')
    return redirect(url_for('main.home'))
