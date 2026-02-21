from app import create_app

# Created at module level so production servers (e.g. Gunicorn) can import it:
#   gunicorn run:app
app = create_app()

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
