import random
import sys
from Cryptodome.PublicKey import RSA

class Node:
    mem_pool = []
    blocks = []
    preEvents = []

    def __init__(self, id, nodes):
        self.coin = 1000
        self.id = id
        self.costs = [0 for _ in range(len(nodes) + 1)]
        self.preEvents = []
        self.key = RSA.generate(1024)

        # Initialize edge values for this node
        for num, node in enumerate(nodes):
            if node.id == self.id:
                self.costs[num] = 0
            else:
                edge_val = random.randint(1, 26)

                if edge_val < 10:  # Example probability threshold
                    self.costs[num] = edge_val
                    if len(node.costs) <= self.id:
                        node.costs.append(edge_val)
                    else:
                        node.costs[self.id] = edge_val
                else:
                    self.costs[num] = sys.maxsize
                    if len(node.costs) <= self.id:
                        node.costs.append(sys.maxsize)
                    else:
                        node.costs[self.id] = sys.maxsize

    def gossip(self, obj, mode):
        # mode 0 : transaction | 1: mine
        strObj = obj
        if mode == 1:
            strObj = base64.b64encode(obj)

        threads = []
        # Simulate gossiping transactions or blocks
        for num, i in enumerate(nodes):
            if num != self.id:
                th = threading.Thread(target=i.receive, args=(obj, mode))
                threads.append(th)
                th.start()

        # join threads to the parent thread
        for t in threads:
            t.join()

    def receive(self, obj, mode):
        # Simulate receiving and processing
        self.gossip(obj, mode)

    def create_transaction(self, receiver, amount):
        # Logic for creating a transaction
        tx = {
            "sender_id": self.id,
            "receiver_id": receiver.id,
            "amount": amount
        }
        return tx

    def mine_block(self):
        # Logic for mining a block (example)
        if self.mem_pool:
            block = {
                "block_id": len(self.blocks),
                "transactions": self.mem_pool
            }
            self.blocks.append(block)
            self.mem_pool.clear()
            return block
        return None

    def update_costs(self, nodes):
        # This method can be used to adjust edge costs if required
        pass
