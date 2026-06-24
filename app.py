from flask import Flask,render_template, request, redirect, url_for , flash
from database import get_connection

app = Flask(__name__)
app.secret_key = "IMSwebapp"

@app.route("/")
def home():
    return redirect(url_for('dashboard'))

@app.route("/test-db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        return f"Database successfully connected:{result}"
    except Exception as e:
        return f"Exception occured when connecting:{e}"
    
@app.route("/add-product")
def add_product():
    return render_template('add_product.html')

@app.route("/add" , methods=["POST"])
def add():
    try:
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        if not name.strip():

            flash(
                'Product name cant be empty',
                "danger"
            )

            return redirect(url_for('add_product'))
        
        try:
            price = float(price)
        except ValueError:
            flash(
                "Price must be a Number",
                "danger"
            )
            return redirect(url_for('add_product'))
        
        if price <= 0:
            flash(
                "Price cant be Zero",
                "danger"
            )
            return redirect(url_for("add_product"))
        
        
        try:
            quantity = int(quantity)
        except ValueError:
            flash(
                "Quantity must be a Number",
                "danger"
            )
            return redirect(url_for('add_product'))
        
        if quantity <= 0:
            flash(
                "Quantity cant be Zero",
                "danger"
            )
            return redirect(url_for("add_product"))
        
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO PRODUCTS (PRODUCT_NAME,CATEGORY,PRICE,QUANTITY)
        VALUES (%s,%s,%s,%s)
        """

        values = (name,category,price,quantity)

        cursor.execute(query,values)
        conn.commit()
        conn.close()

        flash("Product Added Successfully!","success")
        return redirect(url_for('view_products'))

    except Exception as e:
        return f"Error when adding product :{e}"

@app.route('/products')
def view_products():
    search_query = request.args.get('search', '')

    conn = get_connection()
    cursor = conn.cursor()

    if search_query:

        query = """
        SELECT *
        FROM PRODUCTS
        WHERE
            product_name LIKE %s
            OR category LIKE %s
        """

        search_term = f"%{search_query}%"

        cursor.execute(
            query,
            (search_term, search_term)
        )

    else:

        cursor.execute(
            "SELECT * FROM PRODUCTS"
        )

    products = cursor.fetchall()

    conn.close()

    return render_template(
        'products.html',
        products=products,
        search_query=search_query
        )   

@app.route('/edit/<int:id>')
def edit_product(id):

    conn = get_connection()
    cursor = conn.cursor()

    query = '''
    SELECT * FROM PRODUCTS
    WHERE id =%s
    '''

    cursor.execute(query,(id,))

    product = cursor.fetchone()

    conn.close()

    return render_template('edit_product.html',product=product)

@app.route('/update/<int:id>',methods=["POST"])
def update_products(id):

    try:

        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']

        if not name.strip():

            flash(
                'Product name cant be empty',
                "danger"
            )

            return redirect(url_for('edit_product',id=id))
        
        try:
            price = float(price)
        except ValueError:
            flash(
                "Price must be a Number",
                "danger"
            )
            return redirect(url_for('edit_product',id=id))
        
        if price <= 0:
            flash(
                "Price cant be Zero",
                "danger"
            )
            return redirect(url_for("edit_product",id=id))
        
        
        try:
            quantity = int(quantity)
        except ValueError:
            flash(
                "Quantity must be a Number",
                "danger"
            )
            return redirect(url_for('edit_product',id=id))
        
        if quantity <= 0:
            flash(
                "Quantity cant be Zero",
                "danger"
            )
            return redirect(url_for("edit_product",id=id))

        conn = get_connection()
        cursor = conn.cursor()

        query = '''
        UPDATE PRODUCTS
        SET 
            product_name = %s,
            category = %s,
            price = %s,
            quantity = %s
        WHERE id = %s
        '''
        
        values = (name,category,price,quantity,id)

        cursor.execute(query,values)

        conn.commit()
        conn.close()

        flash("Product Updated Successfully!","success")
        return redirect(url_for('view_products'))

    except Exception as e:
        return f"Error Occured:{e}"


@app.route('/delete/<int:id>')
def delete_product(id):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = '''
        DELETE FROM PRODUCTS
        WHERE id = %s
        '''

        cursor.execute(query,(id,))

        conn.commit()
        conn.close()

        flash("Product Deleted Successfully!","danger")
        return redirect(url_for('view_products'))

    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('view_products'))


@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM PRODUCTS")

    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(QUANTITY) FROM PRODUCTS")

    total_stock = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(PRICE * QUANTITY) FROM PRODUCTS")

    inventory_value = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM PRODUCTS WHERE QUANTITY < 5")

    low_stock = cursor.fetchone()[0]

    cursor.execute(
    """
        SELECT *
        FROM PRODUCTS
        WHERE quantity < 5
    """
    )

    low_stock_products = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_quantity=total_stock,
        inventory_value=inventory_value,
        low_stock_count=low_stock,
        low_stock_products = low_stock_products
    )




if __name__ == "__main__":
    app.run(debug=True)

