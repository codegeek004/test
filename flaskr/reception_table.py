from flask import render_template,request,redirect,url_for,flash,Blueprint,session
import mysql.connector
from db import db,cursor
#Blueprint
reception = Blueprint('reception',__name__)
#Display
#Route to display data
@reception.route('/reception')
def reception_table():
    cursor.execute("SELECT * FROM reception;")
    data = cursor.fetchall()
    return render_template('view/view_data.html', data = data)

#Route to add data
@reception.route('/reception/add',methods = ['GET','POST'])
def add_data():
    if request.method == 'POST':
        name= request.form['patient_name']
        age = request.form['patient_age']
        contact = request.form['patient_contact']
        email = request.form['patient_email']
        address = request.form['patient_address']
        cursor.execute('INSERT INTO reception (name,age,contact,email,address) VALUES (%s,%s,%s,%s,%s)',(name,age,contact,email,address))
        db.commit()
        flash('Data added successfully')
        return redirect('/reception')
    return render_template('add/add_data.html')

# Route to update/edit data
@reception.route('/reception/edit/<int:id>', methods=['GET', 'POST'])
def update_data(id):
    if request.method == 'POST':
        name = request.form['patient_name']
        age = request.form['patient_age']
        contact = request.form['patient_contact']
        email = request.form['patient_email']
        address = request.form['patient_address']
        
        try:
            update_query = '''
                UPDATE reception
                SET name=%s, age=%s, contact=%s, email=%s, address=%s
                WHERE id = %s'''
            cursor.execute(update_query, (name, age, contact, email, address, id))
            db.commit()
            flash('Data updated successfully')
            return redirect(url_for('reception.reception_table'))
        except mysql.connector.Error as e:
            db.rollback()
            flash(f'Error updating data: {e}', 'danger')

    fetch_query = """
        SELECT
        name, age, contact, email, address 
        FROM reception
        WHERE id=%s """
    cursor.execute(fetch_query, (id,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        flash('Data not found', 'danger')
        return redirect(url_for('reception.reception_table'))

    return render_template('update/update_data.html', id = id, reception_data=data)

#Route to delete data
@reception.route('/reception/delete/<int:id>',methods=['GET','POST'])
def delete_data(id):
    if request.method=='POST':
        try:
            delete_query = 'DELETE FROM reception WHERE id = %s'
            cursor.execute(delete_query,(id,))
            db.commit()
            flash('Data deleted successfully')
        except mysql.connector.Error as e:
            db.rollback()
            flash(f'Error deleting {e}','danger')

    fetch_query="""
        SELECT 
        name,age,contact,email,address
        FROM reception
        WHERE id=%s"""
    cursor.execute(fetch_query, (id,))
    data=cursor.fetchone()
    print(data)
    if data is None:
        flash(f'data not found','danger')
        return redirect(url_for('reception.reception_table'))
    return render_template('delete/delete_data.html', id = id,reception_data=data)

