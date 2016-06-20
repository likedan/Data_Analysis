from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator

array = [{"price" : 1.13742, "unix_time" : 1463122747},
{
"price" : 1.13743,
"unix_time" : 1463122750
},
{
"price" : 1.13743,
"unix_time" : 1463122751
},
{
"price" : 1.13743,
"unix_time" : 1463122761
},
{
"price" : 1.13743,
"unix_time" : 1463122763
},
{
"price" : 1.13741,
"unix_time" : 1463122771
},
{
"price" : 1.13741,
"unix_time" : 1463122772
},
{
"price" : 1.13743,
"unix_time" : 1463122773
},
{
"price" : 1.1374,
"unix_time" : 1463122775
},
{
"price" : 1.13741,
"unix_time" : 1463122776
},
{
"price" : 1.13742,
"unix_time" : 1463122777
},
{
"price" : 1.13742,
"unix_time" : 1463122780
},
{
"price" : 1.13741,
"unix_time" : 1463122781
},
{
"price" : 1.13742,
"unix_time" : 1463122790
},
{
"price" : 1.13743,
"unix_time" : 1463122791
},
{
"price" : 1.13742,
"unix_time" : 1463122793
}
]

print Helper.get_data_among_intervals(array,[range(0,10),range(10,20),range(20,32)], 60)
