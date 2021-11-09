from webtelnet import app

app.run(host="0.0.0.0", port=8080, workers=8, access_log=False)
