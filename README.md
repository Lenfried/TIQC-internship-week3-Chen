# TIQC-internship-week3-Chen
# Graphics Cards Database Dashboard

A web application that demonstrates CRUD operations on graphics cards data using both **MySQL (SQL)** and **MongoDB (NoSQL)** databases. For a graphics card inventory database, such as one used in an online storefront, MySQL is the better choice due to the structured nature of the data, data accuracy, and complex querying.

## Features

- ✅ **Dual Database Support**: Store and manage data in both MySQL and MongoDB
- ✅ **Full CRUD Operations**: Create, Read, Update, and Delete graphics cards
- ✅ **Modern Dashboard**: Beautiful web interface with tabs for each database
- ✅ **Real-time Comparison**: See how SQL and NoSQL handle the same data differently
- ✅ **Sample Data**: Pre-configured seed script with sample graphics cards

## Project Structure

```
.
├── app.py                 # Flask backend application
├── config.py              # Database configuration
├── mysql_db.py            # MySQL database operations
├── mongodb_db.py          # MongoDB database operations
├── seed_data.py           # Script to populate sample data
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── templates/
│   └── dashboard.html     # Frontend HTML
└── static/
    ├── style.css          # CSS styling
    └── script.js          # Frontend JavaScript
```

## Prerequisites

- Python 3.8 or higher
- MySQL Server (running and accessible)
- MongoDB Server (running and accessible)

**Quick Check**: Run `python check_databases.py` to verify if your databases are running.
If not, see `START_DATABASES.md` for detailed setup instructions.

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update the database connection details:
     ```env
     MYSQL_HOST=localhost
     MYSQL_PORT=3306
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     MYSQL_DATABASE=graphics_cards_db
     
     MONGODB_HOST=localhost
     MONGODB_PORT=27017
     MONGODB_DATABASE=graphics_cards_db
     ```

4. **Start database services**:
   - Check if databases are running: `python check_databases.py`
   - If not running, see `START_DATABASES.md` for instructions
   - Or use PowerShell (as Administrator): `.\start_services.ps1`

5. **Set up databases**:
   ```bash
   python setup_databases.py
   ```
   This script will create the MySQL database and verify MongoDB connection. 
   Alternatively, the application will attempt to create the MySQL database automatically on first run.
   
6. **MongoDB Setup**:
   - Ensure MongoDB is running
   - The application will automatically create the collection and indexes on first run

## Usage

1. **Seed sample data** (optional):
   ```bash
   python seed_data.py
   ```
   This will populate both databases with sample graphics cards.

2. **Start the Flask application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

4. **Use the dashboard**:
   - Switch between MySQL and MongoDB tabs to see data from each database
   - Click "Add New Card" to create a new graphics card entry
   - Click "Edit" on any card to modify its details
   - Click "Delete" to remove a card
   - Click "Refresh" to reload the data

## API Endpoints

### MySQL Endpoints
- `GET /api/mysql/cards` - Get all cards
- `POST /api/mysql/cards` - Create a new card
- `PUT /api/mysql/cards/<id>` - Update a card
- `DELETE /api/mysql/cards/<id>` - Delete a card

### MongoDB Endpoints
- `GET /api/mongodb/cards` - Get all cards
- `POST /api/mongodb/cards` - Create a new card
- `PUT /api/mongodb/cards/<id>` - Update a card
- `DELETE /api/mongodb/cards/<id>` - Delete a card

## Database Schema

### MySQL Schema
The `graphics_cards` table includes:
- `id` (INT, Primary Key, Auto Increment)
- `name` (VARCHAR)
- `manufacturer` (VARCHAR)
- `model` (VARCHAR)
- `memory_gb` (INT)
- `memory_type` (VARCHAR)
- `core_clock_mhz` (INT)
- `boost_clock_mhz` (INT, nullable)
- `price_usd` (DECIMAL, nullable)
- `release_date` (DATE, nullable)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)
- Indexes on: manufacturer, memory_gb, price_usd

### MongoDB Schema
The `graphics_cards` collection stores documents with:
- `_id` (ObjectId, auto-generated)
- Same fields as MySQL (but flexible schema)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- Indexes on: manufacturer, memory_gb, price_usd, name

## Key Differences: SQL vs NoSQL

### MySQL (SQL)
- **Structured Schema**: Fixed table structure with defined columns
- **Relationships**: Supports foreign keys and joins
- **ACID Compliance**: Ensures data integrity
- **ID Generation**: Auto-incrementing integer IDs
- **Data Types**: Strict typing (INT, VARCHAR, DECIMAL, DATE)

### MongoDB (NoSQL)
- **Flexible Schema**: Documents can have varying structures
- **Document-Based**: Stores data as JSON-like documents
- **Scalability**: Better horizontal scaling
- **ID Generation**: ObjectId (12-byte identifier)
- **Data Types**: More flexible, stores native JSON types

## Technologies Used

- **Backend**: Flask (Python)
- **Databases**: MySQL, MongoDB
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database Drivers**: PyMySQL, PyMongo

## Troubleshooting

### MySQL Connection Issues
- Verify MySQL is running: `mysql -u root -p`
- Check credentials in `.env` file
- Ensure database exists: `CREATE DATABASE graphics_cards_db;`

### MongoDB Connection Issues
- Verify MongoDB is running: `mongosh` or check service status
- Check MongoDB port (default: 27017)
- Ensure MongoDB is accessible from your application

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`

## License

This project is created for educational purposes to demonstrate SQL vs NoSQL database operations.
