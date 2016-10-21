# _*_ coding: utf-8 _*_

"""
python_lda.py by xianhu
"""

import os
import numpy
import logging
from collections import defaultdict

# 全局变量
MAX_ITER_NUM = 10000    # 最大迭代次数
VAR_NUM = 20            # 自动计算迭代次数时,计算方差的区间大小


class BiDictionary(object):
    """
    定义双向字典,通过key可以得到value,通过value也可以得到key
    """

    def __init__(self):
        """
        :key: 双向字典初始化
        """
        self.dict = {}            # 正向的数据字典,其key为self的key
        self.dict_reversed = {}   # 反向的数据字典,其key为self的value
        return

    def __len__(self):
        """
        :key: 获取双向字典的长度
        """
        return len(self.dict)

    def __str__(self):
        """
        :key: 将双向字典转化为字符串对象
        """
        str_list = ["%s\t%s" % (key, self.dict[key]) for key in self.dict]
        return "\n".join(str_list)

    def clear(self):
        """
        :key: 清空双向字典对象
        """
        self.dict.clear()
        self.dict_reversed.clear()
        return

    def add_key_value(self, key, value):
        """
        :key: 更新双向字典,增加一项
        """
        self.dict[key] = value
        self.dict_reversed[value] = key
        return

    def remove_key_value(self, key, value):
        """
        :key: 更新双向字典,删除一项
        """
        if key in self.dict:
            del self.dict[key]
            del self.dict_reversed[value]
        return

    def get_value(self, key, default=None):
        """
        :key: 通过key获取value,不存在返回default
        """
        return self.dict.get(key, default)

    def get_key(self, value, default=None):
        """
        :key: 通过value获取key,不存在返回default
        """
        return self.dict_reversed.get(value, default)

    def contains_key(self, key):
        """
        :key: 判断是否存在key值
        """
        return key in self.dict

    def contains_value(self, value):
        """
        :key: 判断是否存在value值
        """
        return value in self.dict_reversed

    def keys(self):
        """
        :key: 得到双向字典全部的keys
        """
        return self.dict.keys()

    def values(self):
        """
        :key: 得到双向字典全部的values
        """
        return self.dict_reversed.keys()

    def items(self):
        """
        :key: 得到双向字典全部的items
        """
        return self.dict.items()


class CorpusSet(object):
    """
    定义语料集类,作为LdaBase的基类
    """

    def __init__(self):
        """
        :key: 初始化函数
        """
        # 定义关于word的变量
        self.local_bi = BiDictionary()      # id和word之间的本地双向字典,key为id,value为word
        self.words_count = 0                # 数据集中word的数量（排重之前的）
        self.V = 0                          # 数据集中word的数量（排重之后的）

        # 定义关于article的变量
        self.artids_list = []               # 全部article的id的列表,按照数据读取的顺序存储
        self.arts_Z = []                    # 全部article中所有词的id信息,维数为 M * art.length()
        self.M = 0                          # 数据集中article的数量

        # 定义推断中用到的变量（可能为空）
        self.global_bi = None               # id和word之间的全局双向字典,key为id,value为word
        self.local_2_global = {}            # 一个字典,local字典和global字典之间的对应关系
        return

    def init_corpus_with_file(self, file_name):
        """
        :key: 利用数据文件初始化语料集数据。文件每一行的数据格式: id[tab]word1 word2 word3......
        """
        with open(file_name, "r", encoding="utf-8") as file_iter:
            self.init_corpus_with_articles(file_iter)
        return

    def init_corpus_with_articles(self, article_list):
        """
        :key: 利用article的列表初始化语料集。每一篇article的格式为: id[tab]word1 word2 word3......
        """
        # 清理数据--word数据
        self.local_bi.clear()
        self.words_count = 0
        self.V = 0

        # 清理数据--article数据
        self.artids_list.clear()
        self.arts_Z.clear()
        self.M = 0

        # 清理数据--清理local到global的映射关系
        self.local_2_global.clear()

        # 读取article数据
        for line in article_list:
            frags = line.strip().split()
            if len(frags) < 2:
                continue

            # 获取article的id
            art_id = frags[0].strip()

            # 获取word的id
            art_wordid_list = []
            for word in [w.strip() for w in frags[1:] if w.strip()]:
                local_id = self.local_bi.get_key(word) if self.local_bi.contains_value(word) else len(self.local_bi)

                # 这里的self.global_bi为None和为空是有区别的
                if self.global_bi is None:
                    # 更新id信息
                    self.local_bi.add_key_value(local_id, word)
                    art_wordid_list.append(local_id)
                else:
                    if self.global_bi.contains_value(word):
                        # 更新id信息
                        self.local_bi.add_key_value(local_id, word)
                        art_wordid_list.append(local_id)

                        # 更新local_2_global
                        self.local_2_global[local_id] = self.global_bi.get_key(word)

            # 更新类变量: 必须article中word的数量大于0
            if len(art_wordid_list) > 0:
                self.words_count += len(art_wordid_list)
                self.artids_list.append(art_id)
                self.arts_Z.append(art_wordid_list)

        # 做相关初始计算--word相关
        self.V = len(self.local_bi)
        logging.debug("words number: " + str(self.V) + ", " + str(self.words_count))

        # 做相关初始计算--article相关
        self.M = len(self.artids_list)
        logging.debug("articles number: " + str(self.M))
        return

    def save_wordmap(self, file_name):
        """
        :key: 保存word字典,即self.local_bi的数据
        """
        with open(file_name, "w", encoding="utf-8") as f_save:
            f_save.write(str(self.local_bi))
        return

    def load_wordmap(self, file_name):
        """
        :key: 加载word字典,即加载self.local_bi的数据
        """
        self.local_bi.clear()
        with open(file_name, "r", encoding="utf-8") as f_load:
            for _id, _word in [line.strip().split() for line in f_load if line.strip()]:
                self.local_bi.add_key_value(int(_id), _word.strip())
        self.V = len(self.local_bi)
        return


