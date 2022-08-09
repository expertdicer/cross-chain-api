class Sessions:
    id = "_id"
    step = "step"
    status = "status"
    timestamp = "timestamp"
    name = "nameOfIdentity"
    requirement = "requirement"
    wallet_addresses = "walletAddresses"
    sign = 'sign'
    isSign = 'isSign'
    created_by_wallet = "walletAddress"
    identity = "identity"
    chain_id = "chainId"


class Identities:
    id = "_id"
    name = "name"
    chain_id = "chain_id"
    created_by_session_id = "sessionId"
    wallet_addresses = "walletAddresses"
    address = 'address'
    timestamp = 'timestamp'
    name_of_identity = 'nameOfIdentity'
    adding_wallet_addresses = 'addingWalletAddresses'
    requirement = "requirement"
    wallet_address = "walletAddress"
    sign = "sign"


class Wallets:
    id = "_id"
    address = "address"
    having_identity = "havingIdentity"
    identity = "identity"
    invited_in_identities = "invitingIdentities"


class Events:
    id = "_id"
    block_timestamp = "block_timestamp"
    block_number = "block_number"
    timestamp = "timestamp"
    contract_address = "contract_address"
    event_type = "event_type"
    log_index = "log_index"
    sender = "sender"
    transaction_hash = "transaction_hash"
    transaction_id = "transaction_id"
    type = "type"
    revocation = "REVOCATION"


class MongoCollections:
    GraphDB = "identity_graph_builder"
    RootGraphDB = "identity_graph_builder_root"
    cross_chain_identities = "CrossChainIdentities"
    wallets = 'wallets'
    identities = 'identities'
    sessions = 'sessions'
    b_richer = "BRicher"
    tokens = 'tokens'
    events = 'events'
    suffix = "_blockchain_etl"
    bsc_testnet = "bsc_testnet"
    rinkeby = "rinkeby"
    goerli = "goerli"
    all_chain = 'all_chain'
    network = [all_chain, bsc_testnet, rinkeby, goerli]
    mapping = {
        "bsc": bsc_testnet,
        "rinkeby": rinkeby,
        "goerli": goerli,
    }
    chain_id = {
        all_chain: '0x',
        bsc_testnet: '0x61',
        rinkeby: '0x4',
        goerli: '0x5'
    }


class ArangoDBConstant:
    TOKEN_DB = "token_database"
    CONFIGS_COL = "configs"
    TOKENS_COL = "tokens"
    MERGED_TOKEN_PRICE_COL = "merged_token_price"
    TOKEN_PRICE_COL = "token_price"
    price_change_logs = "priceChangeLogs"