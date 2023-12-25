document.getElementById('key_word').addEventListener('input', function(event) {
    var keyword = event.target.value;
    if (keyword.trim() === '') {
        event.target.value = '请输入电影名称';
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/search?key_word=' + keyword, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var results = JSON.parse(xhr.responseText);
                // 更新下拉框内容
            }
        };
        xhr.send();
    }
});