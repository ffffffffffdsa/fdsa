import asyncio
import time
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta

import dc_api
import pickle

async def run():
    data = {}
    rank = {}

    done = False

    concount = 0
    count = 0
    now = datetime.now()

    data['date'] = now

    async with dc_api.API() as api:
        async for index in api.board(board_id="iveon",is_minor=True,start_page=983):
            #print(index)
            count += 1

            doc = await index.document()


            try:
                if count % 10 == 0:
                    print(doc.time)
                    data['rank'] = rank
                    with open('data.pickle', 'wb') as fw:
                        pickle.dump(data, fw)

                if doc.time < datetime(2023,7,1,0,0):
                    concount += 1
                    if concount > 5:
                        break
                    continue
                else:
                    concount = 0

                if doc.author_id == None:
                    writer = doc.author
                else:
                    writer = doc.author+"("+doc.author_id+")"

                if writer in rank:
                    rank[writer]['article'] += 1
                else:
                    rank[writer] = {"article":1,"reply":0}
                #print(writer+ "/"+str(doc.time))
            except Exception as e:
                print(e)
            try:
                async for comm in index.comments():
                        if (comm.author_id == None):
                            writer = comm.author
                        else: writer = comm.author + "(" + comm.author_id + ")"

                        if writer in rank:
                            rank[writer]['reply'] += 1
                        else:
                            rank[writer] = {"article":0,"reply":1}
            except Exception as e:
                print(e)


            time.sleep(0.2)


    data['rank'] = rank
    with open('data.pickle','wb') as fw:
        pickle.dump(data, fw)
    print(data)
    a = input()

asyncio.run(run())