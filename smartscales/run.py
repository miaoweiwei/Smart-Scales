from app import app, socketio, cli

if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', debug=True)
    # app.run(debug=True)  # 调试模式
