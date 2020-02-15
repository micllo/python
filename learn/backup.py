def loop_rerun_status(std_tasks_record):
    """
    轮询当前的重跑状态
    1.若当前执行结果为<fail>，结束轮询并返回执行结果[重跑失败]
    2.若当前执行结果为<pending>，则根据[details]中的task_id的结果进行判断
    （1）若不存在<pending>状态且rerun_error_log.pkl文件的总数为0，则更新当前执行结果为<success>，结束轮询并返回执行结果[重跑成功]
    （2）若不存在<pending>状态且rerun_error_log.pkl文件的总数不为0，则更新当前执行结果为<partial_fail>，结束轮询并返回执行结果[重跑部分失败]
    （3）若存在<pending>状态，则统计进度条数值（舍去小数部分），并更新当前执行结果的<progress_percent>字段
    :return:
    """
    rerun_record = get_rerun_status_record()
    if rerun_record.get("status") in "fail":
        return "fail"
    if rerun_record.get("status") in "pending":
        error_cnt = pd.read_pickle(RERUN_TASK_ERROR_LOG).to_dict().get("task_id")
        success_cnt = pd.read_pickle(RERUN_TASK_SUCCESS_LOG).to_dict().get("task_id")
        if task_no_pending_status(rerun_record, std_tasks_record):
            if error_cnt == 0:
                update_rerun_status_record({"func_nm": "rerun"}, {"$set": {"status": "success", "ut": now_timestamp()}})
                return "success"
            else:
                update_rerun_status_record({"func_nm": "rerun"}, {"$set": {"status": "parial_fail", "ut": now_timestamp()}})
                return "parial_fail"
        else:
            rerun_status_record = get_rerun_status_record()
            progress_percent = int((float(success_cnt) + float(error_cnt)) / float(rerun_status_record.get("task_cnt")) * 100)
            update_rerun_status_record({"func_nm": "rerun"}, {"$set": {"progress_percent": progress_percent, "done_cnt": success_cnt + error_cnt}})
            print progress_percent


def task_no_pending_status(rerun_record, std_tasks_record):
    """
    判断最后10个重跑任务的总状态
      1.不存在'pending'，则表示重跑成功
      2.只要存在'pending'，则表示正在重跑
    :param rerun_record:
    :return:
    """
    task_id_list = rerun_record.get("details")
    need_std_status = [each_one.get("status") for each_one in std_tasks_record if each_one.get("sin_id") in task_id_list]
    for status in need_std_status:
        if status == "pending":
            return False
    return True


def record_current_rerun_status(all_task_cnt, need_task_list):
    """
    记录当前重跑任务的状态（monitor_func）
    :param all_task_cnt:
    :param need_task_list:
    :return:
    """
    set = dict()
    st = now_timestamp()
    set["ct"] = st
    set["ut"] = st
    set["status"] = "pending"
    set["progress_percent"] = 0
    set["done_cnt"] = 0
    set["task_cnt"] = all_task_cnt
    set["details"] = [item.get("task_id") for item in need_task_list][-10:]
    update = {"$set": set}
    query = {"func_nm": "rerun"}
    update_rerun_status_record(query, update)




def loop_rerun_status(std_tasks_record):
    """
    轮询当前的重跑状态
    1.若当前执行结果为<fail>，结束轮询并返回执行结果[重跑失败]
    2.若当前执行结果为<pending>，则统计当前进度百分比值(舍去小数部分)
    （1）若进度值<100，则更新当前执行结果的<progress_percent、done_cnt、ut>字段，继续轮询
    （2）若进度值=100且rerun_error_log.pkl文件的总数为0，则更新当前执行结果为<success、progress_percent、done_cnt、ut>，结束轮询并返回执行结果[重跑成功]
    （3）若进度值=100且rerun_error_log.pkl文件的总数不为0，则更新当前执行结果为<partial_fail、progress_percent、done_cnt、ut>，结束轮询并返回执行结果[重跑部分失败]
    :return:
    """
    rerun_record = get_rerun_status_record()
    if rerun_record.get("status") in "fail":
        return "fail"
    if rerun_record.get("status") in "pending":
        error_cnt = pd.read_pickle(RERUN_TASK_ERROR_LOG).count().to_dict().get("task_id")
        success_cnt = pd.read_pickle(RERUN_TASK_SUCCESS_LOG).count().to_dict().get("task_id")
        rerun_status_record = get_rerun_status_record()
        progress_percent = int((float(success_cnt) + float(error_cnt)) / float(rerun_status_record.get("task_cnt")) * 100)
        print progress_percent
        print success_cnt + error_cnt

        update_query = {"func_nm": "rerun"}
        update_set = {"progress_percent": progress_percent, "done_cnt": success_cnt + error_cnt, "ut": now_timestamp()}
        if progress_percent < 100:
            update_rerun_status_record(update_query, {"$set": update_set})
        else:
            if error_cnt == 0:
                update_set["status"] = "success"
                print update_set
                update_rerun_status_record(update_query, {"$set": update_set})
                return "success"
            else:
                update_set["status"] = "parial_fail"
                print update_set
                update_rerun_status_record(update_query, {"$set": update_set})
                return "parial_fail"



