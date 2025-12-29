# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Run the Application
```bash
python main.py
```

### Code Formatting & Linting
The project uses **Ruff** (replaces Black) and **pyrefly** (replaces pylint) for code quality:
```bash
# Format code with Ruff
ruff format .

# Lint with pyrefly
pyrefly
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest test/test_file.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=backend
```

### Database Setup
The project uses MySQL database named `TextbookOrder` with the following credentials:
- Host: localhost
- Port: 3306
- User: root
- Password: root
- Database: TextbookOrder

Database schema files are in `/database/`:
- `ddl.sql` - Table definitions
- `view.sql` - Database views
- `routines.sql` - Stored procedures
- `test_data.sql` - Test data

## High-Level Architecture

### Project Structure
```
book-ordering-system/
├── main.py                 # Application entry point
├── backend/                # Backend logic
│   ├── login_window.py     # Login window controller
│   ├── a_main_window.py    # Admin main window controller
│   ├── s_main_window.py    # Student main window controller
│   └── db_utils.py         # Database utilities (CRUD operations)
├── frontend/               # UI components (Qt Designer .py files)
│   ├── LonginUI.py         # Login window UI
│   ├── AMainWindow.py      # Admin window UI
│   └── SMainWindow.py      # Student window UI
├── database/               # Database schema and data
│   ├── ddl.sql
│   ├── view.sql
│   ├── routines.sql
│   └── test_data.sql
└── requirements.txt        # Python dependencies
```

### Technology Stack
- **Frontend**: PyQt5 (Qt5 for Python)
- **Backend**: Python 3
- **Database**: MySQL with PyMySQL connector
- **Data Processing**: pandas
- **Testing**: pytest
- **Code Quality**: Ruff (formatting) + pyrefly (linting)

### Application Architecture (MVC Pattern)

**Model (backend/db_utils.py)**:
- Database connection management
- CRUD operations for all entities (Administrator, Student, Textbook, Order)
- Data export to CSV using pandas
- Database backup/recovery utilities
- Stored procedure calls for complex queries

**View (frontend/*.py)**:
- Qt UI definitions generated from Qt Designer
- Handles all visual presentation
- Contains stacked widgets for different views

**Controller**:
- **LoginWindow** (backend/login_window.py): Handles authentication for both admin and student roles
- **AMainWindow** (backend/a_main_window.py): Admin functionality - query by college/major, export data, backup/recover, update password
- **SMainWindow** (backend/s_main_window.py): Student functionality - browse textbooks, place orders, view orders, update password

### Database Schema

**Core Tables**:
- `Administrator`: Admin accounts (AdminID, Name, ContactInfo, Username, Password)
- `Student`: Student accounts (StudentID, StudentName, MajorID, ContactInfo, StudentUsername, StudentPassword)
- `College`: College information (CollegeID, CollegeName)
- `Major`: Major information (MajorID, MajorName, CollegeID)
- `Textbook`: Textbook catalog (TextbookID, TextbookName, Author, Publisher, Price, MajorID)
- `Order`: Order records (OrderID, StudentID, TextbookID, Time)
- `order_log`: Order change logging

**Views**:
- `student_order_view`: Joins Student, Order, Textbook, Major, and College tables for comprehensive order data

**Stored Procedures**:
- `pCollege(college_id)`: Get textbook order counts by college
- `pMajor(major_id)`: Get textbook order counts by major
- `pOderBook()`: Get all textbook order counts
- `log_order_changes(action, order_id)`: Log order modifications

### User Roles & Features

**Student Features**:
1. Browse available textbooks
2. Place orders for textbooks
3. View personal order history
4. Update own password

**Admin Features**:
1. View order statistics by college (enter CollegeID)
2. View order statistics by major (enter MajorID)
3. View all textbook order counts
4. Export order data to CSV (/Users/liang/Downloads/data_Order_Book.csv)
5. Backup database to SQL file
6. Restore database from SQL file
7. Update own password

## Development Notes

### Database Credentials
Hardcoded in `backend/db_utils.py:7-13`. Database connection uses:
- host: "localhost"
- port: 3306
- user: "root"
- password: "root"
- database: "TextbookOrder"

### Code Quality Tools Location
- Ruff: `.venv/bin/ruff`
- pyrefly: `.venv/bin/pyrefly`
- Both are pre-installed in the project virtual environment

### Virtual Environment
Project uses `.venv/` for Python dependencies (excluded from git per .gitignore)

### Key Implementation Details

**Login Flow** (backend/login_window.py):
- LoginWindow uses stacked widgets to toggle between student/admin login
- Credentials validated against database via `get_admin_credentials()` and `get_student_credentials()`
- Successful login opens appropriate main window and closes login window

**Data Display**:
- All tables use QStandardItemModel with QTableView
- Headers configured with QHeaderView.Stretch for responsive layout

**Password Updates**:
- Both admin and student can update passwords via database UPDATE queries
- Passwords stored as plain text (no hashing visible)

**Export Functionality** (get_book_orders_out in db_utils.py):
- Uses pandas DataFrame to export to CSV
- Fixed export path: `/Users/liang/Downloads/data_Order_Book.csv`
- Encoding: utf-8-sig

**Database Backup/Recovery**:
- backup_database(): Uses mysqldump command
- recover_database(): Uses mysql command
- Both require system access to MySQL command-line tools

### Security Considerations
- SQL injection vulnerabilities present in `db_utils.py` (string formatting in queries at lines 55, 70, 146-147)
- Plain text password storage in database
- Hardcoded database credentials in source code
- No input validation visible on user inputs

### Known Issues & TODOs
From README.md Tasks section:
- [ ] pytest unit tests (not yet implemented)
- [ ] Test user experience
- [ ] Adjust and optimize application
- [ ] PyInstaller packaging
