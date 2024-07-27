import pickle


def load_single_pkl(file_path):
    # file_path = "./neusis_14deg_planeFull/Data/51.pkl"
    with open(file_path, 'rb') as file:
        # 反序列化文件，恢复原始对象
        data = pickle.load(file)
        # for key in data:
        #     # print(key)
        #     print(key, data[key].shape)
        return data


def save_single_pkl(output_path, object_to_save):
    # 将字典保存为 .pkl 文件
    with open(output_path, 'wb') as f:  # 'wb' 模式以二进制写入
        pickle.dump(object_to_save, f)
    print(f"Dictionary has been successfully saved to {output_path}.")
