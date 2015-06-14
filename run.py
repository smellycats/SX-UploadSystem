from upload import debug_logging, online_logging, app

if __name__ == '__main__':
    debug_logging('log\upload.log')
    app.run(port=8019, threaded=True)
