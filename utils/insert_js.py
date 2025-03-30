def insert_js_to_html(html_file_path):
    # 定义要插入的 JS 代码
    js_code = """
    <script>
        // 尝试从 localStorage 中获取 ALLURE_REPORT_SETTINGS 的值
        let allureSettings = JSON.parse(localStorage.getItem('ALLURE_REPORT_SETTINGS'));

        if (allureSettings) {
            // 如果能获取到值，则修改 language 属性为 "zh"
            allureSettings.language = "zh";
        } else {
            // 如果获取不到值，则创建一个新对象并设置默认值
            allureSettings = {
                "language": "zh",
                "sidebarCollapsed": false,
                "sideBySidePosition": [46.83064516129034, 53.16935483870967]
            };
        }

        // 将修改后的对象或新创建的对象存储回 localStorage
        localStorage.setItem('ALLURE_REPORT_SETTINGS', JSON.stringify(allureSettings));

        console.log("当前设置", JSON.stringify(allureSettings));
    </script>
    """

    # 读取 HTML 文件内容
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找 </head> 标签位置（通常是最佳插入位置）
    head_end_index = content.find('</head>')

    if head_end_index != -1:
        # 在 </head> 前插入 JS 代码
        new_content = content[:head_end_index] + js_code + content[head_end_index:]
    else:
        # 如果没有找到 </head>，则在 <body> 开始标签后插入
        body_start_index = content.find('<body>')
        if body_start_index != -1:
            new_content = content[:body_start_index + 6] + js_code + content[body_start_index + 6:]
        else:
            # 如果都没有，则在文件末尾插入
            new_content = content + js_code

    # 写回文件
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

