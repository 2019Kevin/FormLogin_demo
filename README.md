# 模拟登陆知乎网站和校园网站查询成绩



## 主要用到的模块知识及其要点
> * requests模块的sesssion构造浏览器登陆成功后需要提交的表单,用保存了cookie信息的session来访问主页；
> * lxml.html模块和BeautifulSoup解析网页中的信息；
> * 通过谷歌浏览器里面的检查里面的network按F5来找到验证码的url地址，通过datatime.datetime模块构造变化的url地址将图片下载到本地，手动输入验证码。
> * 通过访问主页的内容及登陆成功才能访问的网页内容判断是否登陆成功。