def get_current_rerun_status_record():
    """
    [ 获取当前重跑状态记录 ] （ monitor_func ）
      1.若当前执行状态为<success、partial_fail>，则直接返回执行结果[成功、部分失败]
      2.若当前执行状态为<fail>，则统计当前进度百分比值(舍去小数部分)
       （1）若进度值<100，则更新当前执行结果的<status=pending、progress_percent、done_cnt、ut>字段，返回执行结果[任务执行中]
       （2）若进度值=100，则更新当前执行结果的<status=fail、progress_percent、done_cnt、ut>字段，返回执行结果[失败]
      3.若当前执行结果为<pending>，则统计当前进度百分比值(舍去小数部分)
       （1）若进度值<100，则更新当前执行结果的<progress_percent、done_cnt、ut>字段，返回执行结果[任务执行中]
       （2）若进度值=100且rerun_error_log.pkl文件的总数为0，则更新当前执行结果为<status=success、progress_percent、done_cnt、ut>，返回执行结果[成功]
       （3）若进度值=100且rerun_error_log.pkl文件的总数不为0，则更新当前执行结果为<status=partial_fail、progress_percent、done_cnt、ut>，返回执行结果[部分失败]
    """
    rerun_status_record = get_rerun_status_record()
    status = rerun_status_record.get("status")
    search_model = rerun_status_record.get("search_model")
    database_id = rerun_status_record.get("database_id")
    std_tasks_record = get_std_tasks_record(search_model=search_model, database_id=database_id)
    if status in ["success", "partial_fail"]:
        return rerun_status_record
    else:
        progress_info = calculation_rerun_progress(rerun_status_record, std_tasks_record)
        update_query = {"func_nm": "rerun"}
        update_set = {"progress_percent": progress_info["percent"], "done_cnt": progress_info["done_cnt"], "ut": now_timestamp()}
        if status in ["fail"]:
            update_set["status"] = "pending" if progress_info["percent"] < 100 else "fail"
        else:  # < status = pending >
            if progress_info["percent"] == 100:
                error_cnt = pd.read_pickle(RERUN_TASK_ERROR_LOG).to_dict().get("task_id")
                update_set["status"] = "success" if error_cnt == 0 else "partial_fail"
        update_rerun_status_record(update_query, {"$set": update_set})
        return get_rerun_status_record()


def calculation_rerun_progress(rerun_status_record, std_tasks_record):
    """
    统计重跑的进度
    1.从重跑状态记录中获取：任务总数量，所有重跑task_id列表
    2.从std_tasks记录匹配所有重跑task_id的status,若status!=pending，则视为已执行完毕
      (注：进度百分比值舍去小数部分)
    """
    progress_info = dict()
    done_cnt = 0
    task_cnt = rerun_status_record.get("task_cnt")
    task_id_list = rerun_status_record.get("details")
    for each_one in std_tasks_record:
        if each_one.get("sin_id") in task_id_list:
            if each_one.get("status") != "pending":
                done_cnt += 1
    percent = int(float(done_cnt) / float(task_cnt) * 100)
    progress_info["done_cnt"] = done_cnt
    progress_info["percent"] = percent
    return progress_info
