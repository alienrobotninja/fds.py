// SPDX-License-Identifier: MIT
pragma solidity 0.8.8;

contract SolidityTestContract {
    address public owner;
    uint256 public count;

    constructor() {
        owner = msg.sender;
    }

    function getCount() external view returns (uint256) {
        return count;
    }

    function increment() external returns (uint256) {
        return count++;
    }
}
