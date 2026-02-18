import pprint

from token_broker import TokenBroker


def dump_raw_store():
    broker = TokenBroker()
    print("--- RAW KEY STORE ---")
    pprint.pprint(broker.key_store)

if __name__ == "__main__":
    dump_raw_store()
