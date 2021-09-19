Requirement for this project for setup:

-> Create a vitual environment.
== virtualenv -p python3.6 venv
-> Activate your virtual environment using this command
== source venv/bin/activate
-> Install required python libraries by using pip installer.
== pip install -r requirements.txt
-> Migrate database.
== python manage.py migrate
-> Finally, run your django runserver.
== python manage.py runserver


# Post API 1 endpoint that allows us to register.
request
{
    "username": "ankur1",
    "password": "root"
}
response
{
"id": 29,
"username": "ankur1"
}
Ex- http://localhost:8000/users/

# GET API 2 endpoint to render product list.
response
[
    {
        "id": 4,
        "product_name": "Chocklate Cake",
        "author": "Ankur",
        "marked price": 220.0,
        "product_ingredients": [
            {
                "material_name": "Milk",
                "material_quantity_used": 10.0
            },
            {
                "material_name": "Choclate",
                "material_quantity_used": 10.0
            }
        ]
    },
    {
        "id": 5,
        "product_name": "Curd",
        "author": "Ankur",
        "marked price": 52.0,
        "product_ingredients": [
            {
                "material_name": "Milk",
                "material_quantity_used": 5.0
            }
        ]
    }
]
Ex- http://localhost:8000/product/

# Post API 3 endpoint that renders order history.
response
[
    [
        {
            "discount %": 10,
            "final_price": 53.1,
            "marked price": 59.0,
            "product_name": "Curd"
        },
        {
            "discount %": 5,
            "final_price": 209.0,
            "marked price": 220.0,
            "product_name": "Chocklate Cake"
        }
    ],
    [
        {
            "discount %": 5,
            "final_price": 209.0,
            "marked price": 220.0,
            "product_name": "Chocklate Cake"
        }
    ]
]
Ex- http://localhost:8000/history/

# Post API 4 endpoint that renders sales report given datetime wise.
request 
{
    "start_date": "2020-10-01",
    "end_date": "2020-12-31"
}
response
{
    "total_earnings": 471.1,
    "most_selling_product": "Chocklate Cake",
    "total_earning_most_selling_product": 209.0,
    "least_selling_product": "Curd",
    "total_earning_least_selling_product": 53.1
}
Ex- http://localhost:8000/sales_report/
