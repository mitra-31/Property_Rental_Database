from app import app




if __name__ == "__main__":
    app.secret_key = "12345"
    app.run(debug=True)