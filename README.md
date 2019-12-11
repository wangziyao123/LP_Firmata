1. 配置 python 的依赖环境
	将python3.7_lib里边的库放到python3.7的安装目录的 \Lib\site-packages 子目录下。
	如果不清楚 python 三方库的目录路径，可以在命令行中，导入 sys 模块，运行 
	print(sys.path), 后可以在打印的列表中找到该路径。
2. 配置 Arduino SDK 环境
	将 github 上下载的 Firmata 目录替换 Arduino 安装包中的 libraries\Firmata 目录
3. 选择leonardo，选择LP_Firmata例程，编译上传
4. 运行examples中的例程，目前已经支持标准读写和 红外 NFC WS2812 DHT11 SSD1306
