from walleapi import app

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=18000)
