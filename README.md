## Introduction

This project is a Web API for an ecommerce application. It provides authentication, product listing and searching, ordering, and payments with paystack. A lot more is still to be added!

### Getting started
You can create a fork or clone this repo directly to download the code to your local repository

    git clone https://github.com/KeneNwogu/store
    cd store

#### Installation and Prerequisites
The following prerequisites are required to run the project locally:

 - Python
 - PostgreSQL
 -
	 #### Project dependencies: Before running the application, some project dependencies need to be installed and these are located in the requirements.txt file. To install each requirement, run:

	`pip install -r requirements.txt`

#### Environment Variables
The following environment variables are needed to properly run the application without any errors. These will be divided into sections to according to their purpose(s):

##### CLOUDINARY CONFIG VARIABLES:
These variables are necessary to setup cloudinary both locally and in production:

 1. CLOUDINARY_CLOUD_NAME
 2. CLOUDINARY_API_KEY
 3. CLOUDINARY_API_SECRET

 For more information about these variables, refer to the cloudinary documentation [here](https://cloudinary.com/documentation)

##### PAYSTACK KEYS

 1. PAYSTACK_SECRET_KEY
 2. PAYSTACK_PUBLIC_KEY

For more information about these variables, refer to the paystack documentation [here](https://paystack.com/docs/)