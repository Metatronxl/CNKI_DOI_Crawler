#!/bin/bash
if [ $# -ne 1 ];then
 echo "Usage:$0 filename"
 exit 1
fi
file=$1
if [ ! -f $file ];then
 echo "the $file is not a file"
 exit 2
fi

work_path=$(dirname $0)


count=0
while read line   #使用read命令循环读取文件内容，并将读取的文件内容赋值给变量line
do
  let count++
  echo " start tcpdump process, NO:$count DOI number:$line"
  nohup tcpdump -w $work_path/data/$count.pcap &
  sleep 1s
  nohup /Users/xulei2/Documents/tmpFile/Paper/IIOT/handle/handle-client-9.3.0/bin/hdl-qresolver $line > $work_path/data/$count.txt &
  sleep 5s # 确保所有的数据均已经获取到
  #杀死tcpdump进程
  ps -ef |grep tcpdump |awk '{print $2}'|xargs kill -9

done <$file      #“done <$file”将整个while循环的标准输入指向文件$file
echo -e "\ntotle $count lines read"
exit 0