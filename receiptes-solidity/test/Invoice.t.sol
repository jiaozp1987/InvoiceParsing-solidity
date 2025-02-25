// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;
import "../src/libraries/InvoiceLib.sol";
import  {Test, console} from "forge-std/Test.sol";
import "../src/Invoice.sol";

contract InvoiceTest is Test{
    Invoice public invoice;
    address public user1 = address(1);
    string notID = '35312000000000600000';

    function setUp() public {
        vm.startPrank(user1);
        invoice = new Invoice();
        vm.stopPrank();

    }

    function testAddInvoice() public {
        vm.startPrank(user1);
        string[11] memory info = [
                    '25312000000000600000',
                    'a.pdf',
                    'asd',
                    '91310115087809055Y',
                    'sdfsfs',
                    '91310000MABT70XH0J',
                    'sdfsdfsdfsdf',
                    '31',
                    '1400.23',
                    '2025-01-02',
                    '2025-02-02'
            ];
        assert(invoice.addInvoice(info));
        InvoiceLib.invoiceDomain memory invoiceResult = invoice.invoiceExisted(info[0]);
        assertTrue(invoiceResult.isRepeat,"not store");

        vm.stopPrank();
    }

    function testInvoiceExisted() public {
        vm.startPrank(user1);
        string[11] memory info = [
                    '25312000000000600000',
                    'a.pdf',
                    'asd',
                    '91310115087809055Y',
                    'sdfsfs',
                    '91310000MABT70XH0J',
                    'sdfsdfsdfsdf',
                    '31',
                    '1400.23',
                    '2025-01-02',
                    '2025-02-02'
            ];
        assert(invoice.addInvoice(info));
        InvoiceLib.invoiceDomain memory invoiceStore = invoice.invoiceExisted(info[0]);
        assertTrue(invoiceStore.isRepeat,"not store");
        InvoiceLib.invoiceDomain memory invoiceNotStore = invoice.invoiceExisted(notID);
        assertTrue(!invoiceNotStore.isRepeat,"wrong store");
        vm.stopPrank();
    }
}
