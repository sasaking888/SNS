#!/bin/sh
# sections/*.html を連結し、CSSを埋め込んだ単一の index.html を出力する。
# 使い方: このディレクトリで ./build.sh
# 出力: index.html (1枚で完結。そのままアップロードできる)
set -eu
cd "$(dirname "$0")"

{
  sed '/__CSS__/,$d' sections/00-head.html   # マーカーの手前まで
  cat tokens.css base.css                    # CSSを流し込む
  sed '1,/__CSS__/d' sections/00-head.html   # マーカーの後ろ
  cat sections/[1-9]*.html                   # 本体セクション(ファイル名順)
} > index.html

echo "index.html を生成しました ($(wc -l < index.html) 行)"
