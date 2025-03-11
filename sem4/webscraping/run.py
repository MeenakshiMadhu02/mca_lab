from scraper_app.routes import app



if __name__ == '__main__':
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule}: {rule.endpoint}")
    app.run(debug=True, port=5000)

    