import pymysql
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

class MySQLDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Connected to MySQL database: {MYSQL_DATABASE}")
        except pymysql.Error as e:
            # If database doesn't exist, try to create it
            if "Unknown database" in str(e) or 1049 in str(e):
                print(f"Database '{MYSQL_DATABASE}' not found. Attempting to create it...")
                try:
                    # Connect without database
                    temp_conn = pymysql.connect(
                        host=MYSQL_HOST,
                        port=MYSQL_PORT,
                        user=MYSQL_USER,
                        password=MYSQL_PASSWORD,
                        charset='utf8mb4'
                    )
                    with temp_conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                        temp_conn.commit()
                    temp_conn.close()
                    print(f"Database '{MYSQL_DATABASE}' created successfully")
                    # Retry connection
                    self.connection = pymysql.connect(
                        host=MYSQL_HOST,
                        port=MYSQL_PORT,
                        user=MYSQL_USER,
                        password=MYSQL_PASSWORD,
                        database=MYSQL_DATABASE,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor
                    )
                    print(f"Connected to MySQL database: {MYSQL_DATABASE}")
                except Exception as create_error:
                    print(f"Error creating database: {create_error}")
                    print("Please run 'python setup_databases.py' first or create the database manually")
                    raise
            else:
                print(f"Error connecting to MySQL: {e}")
                raise
    
    def create_table(self):
        """Create graphics_cards table if it doesn't exist"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS graphics_cards (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        manufacturer VARCHAR(100) NOT NULL,
                        model VARCHAR(100) NOT NULL,
                        memory_gb INT NOT NULL,
                        memory_type VARCHAR(50) NOT NULL,
                        core_clock_mhz INT NOT NULL,
                        boost_clock_mhz INT,
                        price_usd DECIMAL(10, 2),
                        release_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_manufacturer (manufacturer),
                        INDEX idx_memory (memory_gb),
                        INDEX idx_price (price_usd)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                self.connection.commit()
                print("MySQL table 'graphics_cards' created/verified successfully")
        except pymysql.Error as e:
            print(f"Error creating table: {e}")
            raise
    
    def create(self, data):
        """Create a new graphics card entry"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO graphics_cards 
                    (name, manufacturer, model, memory_gb, memory_type, core_clock_mhz, boost_clock_mhz, price_usd, release_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data['name'],
                    data['manufacturer'],
                    data['model'],
                    data['memory_gb'],
                    data['memory_type'],
                    data['core_clock_mhz'],
                    data.get('boost_clock_mhz'),
                    data.get('price_usd'),
                    data.get('release_date')
                ))
                self.connection.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Error creating record: {e}")
            raise
    
    def read_all(self, filters=None):
        """Read graphics cards with optional search and filters.
        filters: dict with optional keys: search, manufacturer, memory_type,
                 memory_min, memory_max, price_min, price_max
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM graphics_cards WHERE 1=1"
                values = []
                if filters:
                    if filters.get('search'):
                        sql += " AND (name LIKE %s OR manufacturer LIKE %s OR model LIKE %s)"
                        term = f"%{filters['search']}%"
                        values.extend([term, term, term])
                    if filters.get('manufacturer'):
                        sql += " AND manufacturer = %s"
                        values.append(filters['manufacturer'])
                    if filters.get('memory_type'):
                        sql += " AND memory_type = %s"
                        values.append(filters['memory_type'])
                    if filters.get('memory_min') is not None:
                        sql += " AND memory_gb >= %s"
                        values.append(int(filters['memory_min']))
                    if filters.get('memory_max') is not None:
                        sql += " AND memory_gb <= %s"
                        values.append(int(filters['memory_max']))
                    if filters.get('price_min') is not None:
                        sql += " AND (price_usd IS NULL OR price_usd >= %s)"
                        values.append(float(filters['price_min']))
                    if filters.get('price_max') is not None:
                        sql += " AND (price_usd IS NULL OR price_usd <= %s)"
                        values.append(float(filters['price_max']))
                sql += " ORDER BY id DESC"
                cursor.execute(sql, values or None)
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error reading records: {e}")
            raise
    
    def read_one(self, card_id):
        """Read a single graphics card by ID"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM graphics_cards WHERE id = %s", (card_id,))
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error reading record: {e}")
            raise
    
    def update(self, card_id, data):
        """Update a graphics card entry"""
        try:
            with self.connection.cursor() as cursor:
                # Build dynamic update query
                fields = []
                values = []
                for key, value in data.items():
                    if value is not None:
                        fields.append(f"{key} = %s")
                        values.append(value)
                
                if not fields:
                    return False
                
                values.append(card_id)
                sql = f"UPDATE graphics_cards SET {', '.join(fields)} WHERE id = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Error updating record: {e}")
            raise
    
    def delete(self, card_id):
        """Delete a graphics card entry"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM graphics_cards WHERE id = %s", (card_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f"Error deleting record: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("MySQL connection closed")
