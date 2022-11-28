class Node:
    def __init__(self, item, freq, father):
        self.item = item
        self.freq = freq
        self.father = father # father節點指標
        self.ptr = None # 定義指標
        self.children = {} # children節點，用dict儲存，方便根據item查詢
    
    # 更新頻次
    def update_freq(self):
        self.freq += 1

    # 新增children
    def add_child(self, node):
        self.children[node.item] = node