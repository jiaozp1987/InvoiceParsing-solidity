// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

library InvoiceLib {
    struct invoiceDomain{
        string id;
        string fileName;
        string fromName;
        string fromID;
        string toName;
        string toID;
        string typeName;
        string typeID;
        string sumPrice;
        string invoiceDate;
        string createDate;
        bool isRepeat;
    }
}