# Vendors Management API's

## Set up

    1. git clone 

    2. pip venv env

    3. source env/Scripts/activate (activate environment)

    4. pip install -r requirement.txt

    5. cd vendorManagement

    6. python manage.py makemigrations

    7. python manage.py migrate


## DataBase Setup 

    Note : I have used localhost postgres. so please setup your own postgres or use default sqlite. before proceeding setup 

    Postgres DB Name = VendorsDB


## Vendor APIs 

    1. CreateVendor  (POST request)

        http://localhost:8000/api/v1/createvendor

        dataformat to post : 
                            {
                            "vendorName": "Prashant",
                            "vendorContact": "bhatt.prashant2000@gmail.com",
                            "address": "D23, Vakeel Sahib Appt, Ram Colony, Chattarpur, New Delhi",
                            "password": "password"
                            }

        Note : vendorContact is Email Field. So please put valid email

    2. Login Vendor (POST request)

        http://localhost:8000/api/v1/loginvendor

        data to post : 

                {
                    "vendorContact": "vishal.singh@gmail.com", 
                    "password": "password"
                }

    
    3. Update Vendor (Put Request)

        Note : You need token to make this request. Token will be get from login

        http://localhost:8000/api/v1/updatevendor/YOUR_vendor_id

        data : 
            {
                "vendorName": "Vishal", 
                "vendorContact": "vishal.singh@gmail.com", 
                "address": "D34, Vishal APPt. Sector 43, Gurugram", 
                "password": "password"
            }

    4. Get all Vendors (Get Request)
            Note : You need token to make this request. Token will be get from login

            http://localhost:8000/api/v1/getallvendors

    
    5. Get Vendor By Id (Get Request)

        Note : You need token to make this request. Token will be get from login

        http://localhost:8000/api/v1/getvendor/Your_vendorid

    
    6. Delete Vendor 
                Note : You need token to make this request. Token will be get from login
            http://localhost:8000/api/v1/deletevendor/Your_vendorid

    
    7. PurchaseOrder

        http://localhost:8000/api/v1/purchaseorder

        data_format : 
                    {
                        "vendor": "a45e71b2-8154-4378-b333-327471af1aaf",
                        "items": [
                                {"name": "Rice", "price": 100.99, "quantity": 2},
                                {"name": "Bread", "price": 99.99, "quantity": 1},
                                {"name": "Butter", "price": 99.99, "quantity": 1}
                            ],
                        "delivery_date": "2023-11-25"
                        }


    8. Get all Orders (Get Request)

            http://localhost:8000/api/v1/getallorders

    
    9. Get Order by Id (Get Request)

        http://localhost:8000/api/v1/getorder/Your_po_number


    10. Update Order (PUT Request)

        http://localhost:8000/api/v1/updateorder/your_po_number
        data : 
                {
                    "vendor": "a45e71b2-8154-4378-b333-327471af1aaf",
                    "items": [
                            {"name": "Rice", "price": 100.99, "quantity": 2},
                            {"name": "Bread", "price": 99.99, "quantity": 1},
                            {"name": "Butter", "price": 99.99, "quantity": 1}
                        ],
                    "delivery_date": "2023-11-25"
                }


    11. Delete Order (Delete Request)

        http://localhost:8000/api/v1/deleteorder/Your_po_number

    
    12. Order Status (Post Request)

        http://localhost:8000/api/v1/orderstatus/Your_po_number

        data : 
                {
                  "status": "completed"
                }


    13. Acknowledge Order (Post Request)

            http://localhost:8000/api/v1/acknowledgeorder/Your_po_number

        
    14. Quality Rating (Post Request)

        http://localhost:8000/api/v1/qualityrating/Your_po_number

        data : 
            {
             "quality_rating": 4
            }


    15. VendorPerformance (Get Request)
        
            http://localhost:8000/api/v1/vend_vendor_id