class LdaBase(CorpusSet):
    """
    LDA模型的基类,相关说明:
    》article的下标范围为[0, self.M), 下标为 m
    》wordid的下标范围为[0, self.V), 下标为 w
    》topic的下标范围为[0, self.K), 下标为 k 或 topic
    》article中word的下标范围为[0, article.size()), 下标为 n
    """

    def __init__(self):
        """
        :key: 初始化函数
        """
        CorpusSet.__init__(self)

        # 基础变量--1
        self.dir_path = ""          # 文件夹路径,用于存放LDA运行的数据、中间结果等
        self.model_name = ""        # LDA训练或推断的模型名称,也用于读取训练的结果
        self.current_iter = 0       # LDA训练或推断的模型已经迭代的次数,用于继续模型训练过程
        self.iters_num = 0          # LDA训练或推断过程中Gibbs抽样迭代的总次数,整数值或者"auto"
        self.topics_num = 0         # LDA训练或推断过程中的topic的数量,即self.K值
        self.K = 0                  # LDA训练或推断过程中的topic的数量,即self.topics_num值
        self.twords_num = 0         # LDA训练或推断结束后输出与每个topic相关的word的个数

        # 基础变量--2
        self.alpha = numpy.zeros(self.K)            # 超参数alpha,K维的float值,默认为50/K
        self.beta = numpy.zeros(self.V)             # 超参数beta,V维的float值,默认为0.01

        # 基础变量--3
        self.Z = []                                 # 所有word的topic信息,即Z(m, n),维数为 M * article.size()

        # 统计计数(可由self.Z计算得到)
        self.nd = numpy.zeros((self.M, self.K))     # nd[m, k]用于保存第m篇article中第k个topic产生的词的个数,其维数为 M * K
        self.ndsum = numpy.zeros((self.M, 1))       # ndsum[m, 0]用于保存第m篇article的总词数,维数为 M * 1
        self.nw = numpy.zeros((self.K, self.V))     # nw[k, w]用于保存第k个topic产生的词中第w个词的数量,其维数为 K * V
        self.nwsum = numpy.zeros((self.K, 1))       # nwsum[k, 0]用于保存第k个topic产生的词的总数,维数为 K * 1

        # 多项式分布参数变量
        self.theta = numpy.zeros((self.M, self.K))  # Doc-Topic多项式分布的参数,维数为 M * K,由alpha值影响
        self.phi = numpy.zeros((self.K, self.V))    # Topic-Word多项式分布的参数,维数为 K * V,由beta值影响

        # 辅助变量,目的是提高算法执行效率
        self.sum_alpha = 0.0                        # 超参数alpha的和
        self.sum_beta = 0.0                         # 超参数beta的和

        # 先验知识,格式为{word_id: [k1, k2, ...], ...}
        self.prior_word = defaultdict(list)

        # 推断时需要的训练模型
        self.train_model = None
        return

    # --------------------------------------------------辅助函数---------------------------------------------------------
    def init_statistics_document(self):
        """
        :key: 初始化关于article的统计计数。先决条件: self.M, self.K, self.Z
        """
        assert self.M > 0 and self.K > 0 and self.Z

        # 统计计数初始化
        self.nd = numpy.zeros((self.M, self.K), dtype=numpy.int)
        self.ndsum = numpy.zeros((self.M, 1), dtype=numpy.int)

        # 根据self.Z进行更新,更新self.nd[m, k]和self.ndsum[m, 0]
        for m in range(self.M):
            for k in self.Z[m]:
                self.nd[m, k] += 1
            self.ndsum[m, 0] = len(self.Z[m])
        return

    def init_statistics_word(self):
        """
        :key: 初始化关于word的统计计数。先决条件: self.V, self.K, self.Z, self.arts_Z
        """
        assert self.V > 0 and self.K > 0 and self.Z and self.arts_Z

        # 统计计数初始化
        self.nw = numpy.zeros((self.K, self.V), dtype=numpy.int)
        self.nwsum = numpy.zeros((self.K, 1), dtype=numpy.int)

        # 根据self.Z进行更新,更新self.nw[k, w]和self.nwsum[k, 0]
        for m in range(self.M):
            for k, w in zip(self.Z[m], self.arts_Z[m]):
                self.nw[k, w] += 1
                self.nwsum[k, 0] += 1
        return

    def init_statistics(self):
        """
        :key: 初始化全部的统计计数。上两个函数的综合函数。
        """
        self.init_statistics_document()
        self.init_statistics_word()
        return

    def sum_alpha_beta(self):
        """
        :key: 计算alpha、beta的和
        """
        self.sum_alpha = self.alpha.sum()
        self.sum_beta = self.beta.sum()
        return

    def calculate_theta(self):
        """
        :key: 初始化并计算模型的theta值(M*K),用到alpha值
        """
        assert self.sum_alpha > 0
        self.theta = (self.nd + self.alpha) / (self.ndsum + self.sum_alpha)
        return

    def calculate_phi(self):
        """
        :key: 初始化并计算模型的phi值(K*V),用到beta值
        """
        assert self.sum_beta > 0
        self.phi = (self.nw + self.beta) / (self.nwsum + self.sum_beta)
        return

    # ---------------------------------------------计算Perplexity值------------------------------------------------------
    def calculate_perplexity(self):
        """
        :key: 计算Perplexity值,并返回
        """
        # 计算theta和phi值
        self.calculate_theta()
        self.calculate_phi()

        # 开始计算
        preplexity = 0.0
        for m in range(self.M):
            for w in self.arts_Z[m]:
                preplexity += numpy.log(numpy.sum(self.theta[m] * self.phi[:, w]))
        return numpy.exp(-(preplexity / self.words_count))

    # --------------------------------------------------静态函数---------------------------------------------------------
    @staticmethod
    def multinomial_sample(pro_list):
        """
        :key: 静态函数,多项式分布抽样,此时会改变pro_list的值
        :param pro_list: [0.2, 0.7, 0.4, 0.1],此时说明返回下标1的可能性大,但也不绝对
        """
        # 将pro_list进行累加
        for k in range(1, len(pro_list)):
            pro_list[k] += pro_list[k-1]

        # 确定随机数 u 落在哪个下标值,此时的下标值即为抽取的类别（random.rand()返回: [0, 1.0)）
        u = numpy.random.rand() * pro_list[-1]

        return_index = len(pro_list) - 1
        for t in range(len(pro_list)):
            if pro_list[t] > u:
                return_index = t
                break
        return return_index

    # ----------------------------------------------Gibbs抽样算法--------------------------------------------------------
    def gibbs_sampling(self, is_calculate_preplexity):
        """
        :key: LDA模型中的Gibbs抽样过程
        :param is_calculate_preplexity: 是否计算preplexity值
        """
        # 计算preplexity值用到的变量
        pp_list = []
        pp_var = numpy.inf

        # 开始迭代
        last_iter = self.current_iter + 1
        iters_num = self.iters_num if self.iters_num != "auto" else MAX_ITER_NUM
        for self.current_iter in range(last_iter, last_iter+iters_num):
            info = "......"

            # 是否计算preplexity值
            if is_calculate_preplexity:
                pp = self.calculate_perplexity()
                pp_list.append(pp)

                # 计算列表最新VAR_NUM项的方差
                pp_var = numpy.var(pp_list[-VAR_NUM:]) if len(pp_list) >= VAR_NUM else numpy.inf
                info = (", preplexity: " + str(pp)) + ((", var: " + str(pp_var)) if len(pp_list) >= VAR_NUM else "")

            # 输出Debug信息
            logging.debug("\titeration " + str(self.current_iter) + info)

            # 判断是否跳出循环
            if self.iters_num == "auto" and pp_var < (VAR_NUM / 2):
                break

            # 对每篇article的每个word进行一次抽样,抽取合适的k值
            for m in range(self.M):
                for n in range(len(self.Z[m])):
                    w = self.arts_Z[m][n]
                    k = self.Z[m][n]

                    # 统计计数减一
                    self.nd[m, k] -= 1
                    self.ndsum[m, 0] -= 1
                    self.nw[k, w] -= 1
                    self.nwsum[k, 0] -= 1

                    if self.prior_word and (w in self.prior_word):
                        # 带有先验知识,否则进行正常抽样
                        k = numpy.random.choice(self.prior_word[w])
                    else:
                        # 计算theta值--下边的过程为抽取第m篇article的第n个词w的topic,即新的k
                        theta_p = (self.nd[m] + self.alpha) / (self.ndsum[m, 0] + self.sum_alpha)

                        # 计算phi值--判断是训练模型,还是推断模型（注意self.beta[w_g]）
                        if self.local_2_global and self.train_model:
                            w_g = self.local_2_global[w]
                            phi_p = (self.train_model.nw[:, w_g] + self.nw[:, w] + self.beta[w_g]) / \
                                    (self.train_model.nwsum[:, 0] + self.nwsum[:, 0] + self.sum_beta)
                        else:
                            phi_p = (self.nw[:, w] + self.beta[w]) / (self.nwsum[:, 0] + self.sum_beta)

                        # multi_p为多项式分布的参数,此时没有进行标准化
                        multi_p = theta_p * phi_p

                        # 此时的topic即为Gibbs抽样得到的topic,它有较大的概率命中多项式概率大的topic
                        k = LdaBase.multinomial_sample(multi_p)

                    # 统计计数加一
                    self.nd[m, k] += 1
                    self.ndsum[m, 0] += 1
                    self.nw[k, w] += 1
                    self.nwsum[k, 0] += 1

                    # 更新Z值
                    self.Z[m][n] = k
        # 抽样完毕
        return

    # -----------------------------------------Model数据存储、读取相关函数-------------------------------------------------
    def save_parameter(self, file_name):
        """
        :key: 保存模型相关参数数据,包括: topics_num, M, V, K, words_count, alpha, beta
        """
        with open(file_name, "w", encoding="utf-8") as f_param:
            for item in ["topics_num", "M", "V", "K", "words_count"]:
                f_param.write("%s\t%s\n" % (item, str(self.__dict__[item])))
            f_param.write("alpha\t%s\n" % ",".join([str(item) for item in self.alpha]))
            f_param.write("beta\t%s\n" % ",".join([str(item) for item in self.beta]))
        return

    def load_parameter(self, file_name):
        """
        :key: 加载模型相关参数数据,和上一个函数相对应
        """
        with open(file_name, "r", encoding="utf-8") as f_param:
            for line in f_param:
                key, value = line.strip().split()
                if key in ["topics_num", "M", "V", "K", "words_count"]:
                    self.__dict__[key] = int(value)
                elif key in ["alpha", "beta"]:
                    self.__dict__[key] = numpy.array([float(item) for item in value.split(",")])
        return

    def save_zvalue(self, file_name):
        """
        :key: 保存模型关于article的变量,包括: arts_Z, Z, artids_list等
        """
        with open(file_name, "w", encoding="utf-8") as f_zvalue:
            for m in range(self.M):
                out_line = [str(w) + ":" + str(k) for w, k in zip(self.arts_Z[m], self.Z[m])]
                f_zvalue.write(self.artids_list[m] + "\t" + " ".join(out_line) + "\n")
        return

    def load_zvalue(self, file_name):
        """
        :key: 读取模型的Z变量。和上一个函数相对应
        """
        self.arts_Z = []
        self.artids_list = []
        self.Z = []
        with open(file_name, "r", encoding="utf-8") as f_zvalue:
            for line in f_zvalue:
                frags = line.strip().split()
                art_id = frags[0].strip()
                w_k_list = [value.split(":") for value in frags[1:]]
                # 添加到类中
                self.artids_list.append(art_id)
                self.arts_Z.append([int(item[0]) for item in w_k_list])
                self.Z.append([int(item[1]) for item in w_k_list])
        return

    def save_twords(self, file_name):
        """
        :key: 保存模型的twords数据,要用到phi的数据
        """
        self.calculate_phi()
        out_num = self.V if self.twords_num > self.V else self.twords_num
        with open(file_name, "w", encoding="utf-8") as f_twords:
            for k in range(self.K):
                words_list = sorted([(w, self.phi[k, w]) for w in range(self.V)], key=lambda x: x[1], reverse=True)
                f_twords.write("Topic %dth:\n" % k)
                f_twords.writelines(["\t%s %f\n" % (self.local_bi.get_value(w), p) for w, p in words_list[:out_num]])
        return

    def load_twords(self, file_name):
        """
        :key: 加载模型的twords数据,即先验数据
        """
        self.prior_word.clear()
        topic = -1
        with open(file_name, "r", encoding="utf-8") as f_twords:
            for line in f_twords:
                if line.startswith("Topic"):
                    topic = int(line.strip()[6:-3])
                else:
                    word_id = self.local_bi.get_key(line.strip().split()[0].strip())
                    self.prior_word[word_id].append(topic)
        return

    def save_tag(self, file_name):
        """
        :key: 输出模型最终给数据打标签的结果,用到theta值
        """
        self.calculate_theta()
        with open(file_name, "w", encoding="utf-8") as f_tag:
            for m in range(self.M):
                f_tag.write("%s\t%s\n" % (self.artids_list[m], " ".join([str(item) for item in self.theta[m]])))
        return

    def save_model(self):
        """
        :key: 保存模型数据
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # 保存训练结果
        self.save_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.save_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.save_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))

        #保存额外数据
        self.save_twords(os.path.join(self.dir_path, "%s.%s" % (name_predix, "twords")))
        self.save_tag(os.path.join(self.dir_path, "%s.%s" % (name_predix, "tag")))
        return

    def load_model(self):
        """
        :key: 加载模型数据
        """
        name_predix = "%s-%05d" % (self.model_name, self.current_iter)

        # 加载训练结果
        self.load_parameter(os.path.join(self.dir_path, "%s.%s" % (name_predix, "param")))
        self.load_wordmap(os.path.join(self.dir_path, "%s.%s" % (name_predix, "wordmap")))
        self.load_zvalue(os.path.join(self.dir_path, "%s.%s" % (name_predix, "zvalue")))
        return


class LdaModel(LdaBase):
    """
    LDA模型定义,主要实现训练、继续训练、推断的过程
    """

    def init_train_model(self, dir_path, model_name, current_iter, iters_num=None, topics_num=10, twords_num=200,
                         alpha=-1.0, beta=0.01, data_file="", prior_file=""):
        """
        :key: 初始化训练模型,根据参数current_iter（是否等于0）决定是初始化新模型,还是加载已有模型
        :key: 当初始化新模型时,除了prior_file先验文件外,其余所有的参数都需要,且current_iter等于0
        :key: 当加载已有模型时,只需要dir_path, model_name, current_iter（不等于0）, iters_num, twords_num即可
        :param iters_num: 可以为整数值或者“auto”
        """
        if current_iter == 0:
            logging.debug("init a new train model")

            # 初始化语料集
            self.init_corpus_with_file(data_file)

            # 初始化部分变量
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.topics_num = topics_num
            self.K = topics_num
            self.twords_num = twords_num

            # 初始化alpha和beta
            self.alpha = numpy.array([alpha if alpha > 0 else (50.0/self.K) for k in range(self.K)])
            self.beta = numpy.array([beta if beta > 0 else 0.01 for w in range(self.V)])

            # 初始化Z值,以便统计计数
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]
        else:
            logging.debug("init an existed model")

            # 初始化部分变量
            self.dir_path = dir_path
            self.model_name = model_name
            self.current_iter = current_iter
            self.iters_num = iters_num
            self.twords_num = twords_num

            # 加载已有模型
            self.load_model()

        # 初始化统计计数
        self.init_statistics()

        # 计算alpha和beta的和值
        self.sum_alpha_beta()

        # 初始化先验知识
        if prior_file:
            self.load_twords(prior_file)

        # 返回该模型
        return self

    def begin_gibbs_sampling_train(self, is_calculate_preplexity=True):
        """
        :key: 训练模型,对语料集中的所有数据进行Gibbs抽样,并保存最后的抽样结果
        """
        # Gibbs抽样
        logging.debug("sample iteration start, iters_num: " + str(self.iters_num))
        self.gibbs_sampling(is_calculate_preplexity)
        logging.debug("sample iteration finish")

        # 保存模型
        logging.debug("save model")
        self.save_model()
        return

    def init_inference_model(self, train_model):
        """
        :key: 初始化推断模型
        """
        self.train_model = train_model

        # 初始化变量: 主要用到self.topics_num, self.K
        self.topics_num = train_model.topics_num
        self.K = train_model.K

        # 初始化变量self.alpha, self.beta,直接沿用train_model的值
        self.alpha = train_model.alpha      # K维的float值,训练和推断模型中的K相同,故可以沿用
        self.beta = train_model.beta        # V维的float值,推断模型中用于计算phi的V值应该是全局的word的数量,故可以沿用
        self.sum_alpha_beta()               # 计算alpha和beta的和

        # 初始化数据集的self.global_bi
        self.global_bi = train_model.local_bi
        return

    def inference_data(self, article_list, iters_num=100, repeat_num=3):
        """
        :key: 利用现有模型推断数据
        :param article_list: 每一行的数据格式为: id[tab]word1 word2 word3......
        :param iters_num: 每一次迭代的次数
        :param repeat_num: 重复迭代的次数
        """
        # 初始化语料集
        self.init_corpus_with_articles(article_list)

        # 初始化返回变量
        return_theta = numpy.zeros((self.M, self.K))

        # 重复抽样
        for i in range(repeat_num):
            logging.debug("inference repeat_num: " + str(i+1))

            # 初始化变量
            self.current_iter = 0
            self.iters_num = iters_num

            # 初始化Z值,以便统计计数
            self.Z = [[numpy.random.randint(self.K) for n in range(len(self.arts_Z[m]))] for m in range(self.M)]

            # 初始化统计计数
            self.init_statistics()

            # 开始推断
            self.gibbs_sampling(is_calculate_preplexity=False)

            # 计算theta
            self.calculate_theta()
            return_theta += self.theta

        # 计算结果,并返回
        return return_theta / repeat_num


if __name__ == "__main__":
    """
    测试代码
    """
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    # train或者inference
    test_type = "train"
    # test_type = "inference"

    # 测试新模型
    if test_type == "train":
        model = LdaModel()
        # 由prior_file决定是否带有先验知识
        model.init_train_model("data/", "model", current_iter=0, iters_num="auto", topics_num=10, data_file="corpus.txt")
        # model.init_train_model("data/", "model", current_iter=0, iters_num="auto", topics_num=10, data_file="corpus.txt", prior_file="prior.twords")
        model.begin_gibbs_sampling_train()
    elif test_type == "inference":
        model = LdaModel()
        model.init_inference_model(LdaModel().init_train_model("data/", "model", current_iter=134))
        data = [
            "cn	咪咕 漫画 咪咕 漫画 漫画 更名 咪咕 漫画 资源 偷星 国漫 全彩 日漫 实时 在线看 随心所欲 登陆 漫画 资源 黑白 全彩 航海王",
            "co	aircloud aircloud 硬件 设备 wifi 智能 手要 平板电脑 电脑 存储 aircloud 文件 远程 型号 aircloud 硬件 设备 wifi"
        ]
        result = model.inference_data(data)

    # 退出程序
    exit()
