## 在原有基础上进行了小幅度的改动， 增加了对红外接收模块、DHT11、WS2812、LCD屏幕、NFC模块的读写

### 配置方法（电脑或树莓派已安装好python环境）

* **配置 python 的依赖环境**
	 * **windows环境下**- 将 pymata-aio-2.19.tar.gz 解压，以被解压的文件夹的路径打开命令行，运行里面的setup.py文件。
		  * **运行命令** >>>python setup.py
	 * **linux环境下**- 将 pymata-aio-2.19.tar.gz 解压，以被解压的文件夹的路径打开命令行，运行里面的setup.py文件。
		  * **运行命令** $tar -zxvf pymata-aio-2.19.tar.gz
		  * **运行命令** $python3 setup.py install
* **配置 Arduino SDK 环境**
	 * 将 Firmata 目录全部替换 Arduino 安装包中的 libraries\Firmata 目录
* 选择 leonardo 主控板，选择 LP_Firmata 例程，编译上传
* 运行examples中的例程
	 * 对 leonardo 主控板，红外接收模块只能接在数字引脚0、1、2、3、7。
	 * 对 leonardo 主控板，由于内限制，最多同时支持两条灯带。
	 * 由于 firmata 协议通过串口传输，传输速度有限，命令在执行时都会有短暂延迟。
