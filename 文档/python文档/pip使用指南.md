#升级pip
python -m pip install --upgrade pip


#查询
pip list																查看已安装包列表
pip search pkg															从pypi上搜索软件包
pip show pkg															查看软件包的详情
pip list --outdated														查看可升级软件包


#下载
pip download pkg														下载软件包
pip wheel --wheel-dir=/local/wheels -r requirements.txt					下载并构建软件包
pip download --destination-directory /local/wheels -r requirements.txt	从requirements.txt中下载软件包


#安装
pip install <pkg1 pkg2 ...>												安装最新版本包
pip install --no-index --find-links=/local/wheels pkg					从本地安装包，而不从pypi安装
pip install pkg==2.1.2													所安装的包的版本为2.1.2
pip install pkg>=2.1.2													所安装的包的版本必须大于等于2.1.2
pip install pkg<=2.1.2													所安装的包的版本必须小于等于2.1.2
pip install -r requirements.txt											从依赖包列表中安装
pip install -c constraints.txt											确保当前环境软件包的版本（并不确保安装）
pip install pkg --no-binary												限制不从wheel安装
pip install --user pkg													仅在当前用户环境中安装软件
pip install pkg --proxy [user:passwd@]proxy.server:port					使用代理服务器转发


#卸载
pip uninstall <pkg1 pkg2 ...>											卸载软件包


#升级
pip install --upgrade <pkg>												升级软件包


#其他
pip freeze >requirements.txt											导出依赖包列表
python -m pip <arguments>												使用pip安装软件包
python3 -m pip3 <arguments>												使用pip3安装软件包
py -m pip <arguments>													仅在windows上有效