// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.8.18;

import "./Depositer.sol";
import "./Strategy.sol";

import {IStrategyInterface} from "./interfaces/IStrategyInterface.sol";

contract CompV3LenderBorrowerCloner {
    address public immutable originalDepositer;
    address public immutable originalStrategy;

    event Cloned(address indexed depositer, address indexed strategy);
    event Deployed(address indexed depositer, address indexed strategy);

    constructor(
        address _asset,
        string memory _name,
        address _comet,
        uint24 _ethToAssetFee
    ) {
        Depositer _depositer = new Depositer(_comet);

        originalDepositer = address(_depositer);

        originalStrategy = address(
            new Strategy(
                _asset,
                _name,
                _comet,
                _ethToAssetFee,
                address(_depositer)
            )
        );

        emit Deployed(originalDepositer, originalStrategy);

        _depositer.setStrategy(originalStrategy);

        // Need to give the address the correct interface.
        IStrategyInterface _strategy = IStrategyInterface(originalStrategy);

        _strategy.setStrategyParams(
            7_000, // targetLTVMultiplier (default: 7_000)
            8_000, // warningLTVMultiplier default: 8_000
            1e10, // min rewards to sell
            false, // leave debt behind (default: false)
            40 * 1e9 // max base fee to perform non-emergency tends (default: 40 gwei)
        );

        _strategy.setPerformanceFeeRecipient(msg.sender);
        _strategy.setKeeper(msg.sender);
        _strategy.setManagement(msg.sender);
    }

    function name() external pure returns (string memory) {
        return "Yearnv3-CompV3LenderBorrowerCloner";
    }

    function cloneCompV3LenderBorrower(
        address _asset,
        string memory _name,
        address _management,
        address _rewards,
        address _keeper,
        address _comet,
        uint24 _ethToAssetFee
    ) external returns (address newDepositer, address newStrategy) {
        newDepositer = Depositer(originalDepositer).cloneDepositer(_comet);

        // Use Tokenized strategy to clone
        newStrategy = IStrategyInterface(originalStrategy).clone(
            _asset,
            _name,
            _management,
            _rewards,
            _keeper
        );

        // Initialize the strategy specific variables.
        IStrategyInterface(newStrategy).initializeCompV3LenderBorrower(
            _comet,
            _ethToAssetFee,
            newDepositer
        );

        // Set the strategy in the depositer.
        Depositer(newDepositer).setStrategy(newStrategy);

        IStrategyInterface(newStrategy).setStrategyParams(
            7_000, // targetLTVMultiplier (default: 7_000)
            8_000, // warningLTVMultiplier default: 8_000
            1e10, // min rewards to sell
            false, // leave debt behind (default: false)
            40 * 1e9 // max base fee to perform non-emergency tends (default: 40 gwei)
        );

        emit Cloned(newDepositer, newStrategy);
    }
}
