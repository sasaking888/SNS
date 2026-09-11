# POWWOW LP 引き継ぎ（セクション1）

女性専門整体サロン POWWOW の LP。セクション分割制作の **セクション1（FV＋3問アンケート）** まで実装済み。

## 確認方法

`index.html` をブラウザで開く。

```
index.html
```

キャッシュが残る場合は Ctrl+F5。

## ファイル

| パス | 内容 |
|---|---|
| `tokens.css` | 共通デザイントークン。セクション側で再定義しない |
| `pw-sec-fv-survey.html` | セクション1本体（HTML/CSS/JS 1ファイル） |
| `index.html` | プレビュー用（中身はセクション1と同じ） |
| `assets/fv/hero.{avif,webp,jpg}` | FVポスター。AVIF → WebP → JPEG |

## できていること

- FV は支給ポスターを **トリミングせず全体表示**
- 3問アンケート（単一選択、上から順、`window.pwSurvey` + `pw:survey-change`）
- 設問UIはピンク帯＋白丸Q番号＋黒枠ピル型ボタン
- 導入「初回限定 特別価格でご案内！」と完了「ご回答ありがとうございます！」は同じピンク帯デザイン
- 薬機法注記あり

## まだないこと

- セクション2以降（コース詳細・予約など）
- セクション結合後の本番 `index.html`
- 実素材の最終差し替え（今の hero は支給ポスター）

## 結合時の注意

- ルートは `<section class="pw-sec pw-sec--fv-survey">`
- CSS変数は `tokens.css` のみ
- FVセクションだけ `padding-top: 0`
- 回答状態は `window.pwSurvey = { q1, q2, q3 }`

## 技術

HTML / CSS / 素の JavaScript。ライブラリなし。
