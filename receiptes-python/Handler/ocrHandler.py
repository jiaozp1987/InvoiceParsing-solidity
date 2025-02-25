import os
import time
import cv2
from confDomain import ConfDomain
from invoiceDomain import InvoiceDomain
from web3Handler import we3Handler
from paddleocr import PaddleOCR


class OCR:
    def __init__(self):
        self.basePath = "./input"
        self.filePaths = ""
        self.invoiceList = list()

    def rename4pic(self):
        """
        重命名函数fun2
        输入：文件夹路径
        功能：对某一个文件夹中的某一类文件进行统一命名，命名格式为：基础名+数字序号
        """
        i = 1
        for file in os.listdir(self.basePath):
            if file.endswith('.png') or file.endswith('.jpg'):
                if file.endswith('.png'):
                    suffix = '.png'
                else:
                    suffix = '.jpg'
                if os.path.isfile(os.path.join(self.basePath, file)):
                    newName = file.replace(file, str(round(time.time())) + str(i) + suffix)  # 根据需要设置基本文件名
                    os.rename(os.path.join(self.basePath, file), os.path.join(self.basePath, newName))
                    i += 1
        print("rename4pic over")

    def getFilepath(self):
        self.rename4pic()
        '''获取当前路径下所有的电子发票pdf文件路径'''
        filePaths = []
        file_names = os.listdir(self.basePath)
        for file_name in file_names:
            if file_name.endswith('.png'):
                filePaths.append(os.path.join(self.basePath, file_name))
            if file_name.endswith('.jpg'):
                filePaths.append(os.path.join(self.basePath, file_name))
        self.filePaths = filePaths

    def getInvoiceList(self):
        for item in self.filePaths:
            self.invoiceList.append(self.getContent(item))

    def getContent(self, imgPath):
        invoice = InvoiceDomain()
        invoice.fileName = imgPath.replace("./input\\", "")
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(imgPath, cls=True)
        txts = list()
        for line in result[0]:
            txts.append(line[1][0])
        conf = ConfDomain()
        for i in range(len(txts)):
            if txts[i].find("发票号码") >= 0:
                ltxt = txts[i].split("：")
                invoice.id = ltxt[1]
            if txts[i].find("开票日期") >= 0:
                ltxt = txts[i].split("：")
                invoice.invoiceDate = ltxt[1]
            if txts[i] == '增值税专用发票' or txts[i] == '增值税电子普通发票':
                invoice.typeName = txts[i]
            if txts[i].find(conf.active) >= 0:
                ltxt = txts[i].split("：")
                invoice.toName = ltxt[1]
            if txts[i].find(conf.company[conf.active]) >= 0:
                ltxt = txts[i].split("：")
                invoice.toID = ltxt[1]
            if txts[i].find('名称') == 0:
                ltxt = txts[i].split("：")
                invoice.formName = ltxt[1]
            if txts[i].find('纳税人识别号') == 0:
                ltxt = txts[i].split("：")
                invoice.formID = ltxt[1]
        qrResult = self.getQR(imgPath)
        qrResult = qrResult[0].split(",")
        invoice.typeID = qrResult[1]
        invoice.id = qrResult[3]
        invoice.sumPrice = qrResult[4]
        info = we3Handler().invoiceExisted(invoice.id)
        if not info[11]:
            invoice.repeat = "否"
        else:
            invoice.createDate = info[10]
            invoice.repeat = "是"
        return invoice

    def getQR(self, imgPath):
        # 使用微信的识别模型
        qrstr = cv2.wechat_qrcode_WeChatQRCode()
        # 读取图片
        image = cv2.imread(imgPath)
        # 获取值
        result, pos = qrstr.detectAndDecode(image)
        return result

    def main(self):
        self.getFilepath()
        self.getInvoiceList()
