import sys
import matplotlib.pyplot as plt
import uuid
import json
import base64
import os
import cv2

def cv2MosaicOnTheFace(image_path):

  #ファイル読み込み
  image = cv2.imread(image_path)

  #グレースケール変換
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  #カスケード識別器のファイルパス　絶対パスで指定に変更してください！！！！
  cascade_path = "haarcascade_frontalface_default.xml"

  #カスケード分類器の特徴量を取得する
  cascade = cv2.CascadeClassifier(cascade_path)
  
  #物体認識（顔認識）の実行
  #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
  #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
  #scaleFactor – 各画像スケールにおける縮小量を表します
   ##設定範囲	1.0を超える ( > 1.0 )
   ##scaleFactorは縮小量の「ステップ」。したがってscaleFactorが大きくなるほど飛び飛びの計算になる。結果として全体としての計算が速くなる（計算時間が短くなる）。
   ##ステップを細かく刻むこと（限りなく1.0に近い値）が良い訳ではないが、かといってステップが大きいと検出『見逃し』が発生する。
  #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
   ##0のとき	検出にマッチする数が多くなる。見逃しは少ないが誤検出が増える
   ##大きいとき	検出にマッチする数は少なくなる。見逃しは多いが誤検出は少ない
  #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
  #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
  facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.11, minNeighbors=1, minSize=(1, 1))

  #print(facerect)
  color = (100, 0, 0) #白

  # 検出した場合
  if len(facerect) > 0:

      #検出した顔を囲む矩形の作成
      for rect in facerect:
          cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=-1)

      #認識結果の保存
      cv2.imwrite(image_path, image)

try:
  jsonData = json.loads(sys.stdin.readline())
  query = jsonData['query']
  post = jsonData['post']
  path = jsonData['path']
  
  # file = open(path + post["clusters"][3]["value"], 'rb').read()
  # enc_file1 = base64.b64encode( file ).decode('utf-8')
  # file.close()

  # file = open(path + post["clusters"][4]["value"], 'rb').read()
  # enc_file2 = base64.b64encode( file ).decode('utf-8')
  # file.close()
  image_path1 = path + "/" + post["clusters"][3]["value"]
  #画像黒塗り
  cv2MosaicOnTheFace(image_path1)
  file = open(image_path1, 'rb').read()
  enc_file1 = base64.b64encode( file ).decode('utf-8')

  image_path2 = path + "/" + post["clusters"][4]["value"]
  #画像黒塗り
  cv2MosaicOnTheFace(image_path2)
  file = open(image_path2, 'rb').read()
  enc_file2 = base64.b64encode( file ).decode('utf-8')

  image_path3 = path + "/" + post["clusters"][5]["value"]
  #画像黒塗り
  cv2MosaicOnTheFace(image_path3)
  file = open(image_path3, 'rb').read()
  enc_file3 = base64.b64encode( file ).decode('utf-8')
  # file.close()
  # enc_file3 = path + "/" + post["clusters"][5]["value"]

  mappings = {"error": "", "mappings": [
    { "item": "chart1","sheet": 1,"cluster":  7,"type": "string","value":query["param1"]},
    { "item": "chart1","sheet": 1,"cluster":  8,"type": "string","value":query["param2"]},
    { "item": "chart1","sheet": 1,"cluster":  9,"type": "string","value":post["clusters"][0]["value"]},
    { "item": "chart1","sheet": 1,"cluster": 10,"type": "string","value":post["clusters"][1]["value"]},
    { "item": "chart1","sheet": 1,"cluster": 11,"type": "string","value":post["clusters"][2]["value"]},
    { "item": "chart1","sheet": 1,"cluster": 12,"type": "string","value":enc_file1},
    { "item": "chart1","sheet": 1,"cluster": 13,"type": "string","value":enc_file2},
    { "item": "chart1","sheet": 1,"cluster": 14,"type": "string","value":enc_file3}
    ]}
  print(json.dumps(mappings))

except Exception as e:
  #標準出力JSONで返す（エラー）
  mappings = {"error": "Pythonでエラー：" + str(e)}
  print(json.dumps(mappings))

