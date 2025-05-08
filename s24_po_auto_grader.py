from GX import po_main as gx

print('=====================')
print('=====================')
print('=====================')
data_path = 'data.csv'
test_samples_item_id = [{'items_id':[0], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[50], 'date': '24-05-2020', 'time':'8:00:00'},
                   {'items_id':[100], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[125], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[175], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[200], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[250], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[300], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[350], 'date': '25-06-2020', 'time':'8:00:00'},
                   {'items_id':[399], 'date': '25-06-2020', 'time':'8:00:00'}]

def test_single_sample(sample, data_path):
    items_id = sample['items_id']
    date = sample['date']
    time = sample['time']

    results = []
    for i in range(len(items_id)):
        cur_item_id = items_id[i]
        cur_res = gx.RecommendPrice(cur_item_id, data_path, time, date)
        results.append(cur_res)
    return results

def compute_performance(test_samples, data_path):
    raw_res_list = []
    for cur_sample in test_samples:
        cur_res = test_single_sample(cur_sample, data_path)
        raw_res_list.append(cur_res)

    return raw_res_list

def test():
    results = compute_performance(test_samples_item_id, data_path)
    print('============================')
    print('results= ', results)


test()
