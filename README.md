
<html lang="en"><head>
    <meta charset="UTF-8">
    <title></title></head>
<body marginheight="0"><pre><code>
foreword:
		平时运维goldengate时候检查比较麻烦，ggsci，*dsc文件都要看，所以写了这个脚本方便检查
[oracle@myhost ~]$ python ggsdsc.py -help
Usage: python ggsdsc.py [options]
This script prints some info of ogg.
Options:
  -h, --help            show this help message and exit
  -d FROM_DATE, --from_date=FROM_DATE
                        Simple:yyyy-mm-dd hh:mi:ss or yyyy-mm-dd(default 00:00:00)

[oracle@myhost ~]$ python ggsdsc.py

=================Simple_time:2016-07-06 00:00:00~2016-07-06 13:09:38=================

Program   Status    Group     Lag at Chkpt   Time Since Chkpt    Discard count       
EXTRACT   RUNNING   EXT01     00:00:00       00:00:05            0                   
EXTRACT   RUNNING   EDP01     00:00:00       00:00:05            0                   
EXTRACT   RUNNING   EDP02     00:00:00       00:00:05            0                   
EXTRACT   RUNNING   EDP03     00:00:00       00:00:05            0                   
EXTRACT   RUNNING   EDP04     00:00:00       00:00:04            0                   
EXTRACT   RUNNING   EDP05     00:00:00       00:00:05            0                   
REPLICAT  RUNNING   REP01     00:00:00       00:00:05            14                  
REPLICAT  RUNNING   REP02     00:00:00       00:00:00            0                   
REPLICAT  RUNNING   REP03     00:00:00       00:00:00            0                   
REPLICAT  RUNNING   REP04     00:00:00       00:00:05            323                 
REPLICAT  RUNNING   REP05     00:00:00       00:00:06            0                   
REPLICAT  RUNNING   REP06     00:00:03       00:00:00            318                 
REPLICAT  RUNNING   REP07     00:00:00       00:00:00            0</code></pre>
</body></html>