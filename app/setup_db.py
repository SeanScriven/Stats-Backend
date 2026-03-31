from database import get_db, init_db

if __name__ == "__main__":
    conn = get_db()
    init_db(conn)
    conn.close()
    print("Setup complete. You can now run main.py")