// SPDX-License-Identifier: UNLICENCED

pragma solidity ^0.7.0;

contract ERC20 {
    string public symbol;
    string public name;
    uint8 public decimals = 0;
    uint256 total;

    address public owner;

    mapping (address => uint256) balances;
    mapping (address => mapping(address => uint256)) allowances;

    constructor(string memory _symbol, string memory _name, uint256 _totalsupply) {
        owner = msg.sender;
        total = _totalsupply;
        symbol = _symbol;
        name = _name;
        balances[owner] = total;
    }

    function totalSupply() view public returns (uint256) {
        return total;
    }

    function balanceOf(address _account) view public returns (uint256) {
        return balances[_account];
    }

    function transfer(address _to, uint256 _amount) public returns (bool) {
        require(balances[msg.sender] >= _amount, 'not sufficient tokens');
        require(_amount > 0, 'positive amount');
        require(balances[_to] + _amount >= _amount, 'overflow protection');

        balances[msg.sender] = balances[msg.sender] - _amount;
        balances[_to] = balances[_to] +  _amount;
        return true;
    }

    function allowance(address _owner, address _spender) view public returns (uint256) {
        return allowances[_owner][_spender];
    }
    
    function approve(address _spender, uint256 _amount) public returns (bool) {
        allowances[msg.sender][_spender] = _amount;
        return true;
    }
    
    function transferFrom(address _from, address _to, uint256 _amount) public returns (bool) {
        require(balances[_from] >= _amount, 'not sufficient tokens');
        require(_amount > 0, 'positive amount');
        require(balances[_to] + _amount >= _amount, 'overflow protection');
        uint256 currentAllowance = allowances[_from][msg.sender];
        require( currentAllowance >= _amount, "Exceed allowance.");
        
        balances[_from] = balances[_from] - _amount;
        balances[_to] = balances[_to] + _amount;
        allowances[_from][msg.sender] = currentAllowance - _amount;
        return true;
    }

}
