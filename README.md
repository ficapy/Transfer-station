# Transfer-station
- 类rapidleech,提供youtube&amp;普通链接中转下载,基于twisted&amp;autobahn
- 还有诸多细节需要修改，前端UI照搬[youtube-download-flask](https://github.com/damiencorpataux/youtube-download-flask)
		#使用如下
        sudo apt-get update
        sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip
        pip install crossbar
        pip install crossbar[all]
        --------------------------以上为最简环境配置
        crossbar start
        python control.py