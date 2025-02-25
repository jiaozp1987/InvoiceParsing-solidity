// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import "../src/Invoice.sol";

contract InvoiceDeploy is Script {
    Invoice public invoice;

    function setUp() public {}

    function run() public {
        vm.startBroadcast();

        invoice = new Invoice();

        vm.stopBroadcast();
    }
}
