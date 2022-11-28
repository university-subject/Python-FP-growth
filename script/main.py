def filter_unfreq_items(fp,min_freq):
    dataset = {}
    # 統計出現數字頻率，存到字典
    if type(fp) is not list:
        fp = open('mushroom.dat', 'r')
        for line in fp.readlines():
            tmp = line.split(' ')
            del tmp[-1]
            for item in tmp:
                # print(item)
                if item.isdigit() == True:
                    item = int(item)
                    if item in dataset:
                        dataset[item] += 1
                    else:
                        dataset[item] = 1
        freq_dataset = {}
        for i, j in dataset.items():
            if j >= min_freq:
                freq_dataset[i] = j
        fp.close()
        return freq_dataset
    elif type(fp) is list:
        for item in fp:
            print(item)
            if item.isdigit() == True:
                item = int(item)
                if item in dataset:
                    dataset[item] += 1
                else:
                    dataset[item] = 1
        freq_dataset = {}
        for i, j in dataset.items():
            if j >= min_freq:
                freq_dataset[i] = j
        return freq_dataset   


def dataset_to_header_table(dataset):
    # value: list[0]:freq,list[1]:NULL pointer
    return {i: [j, None] for i, j in dataset.items()}

def filter_sort_row_data(row_data, freq_dataset):
    filter_data = {}
    for item in row_data:
        item = int(item)
        # 留下出現頻率高的數字
        if item in freq_dataset:
            filter_data[item] = freq_dataset[item]
    sort_dict = {}
    # 根據出現頻率由高到低排序
    sort_dict = sorted(filter_data.items(), key=lambda x: x[1], reverse=True)
    # 回傳排序過的數字list
    return [i[0] for i in sort_dict]

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

def up_forward(node):
    path = []
    while node.father is not None:
        path.append(node)
        node = node.father
        # 過濾樹根
        return path

def insert_table(head_node, node):
    while head_node.ptr is not None:
        head_node = head_node.ptr
    head_node.ptr = node

def create_FP_tree(fp,header_table, min_freq):
    freq_dataset = filter_unfreq_items(fp,min_freq)
    root = Node('Null', 0, None)
    # print(type(fp) is not list)
    if type(fp) is not list:
        fp = open('mushroom.dat', 'r')
        for line in fp.readlines():
            tmp = line.split(' ')
            del tmp[-1]
            # 根據整體出現次數進行排序
            row_data = filter_sort_row_data(tmp, freq_dataset)
            head = root
            # 按照排序順序依次往樹上插入
            for item in row_data:
                # print(item)
                if item in head.children:
                    head = head.children[item]
                else:
                    new_node = Node(item, 0, head)
                    head.add_child(new_node)
                    # 頭指標指向的位置為空，那麼我們直接讓頭指標指向當前位置
                    if header_table[item][1] is None:
                        header_table[item][1] = new_node
                    else:
                        # 否則的話，我們將當前元素新增到連結串列的末尾
                        insert_table(header_table[item][1], new_node)
                    head = new_node
                head.update_freq()
        return root
    elif type(fp) is list:
        print(fp)
        row_data = filter_sort_row_data(tmp, freq_dataset)
        head = root
        # 按照排序順序依次往樹上插入
        for item in row_data:
            print(item)
            if item in head.children:
                head = head.children[item]
            else:
                new_node = Node(item, 0, head)
                head.add_child(new_node)
                # 頭指標指向的位置為空，那麼我們直接讓頭指標指向當前位置
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    # 否則的話，我們將當前元素新增到連結串列的末尾
                    insert_table(header_table[item][1], new_node)
                head = new_node
            head.update_freq()
        return root

def regenerate_dataset(header_table, item):
    dataset = {}
    if item not in header_table:
        return dataset
    # 通過head_table找到連結串列的起始位置
    node = header_table[item][1]
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

def mine_freq_lists(root, header_table, min_freq, base, freq_lists):
    # 對head_table排序，按照頻次從小到大排
    frequents = [i[0] for i in sorted(header_table.items(), key=lambda x: x[0])]
    # print(frequents)
    for freq in frequents:
        # print(freq)
        # base是被列為前提的頻繁項集
        new_base = base.copy()
        # 把當前元素加入頻繁項集
        new_base.add(freq)
        # 加入答案
        freq_lists.append(new_base)
        # 通過FP-tree獲取當前頻繁項集（new_base）為基礎的資料
        new_dataset = regenerate_dataset(header_table, freq)
        # 生成新的head_table
        new_head_table = dataset_to_header_table(filter_unfreq_items(new_dataset, min_freq))
        # 如果為空，說明沒有更長的頻繁項集了
        if len(new_head_table) > 0:
            # 如果還有，就構建新的FP-tree
            new_root = create_FP_tree(new_dataset, new_head_table, min_freq)
            # 遞迴挖掘
            mine_freq_lists(new_root, new_head_table, min_freq, new_base, freq_lists)


if __name__ == '__main__':
    # fp = [line.split(' ') for line in open('mushroom.dat','r').readlines()]
    min_freq = 813
    freq_dataset = {}
    freq_dataset = filter_unfreq_items(None,min_freq)
    # print(freq_dataset)
    header_table = {}
    header_table = dataset_to_header_table(freq_dataset)
    # print(header_table)
    root = create_FP_tree(None,header_table, min_freq)
    # data = {}
    # data = regenerate_dataset(header_table, 65)
    freq_lists = []
    mine_freq_lists(root, header_table, min_freq, set([]), freq_lists)

    for l in range(1,6):
        count=0
        for i in freq_lists:
            if len(i) == l:
                count+=1
        print('L^',l,'=',count)

    print(len(freq_lists))

    # with open('mushroom.dat', 'r') as fp:
    #     for line in fp.readlines():
    #         tmp = line.split(' ')
    #         # del '\n'
    #         del tmp[-1]
    #         row_data = filter_sort_row_data(tmp, freq_dataset)
    #         # print(row_data)
