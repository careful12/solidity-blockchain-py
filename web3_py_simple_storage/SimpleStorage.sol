// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 number;

    struct People {
        uint256 number;
        string name;
    }
    People[] public people;
    mapping(string => uint256) public nameToNum;

    function store(uint256 _number) public returns (uint256) {
        number = _number;
        return number;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }

    function addPerson(string memory _name, uint256 _number) public {
        people.push(People(_number, _name));
        nameToNum[_name] = _number;
    }
}
