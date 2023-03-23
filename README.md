# Tokenized Strategy Mix for Yearn V3 strategies

This repo will allow you to write, test and deploy V3 "Tokenized Strategies".

You will only need to override the three functions in Strategy.sol of '_invest', 'freeFunds' and '_totalInvested'. With the option to also override '_tend' and 'tendTrigger' if needed.

## How to start

### Clone the repo

    git clone https://github.com/Schlagonia/V2-Base-Strategy-Adapter

    cd V2-Base-Strategy-Adapter

### Set up your virtual enviorment

    python3 -m venv venv

    source venv/bin/acitvate

### Install Ape and all dependencies

    pip install -r requirements.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your enviorment Variables

    export WEB3_INFURA_PROJECT_ID=yourInfuraApiKey

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.