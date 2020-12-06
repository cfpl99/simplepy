import os
def main():
    url=input('输入网址：\n')
    n=int(input('输入数字：\n1、查看格式\n2、调用播放器在线播放\n3、下载（默认最高画质）\n4、选择画质下载\n5、获取真实地址（Real URLs:后面的地址）\n'))
    savepath='D:\you get'#这里更改下载路径
    playerpath="'C:\Program Files (x86)\Windows Media Player\wmplayer.exe'"#这里更改播放器路径，这里调用的是Windows Media Player
    if n==1:
        cmd=r'you-get -i "%s"'%url
        os.system(cmd)
    elif n==2:
        cmd=r'you-get -p "%s" "%s"'%(playerpath,url)
        os.system(cmd)
    elif n==3:
        cmd=r'you-get -o "%s" "%s"'%(savepath,url)
        os.system(cmd)
    elif n==4:
        cmd=r'you-get -i "%s"'%url
        os.system(cmd)
        format=input('输入画质，画质是- format:后面的字符串（例如：mp4hd2v2，直接回车默认下载最高画质）：\n')
        cmd=r'you-get --format=%s -o "%s" "%s"'%(format,savepath,url)
        os.system(cmd)
    elif n==5:
        cmd=r'you-get -u "%s"'%url
        os.system(cmd)
    else:
        print('请输入对应数字！')
if os.path.exists('D:\you get')==False:
    os.mkdir('D:\you get')
    main()
else:
    main()
while True:
    i=input('是否继续？q：退出，其它：继续\n')
    if i=='q':
        break
    else:
        main()
