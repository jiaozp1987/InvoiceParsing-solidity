import os
from web3Handler import we3Handler
import fitz
from pyzbar.pyzbar import decode
from PIL import Image
from confDomain import ConfDomain
from invoiceDomain import InvoiceDomain


class PDFInvoice:

    def __init__(self):
        self.basePath = "./input"
        self.filePaths = ""
        self.invoiceList = list()

    def getFilepath(self):
        '''获取当前路径下所有的电子发票pdf文件路径'''
        filePaths = []
        fileNames = os.listdir(self.basePath)
        for fileName in fileNames:
            if fileName.endswith('.pdf'):
                filePaths.append(os.path.join(self.basePath, fileName))
        self.filePaths = filePaths

    def getInvoiceList(self):

        '''逐一对所有电子发票文件左上角的二维码识别并重命名文件'''
        for filePath in self.filePaths:
            invoice = self.getQrcode(filePath)
            self.invoiceList.append(invoice)

    def getQrcode(self, filePath):
        invoice = InvoiceDomain()
        '''提取pdf文件中左上角的二维码并识别'''
        pdfDoc = fitz.open(filePath)
        invoice.fileName = filePath.replace("./input\\", "")
        # 初始化一个空字符串来收集文本
        fullText = ""

        # 遍历每一页
        for page in pdfDoc:
            # 提取当前页面的文本并追加到fullText字符串
            fullText += page.get_text()

        fullTextList = fullText.split("\n")
        invoice.typeName = fullTextList[0]
        conf = ConfDomain()
        iniIndex = 0
        for item in fullTextList:
            if item.find(conf.active) >= 0:
                iniIndex = fullTextList.index(item)

        invoice.id = fullTextList[iniIndex - 2]
        invoice.invoiceDate = fullTextList[iniIndex - 1]
        invoice.toName = fullTextList[iniIndex]
        invoice.toID = fullTextList[iniIndex + 1]
        invoice.formName = fullTextList[iniIndex + 2]
        invoice.formID = fullTextList[iniIndex + 3]
        info = we3Handler().invoiceExisted(invoice.id)

        if not info[11]:
            invoice.repeat = "否"
        else:
            invoice.createDate = info[10]
            invoice.repeat = "是"

        rotate = int(0)
        zoomX = 3.0
        zoomY = 3.0
        mat = fitz.Matrix(zoomX, zoomY).prerotate(rotate)
        rect = page.rect
        mp = rect.tl + (rect.br - rect.tl) * 1 / 5
        clip = fitz.Rect(rect.tl, mp)
        pix = page.get_pixmap(matrix=mat, alpha=False, clip=clip)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        barcodes = decode(img)

        # 关闭文档
        pdfDoc.close()
        for barcode in barcodes:
            QRresult = barcode.data.decode("utf-8")
        QRresultList = QRresult.split(",")
        invoice.sumPrice = QRresultList[4]
        invoice.typeID = QRresultList[1]
        return invoice

    def main(self):
        self.getFilepath()
        self.getInvoiceList()


if __name__ == '__main__':
    PDFInvoice().main()
