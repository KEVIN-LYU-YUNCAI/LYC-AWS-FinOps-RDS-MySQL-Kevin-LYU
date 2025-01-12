# name: lambda_function.py
# version: 1.0
"""
AWS Lambda 处理函数，用于导出指定日期范围内的日志到 S3 存储桶。
此函数接收一个事件和一个上下文对象作为参数。事件对象包含触发此函数的事件数据，上下文对象提供有关运行时环境的信息。

函数执行以下操作：
1. 创建一个 CloudWatch Logs 客户端。
2. 使用 create_export_task 方法创建一个导出任务，将指定日期范围内的日志导出到指定的 S3 存储桶中。
   - logGroupName: 指定要导出的日志组名称。
   - fromTime: 指定导出任务的开始时间。
   - toTime: 指定导出任务的结束时间。
   - destination: 指定目标 S3 存储桶。
   - destinationPrefix: 指定目标存储桶中的前缀。
3.函数打印成功信息和响应，并返回响应对象。

详情请参考
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_export_task.html
https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateExportTask.html#CWL-CreateExportTask-request-taskName
"""
import boto3
import os
import datetime

# 从lambda环境变量中获取日志组名称,目标存储桶名称,日志前缀,天数
# LOG_GROUP_NAME = os.environ['LOG_GROUP_NAME']
# DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']
# PREFIX = os.environ['PREFIX']
# NDAYS = os.environ['NDAYS']

LOG_GROUP_NAME = "/aws/rds/instance/kevin-rds/audit" #改成你自己的cloudwatch logs路径名
DESTINATION_BUCKET = "kevin-rds-mysql-audit-logs-bucket" #改成你自己的bucket名
PREFIX = "kevin-rds-mysql-audit-logs"
NDAYS = 1 #以几天为周期分割日志

# 将天数转换为整数
nDays = int(NDAYS)
# 获取当前时间
currentTime = datetime.datetime.now()

# 计算开始日期
StartDate = currentTime - datetime.timedelta(days=nDays)
# 计算结束日期
EndDate = currentTime - datetime.timedelta(days=nDays - 1)
# 将开始日期转换为时间戳（毫秒）
fromTime = int(StartDate.timestamp() * 1000)
# 将结束日期转换为时间戳（毫秒）
toTime = int(EndDate.timestamp() * 1000)
# 构建存储桶前缀
BUCKET_PREFIX = os.path.join(PREFIX, StartDate.strftime('%Y%m%d').format(os.path.sep))


def lambda_handler(event, context):
    """
    AWS Lambda 处理函数，用于导出指定日期范围内的日志到 S3 存储桶。

    参数:
    event (dict): 包含触发此函数的事件数据的字典。
    context (object): 提供关于运行时环境的信息的对象。

    返回:
    dict: 包含成功状态的字典。
    """
    # 创建 CloudWatch Logs 客户端
    client = boto3.client('logs')
    # 创建导出任务

    response = client.create_export_task(
        # 指定日志组名称
        logGroupName=LOG_GROUP_NAME,
        # 指定开始时间
        fromTime=fromTime,
        # 指定结束时间
        to=toTime,
        # 指定目标存储桶
        destination=DESTINATION_BUCKET,
        # 指定目标存储桶中的前缀
        destinationPrefix=BUCKET_PREFIX
    )
    
    # 打印成功信息
    print("Successful")
    print(response)
    
    # 返回成功状态
    return response

# 添加一个 main 主体，用于本地测试
if __name__ == "__main__":
    # 调用 lambda_handler 函数
    lambda_handler(event, context)