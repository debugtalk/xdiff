import os
import time
import hashlib
from queue import Queue
import yaml
import json
import threading
from . import helpers

files_compare_queue = Queue()
changed_content_dict = {}

def compare_content(origin_data, new_data):
    """ compare contents of two data structure recursively.
    """
    if origin_data == new_data:
        return None

    if type(origin_data) != type(new_data):
        return [origin_data, new_data]

    # compare two lists
    if isinstance(origin_data, list):
        compare_list_result = []
        origin_len = len(origin_data)
        new_len = len(new_data)
        max_list_len = max(origin_len, new_len)
        if origin_len < max_list_len:
            origin_data.extend([None] * (max_list_len - origin_len))
        else:
            new_data.extend([None] * (max_list_len - new_len))

        for idx in range(max_list_len):
            compare_result = compare_content(origin_data[idx], new_data[idx])
            if not compare_result:
                continue
            compare_list_result.append(compare_result)

        return compare_list_result

    # compare two dicts
    elif isinstance(origin_data, dict):
        compare_dict_result = {}
        all_keys_set = set(list(origin_data.keys()) + list(new_data.keys()))

        for key in all_keys_set:
            origin_val = origin_data.get(key, None)
            new_val = new_data.get(key, None)
            compare_result = compare_content(origin_val, new_val)
            if not compare_result:
                continue
            compare_dict_result[key] = compare_result

        return compare_dict_result

    # two values are in the same type, while are in different value
    else:
        return [origin_data, new_data]

def compare_files(origin_file, new_file, file_suffix='.json'):
    """ compare two files, return content difference;
        if no difference exists, return None.
    """
    origin_content = helpers.load_file(origin_file, file_suffix)
    new_content = helpers.load_file(new_file, file_suffix)

    if origin_content['md5'] == new_content['md5']:
        return None

    return compare_content(origin_content['json'], new_content['json'])

def diff_set(origin_set, new_set):

    return {
        'more': new_set - origin_set,
        'less': origin_set - new_set,
        'equal': origin_set & new_set
    }

def worker_compare():
    while True:
        try:
            origin_file, new_file, file_suffix = files_compare_queue.get(block=True, timeout=1)
            helpers.color_logging(
                "Compare file: {} <-> {}".format(origin_file, new_file), "DEBUG")
        except queue.Empty:
            break

        changed_content = compare_files(origin_file, new_file, file_suffix)
        if changed_content:
            filename = os.path.basename(origin_file)
            changed_content_dict[filename] = changed_content

        files_compare_queue.task_done()

def compare_folder_files(origin_folder, new_folder, concurrent_num=10):
    origin_files_set = helpers.load_foler_files(origin_folder)
    new_files_set = helpers.load_foler_files(new_folder)

    diff_result = diff_set(origin_files_set, new_files_set)
    for _file in diff_result['equal']:
        origin_file = os.path.join(origin_folder, _file)
        new_file = os.path.join(new_folder, _file)
        file_suffix = os.path.splitext(_file)[1]
        files_compare_queue.put_nowait((origin_file, new_file, file_suffix))

    for _ in range(concurrent_num):
        thread = threading.Thread(
            target=worker_compare,
            args=()
        )
        thread.start()

    files_compare_queue.join()

    timestamp = int(time.time())
    log_files = {}

    if diff_result['more']:
        log_files['more'] = 'logs/more_{}.yml'.format(timestamp)
        helpers.save_to_yaml(diff_result['more'], log_files['more'])

    if diff_result['less']:
        log_files['less'] = 'logs/less_{}.yml'.format(timestamp)
        helpers.save_to_yaml(diff_result['less'], log_files['less'])

    if changed_content_dict:
        log_files['changed_contents'] = 'logs/changed_contents_{}.yml'.format(timestamp)
        helpers.save_to_yaml(changed_content_dict, log_files['changed_contents'])

    return log_files
