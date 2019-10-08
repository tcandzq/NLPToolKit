#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 15:33
# @Author  : tc
# @File    : utils.py
import re

import pypinyin
from pypinyin import pinyin
from langconv import Converter

def edit_distance_word(word, char_set):
    """
    all edits that are one edit away from 'word'
    :param word:
    :param char_set:
    :return:
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in char_set]
    return set(transposes + replaces)


def get_sub_array(nums):
    """
    取所有连续子串，
    [0, 1, 2, 5, 7, 8]
    => [[0, 3], 5, [7, 9]]
    :param nums: sorted(list)
    :return:
    """
    ret = []
    ii = 0
    for i, c in enumerate(nums):
        if i == 0:
            pass
        elif i <= ii:
            continue
        elif i == len(nums) - 1:
            ret.append([c])
            break
        ii = i
        cc = c
        # get continuity Substring
        while ii < len(nums) - 1 and nums[ii + 1] == cc + 1:
            ii = ii + 1
            cc = cc + 1
        if ii > i:
            ret.append([c, nums[ii] + 1])
        else:
            ret.append([c])
    return ret

def find_all_idx2(lst, item):
    """
    取列表中指定元素的所有下标
    :param lst: 列表或字符串
    :param item: 指定元素
    :return: 下标列表
    """
    ids = []
    for i in range(len(lst)):
        if item == lst[i]:
            ids.append(i)
    return ids

def find_all_idx(lst, item):
    """
    取列表中指定元素的所有下标
    :param lst: 列表或字符串
    :param item: 指定元素
    :return: 下标列表
    """
    ids = []
    pos = -1
    for i in range(lst.count(item)):
        pos = lst.index(item, pos + 1)
        if pos > -1:
            ids.append(pos)
    return ids

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if '\u4e00' <= uchar <= '\u9fa5':
        return True
    else:
        return False


def is_chinese_string(string):
    """判断是否全为汉字"""
    for c in string:
        if not is_chinese(c):
            return False
    return True


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'u0030' <= uchar <= u'u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'u0041' <= uchar <= u'u005a') or (u'u0061' <= uchar <= u'u007a'):
        return True
    else:
        return False


def is_alphabet_string(string):
    """判断是否全部为英文字母"""
    for c in string:
        if c < 'a' or c > 'z':
            return False
    return True


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def B2Q(uchar):
    """半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()


def remove_punctuation(strs):
    """
    去除标点符号
    :param strs:
    :return:
    """
    return re.sub("[\s+\.\!\/<>“”,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", strs.strip())


def traditional2simplified(sentence):
    """
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    """
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


def simplified2traditional(sentence):
    """
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    """
    sentence = Converter('zh-hant').convert(sentence)
    return sentence


def get_homophones_by_char(input_char):
    """
    根据汉字取同音字
    :param input_char:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.NORMAL)[0][0] == pinyin(input_char, style=pypinyin.NORMAL)[0][0]:
            result.append(chr(i))
    return result


def get_homophones_by_pinyin(input_pinyin):
    """
    根据拼音取同音字
    :param input_pinyin:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == input_pinyin:
            # TONE2: 中zho1ng
            result.append(chr(i))
    return result


if __name__ == '__main__':
    l = [1, 2, 3, 4, 2, 3, 4]
    item = 2
    print(find_all_idx(l, item))

    l = '我爱中国，我是中国人'
    item = '中国'
    print(find_all_idx(l, item))