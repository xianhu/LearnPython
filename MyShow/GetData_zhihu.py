# _*_ coding: utf-8 _*_

import pymysql

con = pymysql.connect(host="xxxx", user="root", passwd="xxxx", db="xxxx", charset="utf8")
cursor = con.cursor()
con.autocommit(1)


def get_all_topics():
    cursor.execute("select distinct t_topic_id, t_topic_name from t_zhihutopics where t_topic_haschildren = 1;")
    return [item for item in cursor.fetchall() if item[0].strip()]


def get_topic_data(topic_id, topic_name):
    data_dict = {
        "type": "force",
        "nodes": [
            {"id": topic_id, "name": topic_name, "level": 0}
        ],
        "links": []
    }

    nodes_set = set([topic_id])
    dai_ids = set([topic_id])
    while dai_ids:
        cursor.execute("select * from t_zhihutopics where t_topic_parentid = %s;", [dai_ids.pop()])
        for item in cursor.fetchall():
            _, t_id, t_name, t_pid, t_haschild, _ = item

            if t_id not in nodes_set:
                nodes_set.add(t_id)
                data_dict["nodes"].append({"id": t_id, "name": t_name, "level": 1 if t_pid == topic_id else 2})
            data_dict["links"].append({"source": t_pid, "target": t_id})

            if t_haschild == 1:
                dai_ids.add(t_id)
    return data_dict
