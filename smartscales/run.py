from app import app, socketio, cli

if __name__ == '__main__':
    # socketio.run(app=app, host='0.0.0.0', debug=True)
    # 这里不要用 debug 模式这会使启动时 启动两次，这样会使程序保存，因为在TensorFlow-GPU第一次加载了显存，
    # 第二次就不能分配到显存就会报错
    # 当调用app.run()的时候，用到了Werkzeug库，它会生成一个子进程，当代码有变动的时候它会自动重启
    # 如果在run（）里加入参数 use_reloader=False，就会取消这个功能，当然，在以后的代码改动后也不会自动更新了。
    # 可以查看WERKZEUG_RUN_MAIN环境变量， 默认情况下，调用子程序时，它会被设置为True
    # WERKZEUG_RUN_MAIN = False
    socketio.run(app=app, host='0.0.0.0', port='5000')
    # app.run(host='0.0.0.0', port='8888')  # 调试模式
