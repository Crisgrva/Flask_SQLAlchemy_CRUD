from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db

contacts = Blueprint('contacts', __name__)


@contacts.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@contacts.route('/new', methods=['POST'])
def add_contact():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']

    new_contact = Contact(fullname, email, phone)

    db.session.add(new_contact)
    db.session.commit()

    flash(f"{fullname} was added succesfully")

    return redirect(url_for('contacts.index'))


@contacts.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.fullname = request.form['fullname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        db.session.commit()

        flash(f"{contact.fullname} was updated succesfully")
        return redirect(url_for('contacts.index'))

    return render_template('update.html', contact=contact)


@contacts.route('/delete/<id>')
def delete(id):
    contact = Contact.query.get(id)
    tmp_fullname = contact.fullname
    db.session.delete(contact)
    db.session.commit()

    flash(f"{tmp_fullname} was deleted succesfully")
    return redirect(url_for('contacts.index'))


@contacts.route('/about')
def about():
    return render_template('about.html')
