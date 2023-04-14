import pytest
from ape import Contract, project


############ CONFIG FIXTURES ############

# Adjust the string based on the `asset` your strategy will use
# You may need to add the token address to `tokens` fixture.
@pytest.fixture(scope="session")
def asset(tokens):
    yield Contract(tokens["wbtc"])


# Adjust the amount that should be used for testing based on `asset`.
@pytest.fixture(scope="session")
def amount(asset, user, whale):
    amount = 100 * 10 ** asset.decimals()

    asset.transfer(user, amount, sender=whale)
    yield amount


@pytest.fixture(scope="session")
def comets():
    comets = {
        "weth": "0xA17581A9E3356d9A858b789D68B4d866e593aE94",
        "usdc": "0xc3d688B66703497DAA19211EEdff47f25384cdc3",
    }
    yield comets


@pytest.fixture(scope="session")
def comet(comets):
    return Contract(comets["usdc"])


@pytest.fixture(scope="session")
def comet_rewards():
    yield project.CometRewards.at("0x1B0e765F6224C21223AeA2af16c1C46E38885a40")


@pytest.fixture(scope="session")
def comp():
    yield Contract("0xc00e94Cb662C3520282E6f5717214004A7f26888")


@pytest.fixture(scope="session")
def eth_to_asset_fee():
    yield 3_000


############ STANDARD FIXTURES ############


@pytest.fixture(scope="session")
def daddy(accounts):
    yield accounts["0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52"]


@pytest.fixture(scope="session")
def user(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def rewards(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def management(accounts):
    yield accounts[2]


@pytest.fixture(scope="session")
def keeper(accounts):
    yield accounts[3]


@pytest.fixture(scope="session")
def tokens():
    tokens = {
        "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "wbtc": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "dai": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    }
    yield tokens


@pytest.fixture(scope="session")
def whale(accounts):
    # In order to get some funds for the token you are about to use,
    # The Balancer vault stays steady ballin on almost all tokens
    # NOTE: If `asset` is a balancer pool this may cause issues on amount checks.
    yield accounts["0xBA12222222228d8Ba445958a75a0704d566BF2C8"]


@pytest.fixture(scope="session")
def weth(tokens):
    yield Contract(tokens["weth"])


@pytest.fixture(scope="session")
def weth_amount(user, weth):
    weth_amount = 10 ** weth.decimals()
    user.transfer(weth, weth_amount)
    yield weth_amount


@pytest.fixture(scope="session")
def create_cloner(management, keeper, rewards, comet, eth_to_asset_fee):
    def create_cloner(asset, performanceFee=0):
        cloner = management.deploy(project.CompV3LenderBorrowerCloner, asset, "yCompV3-lender-borrower-UniSwaps", comet, eth_to_asset_fee)
        
        strategy = project.IStrategyInterface.at(cloner.originalStrategy())

        strategy.setKeeper(keeper, sender=management)
        strategy.setPerformanceFeeRecipient(rewards, sender=management)
        strategy.setPerformanceFee(performanceFee, sender=management)

        return cloner

    yield create_cloner


@pytest.fixture(scope="session")
def create_oracle(management):
    def create_oracle(_management=management):
        oracle = _management.deploy(project.StrategyAprOracle)

        return oracle

    yield create_oracle


@pytest.fixture(scope="session")
def cloner(asset, create_cloner):
    cloner = create_cloner(asset)

    yield cloner


@pytest.fixture(scope="session")
def strategy(cloner):
    strategy = project.IStrategyInterface.at(cloner.originalStrategy())
    
    yield strategy

@pytest.fixture(scope="session")
def depositer(cloner):
    depositer  = project.Depositer.at(cloner.orginalDepositer())

    yield depositer


@pytest.fixture(scope="session")
def oracle(create_oracle):
    oracle = create_oracle()

    yield oracle


############ HELPER FUNCTIONS ############


@pytest.fixture(scope="session")
def deposit(strategy, asset, user, amount):
    def deposit(_strategy=strategy, _asset=asset, assets=amount, account=user):
        _asset.approve(_strategy, assets, sender=account)
        _strategy.deposit(assets, account, sender=account)

    yield deposit


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
