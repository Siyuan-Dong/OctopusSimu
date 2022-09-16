import simpy
import numpy as np
from numpy import random
# import matplotlib.pyplot as plt
# import seaborn as sns

print(1085552526864898172692696872008>>80)
# import Sketches
# sketches=Sketches.Sketches()
# # id = sketches.TUPLES(4000,0,0,0,0)
# id = 4000<<72

# src_ip = id>>72
# dst_ip = id>>40 & 0xffffffff
# src_port = (id>>24) & 0xffff
# dst_port = (id>>8) & 0xffff
# _proto = id & 0xff

# for i in range(0,50):
#     # id = Sketches.Sketches.TUPLES(100,0,0,0,0)
#     # id = sketches.TUPLES(4000,0,0,0,0)
#     sketches.insketch[3].insert_pre(src_ip,dst_ip,src_port,dst_port,_proto)
# ab_fgroup = set(sketches.ab_fg())
# print(ab_fgroup)

# def subnet(flow_id):
#     return flow_id>>8

# def convert(x):
#     res = x.srcIP_dstIP()
#     res = (res<<16)+x.srcPort()
#     res = (res<<16)+x.dstPort()
#     res = (res<<8)+x.proto()
#     return res

# def converts(xs):
#     ress = []
#     for x in xs:
#         res = convert(x)
#         ress.append(res)
#     return ress


# if subnet(src_ip) in ab_fgroup:
#     print("insert core",src_ip,subnet(src_ip))
#     sketches.coresketch[2].insert_pre(src_ip,dst_ip,src_port,dst_port,_proto)
#     sketches.update_core_key(src_ip,dst_ip,src_port,dst_port,_proto)

# tmp=sketches.get_ab_fs()
# print(tmp)
# # lala = converts(sketches.ab_fs)
# # la = convert(id)
# # print(la in lala)
# # if la in lala:
# #     print(sketches.coresketch[2].query(id))

# sketches.Clear()



# id = sketches.TUPLES(4000,0,0,0,0)
# for i in range(0,50):
#     # id = Sketches.Sketches.TUPLES(100,0,0,0,0)
#     # id = sketches.TUPLES(4000,0,0,0,0)
#     sketches.insketch[3].insert(id,1)
# ab_fgroup = set(sketches.ab_fg())
# print(ab_fgroup)

# if subnet(id.srcIP()) in ab_fgroup:
#     print("insert core",id.srcIP(),subnet(id.srcIP()))
#     sketches.coresketch[2].insert(id)
#     sketches.update_core_key(id)

# lala = converts(sketches.ab_fs)
# la = convert(id)
# print(la in lala)
# if la in lala:
#     print(sketches.coresketch[2].query(id))

# sketches.Clear()


# a = 1<<80
# print(type(a))





# print(sketches.insketch[3].Query(100))
# sketches.Clear()
# print(sketches.insketch[3].Query(100))


# def cal_gp(src):
#     k=4
#     pod = (src-20)//(k*k//4)
#     lala = k*k//4 + k*pod + k//2 + (src-20-pod*k*k//4)//(k//2)
#     return lala

# for i in range(20,36):
#     print(cal_gp(i))

# a=[1,2,3,4]
# print(2 in a)


# li = []
# li.append(1)
# li.append("x")
# li.append(1.23)
# print(li)

a = 16+(1<<3)
print((a>>3)&1)
if((a>>3)&1):
        print("lala")
