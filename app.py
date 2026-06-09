# app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import *

app = Flask(__name__)
CORS(app)

DATABASE_URL = "postgresql://neondb_owner:npg_ubcCS7d0YUnz@ep-fancy-meadow-apocfv7f.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

@app.route('/tenants', methods=['GET'])
def get_tenants():

    conn = engine.connect()

    result = conn.execute(
        text("SELECT * FROM tenants")
    )

    data = []

    for row in result:
        data.append({
            "id": row.id,
            "name": row.name,
            "phone": row.phone,
            "property_type": row.property_type,
            "property_number": row.property_number,
            "deposit": row.deposit,
            "deposit_mode": row.deposit_mode
        })

    conn.close()

    return jsonify(data)

@app.route('/tenants', methods=['POST'])
def add_tenant():

    data = request.json

    conn = engine.connect()

    conn.execute(
        text("""
        INSERT INTO tenants
        (
            name,
            phone,
            property_type,
            property_number,
            deposit,
            deposit_mode
        )
        VALUES
        (
            :name,
            :phone,
            :ptype,
            :pnumber,
            :deposit,
            :dmode
        )
        """),
        {
            "name": data["name"],
            "phone": data["phone"],
            "ptype": data["property_type"],
            "pnumber": data["property_number"],
            "deposit": data["deposit"],
            "dmode": data["deposit_mode"]
        }
    )

    conn.commit()

    conn.close()

    return jsonify({
        "success": True
    })


@app.route('/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):

    conn = engine.connect()

    conn.execute(
        text(
            "DELETE FROM tenants WHERE id=:id"
        ),
        {
            "id": id
        }
    )

    conn.commit()

    conn.close()

    return jsonify({
        "success": True
    })


@app.route('/rent', methods=['POST'])
def add_rent():

    data = request.json

    conn = engine.connect()

    conn.execute(
        text("""
        INSERT INTO rent
        (
            tenant_id,
            month,
            amount,
            transaction_id,
            payment_mode
        )
        VALUES
        (
            :tenant,
            :month,
            :amount,
            :txn,
            :mode
        )
        """),
        {
            "tenant": data["tenant_id"],
            "month": data["month"],
            "amount": data["amount"],
            "txn": data["transaction_id"],
            "mode": data["payment_mode"]
        }
    )

    conn.commit()

    conn.close()

    return jsonify({
        "success": True
    })


@app.route('/rent/<int:tenant_id>')
def rent_history(tenant_id):

    conn = engine.connect()

    result = conn.execute(
        text(
            "SELECT * FROM rent WHERE tenant_id=:id"
        ),
        {
            "id": tenant_id
        }
    )

    data = []

    for row in result:
        data.append({
            "month": row.month,
            "amount": row.amount,
            "transaction": row.transaction_id,
            "mode": row.payment_mode
        })

    conn.close()

    return jsonify(data)

@app.route('/stats')
def stats():

    conn = engine.connect()

    tenants = conn.execute(
        text(
            "SELECT COUNT(*) FROM tenants"
        )
    ).scalar()

    rent = conn.execute(
        text(
            "SELECT COALESCE(SUM(amount),0) FROM rent"
        )
    ).scalar()

    conn.close()

    return jsonify({
        "tenants": tenants,
        "rent": rent
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )