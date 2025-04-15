#!/bin/bash

# 测试健康检查端点
echo "测试健康检查端点..."
curl -s http://localhost:5556/api/health

# 测试Markdown转换端点
echo -e "\n测试Markdown转换端点..."
curl -X POST \
  -H "Content-Type: application/json" \
  --max-time 600 \
  -d '{
    "markdown": "# MD2Card\n\n> MD2Card 是一个 markdown 转知识卡片工具，可以让你用 Markdown 制作优雅的图文海报。 🌟\n\n![](https://picsum.photos/600/300)\n\n\n## 它的主要功能：\n\n1. 将 Markdown 转化为**图文海报**\n2. 多种主题风格任你选择\n3. 长文自动拆分，或者根据 markdown `---` 横线拆分\n4. 可以复制图片到`剪贴板`，或者下载为`PNG`、`SVG`图片\n5. 所见即所得",
    "style": {
      "theme": "dark",
      "fontSize": 18,
      "width": 720,
      "height":1000
    }
  }' \
  http://localhost:5556/api/convert | tee ../temp/response.json

# 检查是否成功
if grep -q '"success":true' ../temp/response.json; then
  echo -e "\nAPI调用成功!"
  
  # 提取图片数据并保存
  echo -e "正在提取图片数据..."
  grep -o '"image":"[^"]*"' ../temp/response.json | sed 's/"image":"//;s/"$//' > ../temp/image_base64.txt
  cat ../temp/image_base64.txt | base64 -d > ../temp/output.png
  echo "图片已保存为 ../temp/output.png"
else
  echo -e "\nAPI调用失败，内容如下:"
  cat ../temp/response.json
fi