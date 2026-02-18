from token_broker import TokenBroker
import pprint

def dump_raw_store():
    broker = TokenBroker()
    print("--- RAW KEY STORE ---")
    pprint.pprint(broker.key_store)

if __name__ == "__main__":
    dump_raw_store()
