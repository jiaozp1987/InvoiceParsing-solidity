// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;
import "./libraries/InvoiceLib.sol";

contract Invoice{
    address private immutable owner;
    mapping (string => InvoiceLib.invoiceDomain) public  invoices;

    constructor(){
        owner = msg.sender;
    }

    receive() external payable { }
    fallback() external payable { }

    function invoiceExisted(string calldata id) public view returns(InvoiceLib.invoiceDomain memory invoiceResult){
        invoiceResult = invoices[id];
        if(bytes(invoiceResult.id).length > 0){
            invoiceResult.isRepeat = true;
        }
    }

    function __addInvoice(string[11] calldata params) private pure returns(InvoiceLib.invoiceDomain memory invoiceResult){
        invoiceResult.id = params[0];
        invoiceResult.fileName = params[1];
        invoiceResult.fromName = params[2];
        invoiceResult.fromID = params[3];
        invoiceResult.toName = params[4];
        invoiceResult.toID = params[5];
        invoiceResult.typeName = params[6];
        invoiceResult.typeID = params[7];
        invoiceResult.sumPrice = params[8];
        invoiceResult.invoiceDate = params[9];
        invoiceResult.createDate = params[10];
    }    

    function _addInvoice(InvoiceLib.invoiceDomain memory invoiceResult) private returns(bool callback){
        invoices[invoiceResult.id] = invoiceResult;
        callback = true;
        return callback;
    }

    function addInvoice( string[11] calldata params ) external returns(bool){
        require(!invoiceExisted(params[0]).isRepeat,"invoice exists");
        InvoiceLib.invoiceDomain memory invoice = __addInvoice(params);
        return _addInvoice(invoice);
    }
}