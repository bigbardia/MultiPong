from multipong import create_app

app , socketio = create_app()

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)