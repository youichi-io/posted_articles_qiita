import requests
import json
import math
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


USER_ID = 'youichi_io'
key = config['API_KEY']['key']
PER_PAGE = 20
allViews = 0
allLikes = 0
allStocks = 0


headers = {"content-type": "application/json", 'Authorization': f'Bearer {key}'}

url = 'https://qiita.com/api/v2/users/' + USER_ID
res = requests.get(url, headers=headers)
json_qiita_info = res.json()

#投稿したQiita記事の数
items_count = json_qiita_info['items_count']

# Qiita APIは一回のリクエスト上限があるのでリクエスト数を分けるために定義
page = math.ceil(items_count / PER_PAGE)

print('|記事タイトル|いいね数|ストック数|View数|')

for i in range(page):

    # リクエスト送ってそれぞれの記事の情報が含まれたjsonをぶち込む
    url = 'https://qiita.com/api/v2/authenticated_user/items' + \
        '?page=' + str(i + 1)
    res = requests.get(url, headers=headers)
    json_qiita_info = res.json()

    for j in range(PER_PAGE):
        try:
            # IDをjsonから引っ張り出す
            item_id = json_qiita_info[j]['id']

            # リクエスト送って指定したIDの記事のView数が含まれたjsonをぶち込む
            url = 'https://qiita.com/api/v2/items/' + str(item_id)
            res = requests.get(url, headers=headers)
            json_view = res.json()

            # View数をjsonから引っ張り出す
            page_view = json_view['page_views_count']

            # 加算代入して総View数とする
            allViews += page_view
            
            #  総いいね数を取得
            allLikes += json_qiita_info[j]['likes_count']
            
            #  総ストック数を取得
            allStocks += json_qiita_info[j]['stocks_count']
            
            # タイトル、いいね数、ストック数、View数の順に表示
            print('| ' + json_qiita_info[j]['title'] + ' | ' +
                  str(json_qiita_info[j]['likes_count']) + ' |' +
                  str(json_qiita_info[j]['stocks_count']) + ' |' +
                  str(page_view) + ' |')

        except IndexError:
            #1記事あたりの平均いいね数を取得
            averageLikes = round(allLikes / items_count, 1)
            
            #1記事あたりの平均ストック数を取得
            averageStocks = round(allStocks / items_count, 1)
            
            #平均いいね率を取得(いいね数/総閲覧数 *100)
            engagementRate= round(allLikes / allViews * 100, 2)
            
            print('View総計:' + str(allViews))
            print('平均いいね数:' + str(averageLikes))
            print('平均ストック数:' + str(averageStocks))
            print('平均いいね率:' + str(engagementRate) + '%')
            print('出力完了')
            break

# 何も出力されない場合のみ以下を実行

#1記事あたりの平均いいね数を取得
averageLikes = round(allLikes / items_count, 1)
            
#1記事あたりの平均ストック数を取得
averageStocks = round(allStocks / items_count, 1)
            
#平均いいね率を取得(いいね数/総閲覧数 *100)
engagementRate= round(allLikes / allViews * 100, 2)
            
print('View総計:' + str(allViews))
print('平均いいね数:' + str(averageLikes))
print('平均ストック数:' + str(averageStocks))
print('平均いいね率:' + str(engagementRate) + '%')
print('正常出力完了')