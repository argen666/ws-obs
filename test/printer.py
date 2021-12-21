from escpos.printer import Network, Usb, Serial


def printMessageLAN(message):
    kitchen = Network("192.168.16.241")  # Printer IP Address
    kitchen.text("Hello World\n")
    kitchen.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    kitchen.cut()


def printMessageUSB(message):
    p = Usb(0x0519, 0x0003, in_ep=0x82, out_ep=0x02)
    p.text("Hello World\n")
    # p.image("bgg.png")
    # p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    p.cut()


def printMessageSerial(message):
    p = Serial(devfile="COM9")
    print(1)
    p.text("Hello World\n")
    print(1)
    # p.image("bgg.png")
    # p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    # print(1)
    # p.cut()
    print(1)
    p.close()
    print(1)


# printMessageLAN("")
# printMessageSerial("")
printMessageUSB("")
