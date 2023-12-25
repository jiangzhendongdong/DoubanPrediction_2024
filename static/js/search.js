document.getElementById('key_word').addEventListener('input', function(event) {
    // 获取输入框的值
    var keyword = event.target.value;
    // 判断输入框是否为空
    if (keyword.trim() === '') {
        // 如果为空，则将输入框的值设置为提示信息
        event.target.value = '请输入电影名称';
    } else {
        // 如果不为空，则发送ajax请求
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/search?key_word=' + keyword, true);
        xhr.onreadystatechange = function() {
            // 当ajax请求状态为4且状态码为200时，表示请求成功
            if (xhr.readyState === 4 && xhr.status === 200) {
                // 解析ajax请求返回的数据
                var results = JSON.parse(xhr.responseText);
                // 更新下拉框内容
                var selectElement = document.getElementById('movie_list');
                selectElement.innerHTML = "";
                // 遍历ajax请求返回的数据，创建option元素，添加到下拉框中
                for (var i = 0; i < results.length; i++) {
                    var optionElement = document.createElement("option");
                    optionElement.value = results[i].id;
                    optionElement.text = results[i].movie;
                    selectElement.appendChild(optionElement);
                }
            }
        };
        xhr.send();
    }
});
