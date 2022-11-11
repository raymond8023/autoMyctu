# autoMyctu
good good study, day day up
网大挂课，url输入课程页面地址（通常是kc.zhixueyun.com开头的），会自动跳转到登陆页面，设置为30s以内需要完成扫码登陆，然后就是自动学习了
目前只实现了html5的视频课程
可以使用：python main.py --url "课程页面网址"
也可以直接运行后再输入网址

目前难以解决的问题：
1、网大是kc.zhixueyun.com跳转到myctu.cn登陆，不知道是不是这个原因导致cookie无法生效，最后放弃
2、找到“继续学习”用click()进入链接，driver获取不到新窗口的handle，最终只能从属性中找到相关信息硬凑了一个地址（不确定是不是都适用），然后手动开启新窗口

下一步可以优化的地方：
1、支持pdf，url，ppt等格式的课程
2、增强代码健壮性