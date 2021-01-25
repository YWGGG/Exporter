## Snort_hwk
### 使用方法:
1、namesort.txt文件中按行存放学生的  ```学号 + github account name```  (例如```205255 fleetpip```)。 

学生需要在自己的github上新建两个repository(idshwk1和idshwk2)，idshwk1存放第一次作业的test.rules，idshwk2存放第二次作业的test.rules。


2、在root下，运行```python3 readHomeWork.py -i 1```和```python3 readHomeWork.py -i 2```，获取学生的两次作业。

两次作业分别保存在当前目录下的idshwk1和idshwk2中(每个学生的作业以学号标识)。


3、然后在root下，运行```python3 evalHomeWokr.py -i 1 ```评估第一次作业，成绩保存在scores.xls的IDS Course Score hwk1分表中，将其导出。

再运行```python3 evalHomeWokr.py -i 2```评估第二次作业，成绩保存在scores.xls的IDS Course Score hwk2分表中，将其导出。
