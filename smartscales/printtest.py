from escpos import *
usb = printer.Usb(0x0fe6, 0x811e, 0, out_ep=0x02)
contents = u'苹果   ￥18.88/kg   0.50kg    ￥9.44'.encode('utf8')

print(type(contents), contents)
usb.text(str(contents))
#usb.text(u"苹果   ￥18.88/kg   0.50kg    ￥9.44".encode('utf8'))
usb.text("\n")
usb.text("print sueecssfully\n")
usb.text("time: 23:28---0\n")
usb.text("time: 23:28---1\n")
usb.text("time: 23:28---2\n")
#usb.text("time: 23:28---3\n")
#usb.text("time: 23:28---4\n")
#usb.text("time: 23:28---5\n")
#usb.image(‘image path’)#打印图片（黑白2值）
#usb.qr(‘值’)#打印二维码
#usb.set(codepage=None, align='center')#设置页面居中
usb.cut()#切纸
usb.close()#关闭连接