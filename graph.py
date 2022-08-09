from inspect import signature
import pymongo
from config import MongoDBConfig
from constants import MongoCollections


class Graph:
    def __init__(self):
        self.myclient = pymongo.MongoClient(MongoDBConfig.CONNECTION_URL)
        self.db = self.myclient[MongoCollections.cross_chain_identities]
        # remove all old data_base
        self.clear_data_base()

        self.last_block_number = {}
        for db_col in MongoCollections.network:
            self.last_block_number[db_col] = 0

        self.build_total_graph()

        for db_col in MongoCollections.network:
            last_block = self.build_graph(db_col)
            self.last_block_number[db_col] = last_block

    def get_chain_id(self, network):
        return MongoCollections.chain_id[network]

    def get_all_event_in_db(self, query, network_db):
        events = []
        for db_col in MongoCollections.network:
            if db_col == network_db:
                chain_id = self.get_chain_id(db_col)
                # db = self.myclient[db_col]
                # col = db[MongoCollections.Collection]
                col = self.db[chain_id + "_events"]
                events = col.find(query)
        return events

    def clear_data_base(self):
        for db_col in MongoCollections.network:
            # db = self.myclient[db_col]

            col1 = self.db[MongoCollections.GraphDB]
            col1.drop()

            col2 = self.db[MongoCollections.RootGraphDB]
            col2.drop()

    def is_address_in_graph(self, address, network_db):
        try:
            for db_col in MongoCollections.network:
                if db_col == network_db:
                    # db = self.myclient[db_col]
                    col = self.db[MongoCollections.RootGraphDB]
                    # query = {"address": address, "chainId": self.get_chain_id(db_col)}
                    query = {"_id": self.get_chain_id(db_col) + "_" + address}
                    answer = col.find_one(query)
                    if answer is None:
                        return False
                    else:
                        return True
        except:
            return False

        return False

    def get_root_of_address(self, address, network_db):
        for db_col in MongoCollections.network:
            if db_col == network_db:
                # db = self.myclient[db_col]
                col = self.db[MongoCollections.RootGraphDB]
                # query = {"address": address, "chainId": self.get_chain_id(db_col)}
                query = {"_id": self.get_chain_id(db_col) + "_" + address}
                answer = col.find_one(query)
                if answer is not None:
                    try:
                        return answer["root"]
                    except:
                        return address
        return address

    def insert_new_address_to_graph(self, address, network_db):
        for db_col in MongoCollections.network:
            if db_col == network_db:
                # db = self.myclient[db_col]
                col_root = self.db[MongoCollections.RootGraphDB]
                # data = {"address": address, "root": address, "chainId": self.get_chain_id(db_col)}
                data = {"_id": self.get_chain_id(db_col) + "_" + address, "address": address, "root": address,
                        "chainId": self.get_chain_id(db_col)}
                col_root.insert_one(data)

                col_graph = self.db[MongoCollections.GraphDB]
                # data2 = {"root": address, "addresses": [address], "chainId": self.get_chain_id(db_col)}
                data2 = {"_id": self.get_chain_id(db_col) + "_" + address, "root": address, "addresses": [address],
                         "chainId": self.get_chain_id(db_col)}
                col_graph.insert_one(data2)

    def insert_element_to_tree(self, root, network_db, address):

        root_add = self.get_root_of_address(address, network_db)
        if root_add == root:
            return

        for db_col in MongoCollections.network:
            if db_col == network_db:
                # db = self.myclient[db_col]
                col_graph = self.db[MongoCollections.GraphDB]
                # col_graph.update_one({"root": root, "chainId": self.get_chain_id(db_col)}, {"$push": {"addresses": address}})
                col_graph.update_one({"_id": self.get_chain_id(db_col) + "_" + root},
                                     {"$push": {"addresses": address}})

                col_root_graph = self.db[MongoCollections.RootGraphDB]
                # col_root_graph.update_one({"address": address, "chainId": self.get_chain_id(db_col)}, {"$set": {"root": root}})
                col_root_graph.update_one({"_id": self.get_chain_id(db_col) + "_" + address},
                                          {"$set": {"root": root}})

    def remove_old_root(self, root, network_db):
        for db_col in MongoCollections.network:
            if db_col == network_db:
                # db = self.myclient[db_col]
                col_graph = self.db[MongoCollections.GraphDB]
                # col_graph.delete_one({"root": root, "chainId": self.get_chain_id(db_col)})
                col_graph.delete_one({"_id": self.get_chain_id(db_col) + "_" + root})

    def get_all_user_from_root(self, root, network_db):
        for db_col in MongoCollections.network:
            if db_col == network_db:
                # db = self.myclient[db_col]
                col = self.db[MongoCollections.GraphDB]
                # query = {"root": root, "chainId": self.get_chain_id(db_col)}
                query = {"_id": self.get_chain_id(db_col) + "_" + root}
                answer = col.find_one(query)
                if answer is not None:
                    try:
                        return answer["addresses"]
                    except:
                        return [root]

        return [root]

    def connect_user(self, address_a, address_b, network_db):
        if not self.is_address_in_graph(address_a, network_db):
            self.insert_new_address_to_graph(address_a, network_db)
        if not self.is_address_in_graph(address_b, network_db):
            self.insert_new_address_to_graph(address_b, network_db)

        # get root
        root_a = self.get_root_of_address(address_a, network_db)
        root_b = self.get_root_of_address(address_b, network_db)
        # same root
        if root_a == root_b:
            return

        # mer root_a and root_b
        addresses_a = self.get_all_user_from_root(root_a, network_db)
        addresses_b = self.get_all_user_from_root(root_b, network_db)

        if len(addresses_a) < len(addresses_b):
            for x in addresses_a:
                self.insert_element_to_tree(root_b, network_db, x)
            self.remove_old_root(root_a, network_db)

        else:
            for x in addresses_b:
                self.insert_element_to_tree(root_a, network_db, x)
            self.remove_old_root(root_b, network_db)

    def add_event_to_graph(self, event, network_db):
        try:
            root = event["addresses"][0]
            for address in event["addresses"]:
                self.connect_user(root, address, network_db)
        except:
            print("some error!!!")

    def build_graph(self, network_db):
        query = {"event_type": "CONNECTUSER", "block_number": {"$gt": self.last_block_number[network_db]}}
        events = self.get_all_event_in_db(query, network_db)
        max_block_number = self.last_block_number[network_db]

        for event in events:
            self.add_event_to_graph(event, network_db)
            if event["block_number"] > max_block_number:
                max_block_number = event["block_number"]

        return max_block_number

    def build_total_graph(self):
        for network_db in MongoCollections.network:
            query = {"event_type": "CONNECTUSER", "block_number": {"$gt": self.last_block_number[network_db]}}
            events = self.get_all_event_in_db(query, network_db)

            for event in events:
                self.add_event_to_graph(event, MongoCollections.all_chain)

    def get_all_user(self, address, network_db):
        if self.is_address_in_graph(address, network_db):
            root = self.get_root_of_address(address, network_db)
            answer = self.get_all_user_from_root(root, network_db)
            return answer
        else:
            return [address]

    def get_network_db(self, network):
        # return network.lower() + MongoCollections.Suffix
        return MongoCollections.mapping[network]

    def query_update_user(self, address_a, network):
        address_a = address_a.lower()

        # list event response
        list_event_response = []

        # update all graph
        self.build_total_graph()
        for db_col in MongoCollections.network:
            last_block = self.build_graph(db_col)
            self.last_block_number[db_col] = last_block

        # get all user from graph
        addresses = self.get_all_user(address_a, MongoCollections.all_chain)
        network_db = self.get_network_db(network)

        # get all user from component graph
        is_address_exits = {}
        cnt = 0
        for address in addresses:
            if address.lower() not in is_address_exits:
                wallet = self.get_all_user(address, network_db)
                cnt = cnt + 1
                for x in wallet:
                    is_address_exits[x.lower()] = cnt

        # get all event have list adress in addresses
        query = {"event_type": "CONNECTUSER", "addresses": {"$elemMatch": {"$in": addresses}}}
        list_event = []
        for db_col in MongoCollections.network:
            events = self.get_all_event_in_db(query, db_col)
            for x in events:
                list_event.append(x)

        while len(list_event) != 0:
            tmp = []

            best_event = {}
            best_connect = 0

            for event in list_event:
                # kiem tra xem 1 event connect duoc bao nhieu wallet
                check = {}
                for address in event["addresses"]:
                    if address in is_address_exits:
                        check[is_address_exits[address]] = is_address_exits[address]

                if len(check) >= 2:
                    tmp.append(event)
                    if len(check) > best_connect:
                        best_connect = len(check)
                        best_event = event

            if best_connect == 0:
                break

            list_event_response.append(best_event)

            # danh dau lai nhung address chung 1 wallet
            wallet = 0
            for address in best_event["addresses"]:
                if address in is_address_exits:
                    if wallet == 0:
                        wallet = is_address_exits[address]
                    is_address_exits[address] = wallet

            list_event = tmp
        addresses = []
        signature = []

        for event in list_event_response:
            addresses.append(event["addresses"])
            signature.append(event["signature"])

        return (addresses, signature)