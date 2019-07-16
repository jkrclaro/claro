from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
from flask_login import login_required, current_user

from src.wadless.helpers.flash import flash_form_errors
from src.wadless.helpers.model import get_or_404
from src.wadless.models import db
from src.wadless.models.dashboard import Product, Variant, Inventory
from src.wadless.forms import (
    ProductBaseForm,
    VariantBaseForm,
    InventoryBaseForm,
)

product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ProductBaseForm()
    if form.validate_on_submit():
        title = form.title.data
        data_product = {
            'account_id': current_user.account.id,
            'title': title,
            'url': form.url.data,
            'caption': form.caption.data,
            'description': form.description.data,
            'uid': form.uid.data,
        }
        product = Product(**data_product)
        db.session.add(product)
        db.session.commit()
        flash(f'Successfully added {title}', 'success')
        return redirect(url_for('product.index'))
    else:
        flash_form_errors(form.errors)

    products = Product.query.filter_by(account_id=current_user.account.id).all()
    return render_template('product/index.html', products=products, form=form)


@product_bp.route('/<uid>', methods=['GET', 'POST'])
@login_required
def retrieve(uid: str):
    options = {'account_id': current_user.account.id, 'uid': uid}
    product = get_or_404(Product, options)

    form = ProductBaseForm(obj=product)
    if form.validate_on_submit():
        product.title = form.title.data
        product.url = form.url.data
        product.caption = form.caption.data
        product.description = form.description.data
        product.uid = form.uid.data
        db.session.add(product)
        db.session.commit()
        flash('Successfully updated product', 'success')
        return redirect(url_for('product.retrieve', uid=product.uid))
    else:
        flash_form_errors(form.errors)

    context = {
        'form': form,
        'form_inventory': InventoryBaseForm(),
        'product': product
    }
    return render_template('product/retrieve.html', **context)


@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form_product = ProductBaseForm(prefix='product')
    form_variant = VariantBaseForm(prefix='variant')
    form_inventory = InventoryBaseForm(prefix='inventory')

    if request.method == 'POST':
        forms_validated = (
                form_product.validate() and
                form_variant.validate() and
                form_inventory.validate()
        )

        if forms_validated:
            data_product = {
                'account_id': current_user.account.id,
                'title': form_product.title.data,
                'url': form_product.url.data,
                'caption': form_product.caption.data,
                'description': form_product.description.data,
                'uid': form_product.uid.data,
            }
            product = Product(**data_product)
            db.session.add(product)
            db.session.commit()

            data_variant = {
                'product_id': product.id,
                'title': form_variant.title.data
            }
            variant = Variant(**data_variant)
            db.session.add(variant)
            db.session.commit()

            data_inventory = {
                'variant_id': variant.id,
                'quantity': form_inventory.quantity.data,
                'price': form_inventory.price.data,
                'sku': form_inventory.sku.data,
            }
            inventory = Inventory(**data_inventory)
            db.session.add(inventory)
            db.session.commit()

            flash(f'Successfully added product', 'success')
            return redirect(url_for('product.index'))
        else:
            flash_form_errors(form_product.errors)
            flash_form_errors(form_variant.errors)
            flash_form_errors(form_inventory.errors)

    context = {
        'form_product': form_product,
        'form_variant': form_variant,
        'form_inventory': form_inventory
    }
    return render_template('product/create.html', **context)
