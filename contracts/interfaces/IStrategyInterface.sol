// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.18;

import {IStrategy} from "@tokenized-strategy/interfaces/IStrategy.sol";

interface IStrategyInterface is IStrategy {
    function baseToken() external view returns (address);

    function depositer() external view returns (address);

    function setStrategyParams(
        uint16 _targetLTVMultiplier,
        uint16 _warningLTVMultiplier,
        uint256 _minToSell,
        bool _leaveDebtBehind,
        uint256 _maxGasPriceToTend
    ) external;

    function initializeCompV3LenderBorrower(
        address _comet,
        uint24 _ethToAssetFee,
        address _depositer
    ) external;
}
