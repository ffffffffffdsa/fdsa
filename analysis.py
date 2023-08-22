import pickle
from datetime import timedelta, datetime

with open("data.pickle","rb") as fr:
    data = pickle.load(fr)

rank = data["rank"]
idrank = {}

for x in rank:
    nick = x.split('(')[0]
    id = x.split('(')[1][:-1]

    if id not in idrank:
        idrank[id] = {}
        idrank[id]["nicks"] = set()
        idrank[id]["article"] = 0
        idrank[id]["reply"] = 0

    idrank[id]["article"] += int(rank[x]["article"])
    idrank[id]["reply"] += int(rank[x]["reply"])
    if nick[-2:]!='..':
        idrank[id]["nicks"].add(nick)

for id in idrank:
    idrank[id]["score"] = idrank[id]["article"]*3+idrank[id]["reply"]

sortByArticle = sorted(idrank.items(),key = lambda x:x[1]["article"],reverse=True)

rank=1
for i in range(len(sortByArticle)):
    x=sortByArticle[i]
    if i!=0 and sortByArticle[i-1][1]["article"]!=sortByArticle[i][1]["article"]:
        rank+=1
    idrank[x[0]]["articleRank"] = rank

sortByReply = sorted(idrank.items(),key = lambda x:x[1]["reply"],reverse=True)

rank=1
for i in range(len(sortByReply)):
    x=sortByReply[i]
    if i!=0 and sortByReply[i-1][1]["reply"]!=sortByReply[i][1]["reply"]:
        rank+=1
    idrank[x[0]]["replyRank"] = rank

sortByScore = sorted(idrank.items(),key = lambda x:x[1]["score"],reverse=True)

rank=1
i=0
startdate = (data["date"]-timedelta(days=1)).strftime('%Y/%m/%d %H:%M:%S')
enddate = data["date"].strftime('%Y/%m/%d %H:%M:%S')
print("집계 기간 : "+startdate+"~"+enddate)
print()

for i in range(len(sortByScore)):
    x=sortByScore[i]
    if i!=0 and sortByScore[i-1][1]["score"]!=sortByScore[i][1]["score"]:
        rank+=1
    print(rank,"등 : ",sep='',end='')

    comma=False
    for k in x[1]["nicks"]:
        if (comma):
            print(",",end='')
        else:
            comma=True
        print(k,end='')
    print("("+x[0]+")",end='')
    print(" | ","글 ",x[1]["article"],"개(",x[1]["articleRank"],"위), ","댓글 ",x[1]["reply"],"개(",x[1]["replyRank"],"위)",end='',sep='')

    print()