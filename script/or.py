from collections import defaultdict

def filter_unfreq_items(dataset, min_freq):
    data_dict = defaultdict(int)
    # 統計每一項出現的次數
    for trans in dataset:
        for item in trans:
            data_dict[item] += 1
        
    # 根據閾值過濾
    ret = {}
    for k, v in data_dict.items():
        if v >= min_freq:
            ret[k] = v
    return ret

def transform_to_header_table(data_dict):
    return {k: [v, None] for k, v in data_dict.items()}

def rank_by_header(data, header_dict):
    rank_dict = {}
    for item in data:
        # 如果元素是高頻的則保留，否則則丟棄
        if item in header_dict:
            rank_dict[item] = header_dict[item]
    
    # 對元素按照整體出現的頻次排序
    item_list = sorted(rank_dict.items(),key=lambda x: x[1], reverse=True)
    return [i[0] for i in item_list]

class Node:
    def __init__(self, item, freq, father):
        self.item = item
        self.freq = freq
        # 父節點指標
        self.father = father
        # 定義指標
        self.ptr = None
        # 孩子節點，用dict儲存，方便根據item查詢
        self.children = {}
    
    # 更新頻次
    def update_freq(self):
        self.freq += 1

    # 新增孩子
    def add_child(self, node):
        self.children[node.item] = node

def up_forward(node):
    path = []
    while node.father is not None:
        path.append(node)
        node = node.father
    # 過濾樹根return path

def insert_table(head_node, node):
    while head_node.ptr is not None:
        head_node = head_node.ptr
    head_node.ptr = node

def create_FP_tree(dataset, header_dict=None, min_freq=3):
    if head_table == None:
        header_dict = filter_unfreq_items(dataset, min_freq)
    root = Node('Null', 0, None)
    for data in dataset:
        # 根據整體出現次數進行排序
        item_list = rank_by_header(data, header_dict)
        print(item_list)
        head = root
        # 按照排序順序依次往樹上插入
        for item in item_list:
            if item in head.children:
                head = head.children[item]
            else:
                new_node = Node(item, 0, head)
                head.add_child(new_node)
                # 頭指標指向的位置為空，那麼我們直接讓頭指標指向當前位置
                if head_table[item][1] is None:
                    head_table[item][1] = new_node
                else:
                    # 否則的話，我們將當前元素新增到連結串列的末尾
                    insert_table(head_table[item][1], new_node)
                head = new_node
            head.update_freq()
    return root

def regenerate_dataset(head_table, item):
    dataset = {}
    if item not in head_table:
        return dataset
    # 通過head_table找到連結串列的起始位置
    node = head_table[item][1]
    # 遍歷連結串列
    while node is not None:
        # 對連結串列中的每個位置，呼叫up_forward，獲取FP-tree上的資料
        path = up_forward(node)
        if len(path) > 1:
            # 將元素的set作為key
            # 這裡去掉了item，為了使得新構建的資料當中沒有item
            # 從而挖掘出以含有item為前提的新的頻繁項
            dataset[frozenset(path[1:])] = node.freq
        node = node.ptr
    
    # 將kv格式的資料還原成陣列形式
    ret = []
    for k, v in dataset.items():
        for i in range(v):
            ret.append(list(k))
    return ret


def mine_freq_lists(root, head_table, min_freq, base, freq_lists):
    # 對head_table排序，按照頻次從小到大排
    frequents = [i[0] for i in sorted(head_table.items(), key=lambda x: x[0])]
    for freq in frequents:
        # base是被列為前提的頻繁項集
        new_base = base.copy()
        # 把當前元素加入頻繁項集
        new_base.add(freq)
        # 加入答案
        freq_lists.append(new_base)
        # 通過FP-tree獲取當前頻繁項集（new_base）為基礎的資料
        new_dataset = regenerate_dataset(head_table, freq)
        # 生成新的head_table
        new_head_table = transform_to_header_table(filter_unfreq_items(new_dataset, min_freq))
        # 如果為空，說明沒有更長的頻繁項集了
        if len(new_head_table) > 0:
            # 如果還有，就構建新的FP-tree
            new_root = create_FP_tree(new_dataset, new_head_table, min_freq)
            # 遞迴挖掘
            mine_freq_lists(new_root, new_head_table, min_freq, new_base, freq_lists)

data_path = 'test_data/mushroom.dat'
def create_dataset(min_freq=3):
    # dataset = {}
    dataset = {}
    # 統計出現數字頻率，存到字典
    # if type(fp) is not list:
    fp = open(data_path, 'r')
    for line in fp.readlines():
        tmp = line.replace('\n', '').split(' ')
        for item in tmp:
            temp_set = list()
            temp_set.append(item)
        temp_set = tuple(temp_set)
        if temp_set in dataset:
            dataset[temp_set]+=1
        else:
            dataset[temp_set]=1
            # dataset.append(temp_set)
            # print(item)
            # if item.isdigit() == True:
            #     item = int(item)
            #     if item in dataset:
            #         dataset[item] += 1
            #     else:
            #         dataset[item] = 1
    freq_dataset = {}
    for i, j in dataset.items():
        if j >= min_freq:
            freq_dataset[i] = j
    fp.close()
    return freq_dataset

if __name__ == "__main__":
    dataset = create_dataset()
    data_dict = filter_unfreq_items(dataset, 3)
    head_table = transform_to_header_table(data_dict)
    root = create_FP_tree(dataset, head_table, 3)
    data = regenerate_dataset(head_table, 'r')
    freq_lists = []
    mine_freq_lists(root, head_table, 3, set([]), freq_lists)
