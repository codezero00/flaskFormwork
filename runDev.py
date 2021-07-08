from server import create_app


app = create_app(None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True, threaded=True)