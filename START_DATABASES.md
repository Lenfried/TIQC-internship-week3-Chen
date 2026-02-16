# Quick Start Guide - Starting Database Services

Both MySQL and MongoDB need to be running before you can use the application.

## Option 1: Start Services via Services Manager (GUI)

1. Press `Win + R` to open Run dialog
2. Type `services.msc` and press Enter
3. Find **MySQL** service
   - Right-click → **Start**
4. Find **MongoDB** service  
   - Right-click → **Start**

## Option 2: Start Services via PowerShell (Administrator)

Open PowerShell **as Administrator** and run:

```powershell
# Start MySQL
Start-Service MySQL

# Start MongoDB
Start-Service MongoDB

# Check status
Get-Service MySQL, MongoDB
```

## Option 3: If Databases Are Not Installed

### MySQL Installation Options:

**Option A: MySQL Community Server**
- Download: https://dev.mysql.com/downloads/mysql/
- Install MySQL Installer for Windows
- During installation, set root password
- Update `.env` file with your MySQL root password

**Option B: XAMPP (Easier for beginners)**
- Download: https://www.apachefriends.org/
- Install XAMPP (includes MySQL)
- Start MySQL from XAMPP Control Panel
- Default user: `root`, password: (empty)

### MongoDB Installation Options:

**Option A: MongoDB Community Server**
- Download: https://www.mongodb.com/try/download/community
- Install MongoDB Community Edition
- MongoDB runs as a Windows service automatically

**Option B: MongoDB Atlas (Cloud - No Installation)**
- Sign up: https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string
- Update `.env` file with Atlas connection details:
  ```
  MONGODB_HOST=your-cluster.mongodb.net
  MONGODB_PORT=27017
  ```

## Verify Services Are Running

Run the check script:
```bash
python check_databases.py
```

You should see:
```
[OK] MySQL is running on localhost:3306
[OK] MongoDB is running on localhost:27017
```

## Next Steps

Once both databases are running:

1. **Set up databases:**
   ```bash
   python setup_databases.py
   ```

2. **Add sample data (optional):**
   ```bash
   python seed_data.py
   ```

3. **Start the application:**
   ```bash
   python app.py
   ```

4. **Open browser:**
   ```
   http://localhost:5000
   ```

## Troubleshooting

### MySQL Service Not Found
- MySQL may not be installed
- Service name might be different (check in services.msc)
- Try: `Get-Service | Where-Object {$_.DisplayName -like "*MySQL*"}`

### MongoDB Service Not Found
- MongoDB may not be installed
- Service name might be different (check in services.msc)
- Try: `Get-Service | Where-Object {$_.DisplayName -like "*Mongo*"}`

### Port Already in Use
- Another application might be using the port
- Check: `netstat -ano | findstr :3306` (MySQL)
- Check: `netstat -ano | findstr :27017` (MongoDB)
