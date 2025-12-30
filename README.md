# 🛒 NeoMart – Online Shopping Web Application

**NeoMart** is a web-based e-commerce application developed using **Python Flask** and **MongoDB**.  
The system allows users to browse products, manage cart and wishlist, place orders, and track order status.  
Administrators can manage products, control inventory, and monitor customer orders through a dedicated dashboard.

This project is developed for **academic purposes** and is ideal for beginners to understand full-stack web application development.

---

## 🚀 Features

### 👤 User Features
- User Registration and Login
- Forgot Password and Reset Password
- Browse Products by Category
- Add Products to Cart
- Wishlist Management
- Place Orders
- View Order History
- Track Order Status (Placed, Approved, Shipped, Delivered)

### 🛠 Admin Features
- Admin Login
- Add / Edit / Delete Products
- Stock Management
- Hide / Show Products
- Low Stock Alerts
- View All Orders
- Update Order Status
- Export Orders as CSV File

---

## 🧰 Technologies Used

- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask Framework)  
- **Database:** MongoDB (NoSQL)  
- **Authentication:** bcrypt (Password Hashing)  
- **Tools:**
  - Visual Studio Code
  - MongoDB Compass
  - Web Browser (Chrome / Edge / Firefox)

---

## 💻 Hardware Requirements

### Minimum Requirements
- Processor: Intel Core i3 or equivalent
- RAM: 4 GB
- Storage: 5 GB free disk space
- Display: 1366 × 768 resolution
- Keyboard and Mouse

### Recommended Requirements
- Processor: Intel Core i5 or higher
- RAM: 8 GB
- Storage: 10 GB free disk space (SSD preferred)

> Hardware details can be checked via:  
> **This PC → Properties** or **Settings → System → About**

---

## 🧪 Software Requirements

- Operating System:
  - Windows 10 / 11
  - Linux (Ubuntu 20.04 or above)
- Python Version: 3.10 or higher
- Database: MongoDB Community Edition
- Web Browser: Chrome / Edge / Firefox
- Code Editor: Visual Studio Code (optional)

---

## 📦 Python Libraries Used

- flask
- pymongo
- bcrypt
- python-dotenv (optional)

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## 🗄 Database Details

- Database Type: NoSQL
- Database Name: neomart
- Database Server: MongoDB (Localhost)
- Default Port: 27017

▶️ Project Execution Steps (Beginner Friendly)

**Step 1: Install Python**

Download Python from https://www.python.org

During installation, enable “Add Python to PATH”

Verify installation:
```bash
python --version
```

**Step 2: Install MongoDB**

Download MongoDB Community Edition from https://www.mongodb.com

Install MongoDB Compass (recommended)

Start MongoDB service:
```bash
mongod
```

**Step 3: Copy Project Folder**

Copy the NeoMart project folder

Paste it into Desktop or any preferred directory

**Step 4: Install Dependencies**

Open terminal or command prompt inside the project folder:
```bash
pip install -r requirements.txt
```

**Step 5: Run the Application**
```bash
python app.py
```

**Step 6: Open in Browser**

Open the following URL:
```bash
http://127.0.0.1:5000
```

👥 User Roles

**Admin**
- Manage products
- Control inventory
- Update order status
- Export order reports

**User**
- Register and login
- Browse products
- Add items to cart and wishlist
- Place and track orders

📂 Project Folder Structure

```
NeoMart/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── mongo.py
│
├── routes/
│   ├── auth.py
│   ├── admin.py
│   ├── cart.py
│   ├── wishlist.py
│   └── orders.py
│
├── templates/
│   ├── auth/
│   ├── admin/
│   └── user/
│
└── static/
    ├── css/
    └── uploads/
```

⚠ Common Errors and Solutions

❌ MongoDB connection failed

Solution:
Ensure MongoDB service is running.

❌ Module not found

Solution:
Install dependencies:
```bash
pip install -r requirements.txt
```

❌ Page not loading

Solution:
Ensure app.py is running and the correct URL is used.

📄 License

This project is developed strictly for academic and educational purposes.

✅ Conclusion

NeoMart is a complete, beginner-friendly full-stack web application demonstrating real-world e-commerce functionality using Flask and MongoDB.
