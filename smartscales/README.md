# 智能秤 - Flask

## 安装所需要的包  
在PyCharm的Terminal里执行下面的命令  
<code> 

    pip install -r requirements.txt  
</code>
导出该项目安装的包  
<code> 

    pip freeze > requirements.txt
</code>


<code>

    {% block styles %} {# 样式块 #}
        {{ super() }}
        <link rel="stylesheet" href="{{ url_for('static',filename='css/style.css') }}">{# 下面的这种方式加载 css也是可以的 #}
        {#    <link rel="stylesheet" type="text/css" href="../static/css/style.css">#}
    {% endblock %}
</code>

flask translate init LANG用于添加新语言  
flask translate update用于更新所有语言存储库  
flask translate compile用于编译所有语言存储库  