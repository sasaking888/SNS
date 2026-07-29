# CHARGE OFFICE LP — Claude 引き継ぎメモ（2026-07-30）

## 渡すファイル（必須）

作業フォルダ: `C:\Users\(株)SMILECREATEGROUP\Desktop\SNS\`

| ファイル | 役割 |
|---|---|
| **`index.html`** | LP本体（約580行） |
| **`styles.css`** | メインCSS（約2800行・パッチ多数） |
| **`GROKRULES.md`** | 編集ルール（毎回必読） |
| **`chargeofficelpspec.md`** | コピー・法令・数字の正本 |
| `images/hero.jpg` | ヒーロー実写 |
| `assets/worry-*.png` | お悩み3アイコン |

任意: `BUILDGUIDE.md` / `_serve-local.ps1`（ローカル確認用）

**`base.css` / `tokens.css` は現状ほぼ未使用。** 本番見た目は `styles.css` のみ。

---

## 絶対ルール（GROKRULES）

1. **`styles.css` 末尾に追記しない**。該当セレクタを探して**その場で書き換える**
2. **`!important` を新規追加しない**
3. **数字・法令文言は1文字も変えない**（下表）
4. 禁止語: マッサージ / 治る・治療 / 必ず・絶対 / 効果の断定
5. 語は **無料トライアル**（「無料体験」禁止）
6. 変更報告は差分のみ。全文再出力しない

### 確定数字

| 項目 | 値 |
|---|---|
| 施術実績 | グループ累計**12万人以上** |
| 施術料 | **11,000円 / 1時間（税込）** |
| 出張費 | **1,100円（税込）** |
| 総額例 | **34,100円（税込）** |
| 1人あたり | **約2,300円**（2,200は誤り） |
| 施術時間 | **約10分**（12分は誤り） |
| 1時間/3時間 | **5名 / 15名** |
| 最低契約 | スタッフ1名派遣につき**3時間から** |
| 満足度 | **94.2%** |
| 継続率 | **98.4%** |
| 出典 | ※2025年1月〜2026年5月の自社アンケートによる |

---

## 現状のページ構成（上から）

1. **header** — ロゴ / TEL / オレンジ `btn--header`「無料トライアル」
2. **hero**（新構造・2026-07-30）
   - テキスト（sub / title / service）
   - 実績バッジ 94.2% / 98.4% + 出典
   - CTA（かんたん入力・ご相談無料）
   - 写真 `images/hero.jpg`（全幅帯）
   - 3タイル `hero__badges-post`（省スペース / 高回転 / 高品質）
3. **worries** — お悩み3カード（左アイコン・右文言）
4. **solution** — 「その課題、CHARGE OFFICEが解決します。」黄→白グラデ + 上V字
5. **about** — CHARGE OFFICEとは（リードのみ・数字なし。画像は見出し下）
6. **reasons** — 選ばれる3つの理由
7. **benefits** — 導入メリット
8. **pricing** — 料金（メインカード / 3項目 / 出張費備品 / 総額例 / 2CTA）
9. **gallery / flow / industries / faq / support / contact**
10. **sticky-cta** — スマホ下部2カード（トライアル橙 / LINE緑）。720px以上は非表示

---

## ヒーロー（最新）

```
.hero > .hero__inner
  .hero__text
  .hero__stats（.stat-badge ×2 + .hero__stats-note）
  .hero__cta
  .hero__photo-block > .hero__photo
  .hero__badges-post（3タイル）
```

- 旧: `hero__stage` / `veil` / `copy` / `person` / `lead` / `trust` → **削除済み**
- 実績バッジは**角丸四角**（円形にしない）
- 3タイル文言は変更禁止

---

## CSSの注意（重要）

`styles.css` は**ベース + パッチ30個以上 + `!important` 大量**の状態。

- 同じセレクタが複数回ある → **ファイル内の最後の指定が効く**
- ヒーロー旧レイアウト用パッチ（absolute写真・140% CTA・padding-right 44% 等）が残っている
  - 新構造向けに一部中和済みだが、**残骸はまだ多い**
  - 触るときは `.hero__copy` / `.hero__stage` / `.hero__badges`（旧）と  
    `.hero__inner` / `.hero__badges-post` / `.stat-badge`（新）を混同しないこと
- 新しい見た目を足すときは **末尾追記ではなく、関連ブロック直下 or 最後の同セレクタを編集**

### 主要な新クラス

| クラス | 用途 |
|---|---|
| `.hero__inner` / `.hero__text` / `.hero__stats` / `.stat-badge` | 新ヒーロー |
| `.hero__photo-block` / `.hero__photo` | 写真帯（static・全幅） |
| `.hero__badges-post` | 写真下の3タイル |
| `.solution` / `.solution__title` | 橋渡しセクション |
| `.price-main` / `.price-feats` / `.price-feat` | 料金メイン |
| `.price-extras` / `.price-extra` | 出張費・備品 |
| `.price-example` | 総額例 |
| `.scta` / `.scta--trial` / `.scta--line` / `.scta--docs` | 2カードCTA |
| `.btn--header` | ヘッダー橙ボタン |
| `.reveal` / `.is-inview` | スクロールふわっと表示 |

---

## 未着手・TODO

- [ ] LINE公式URL（`href=""` のまま・HTMLコメント TODO あり）
- [ ] フォーム action 未設定
- [ ] about / gallery の画像プレースホルダー差し替え
- [ ] お客様の声（`#voices-slot` 空）
- [ ] `styles.css` のパッチ整理（任意・大きい作業）
- [ ] ヒーロー新構造の実機確認（320 / 375 / 1200）をオーナーと突合

---

## ローカル確認

```powershell
# プロジェクト直下で
.\ _serve-local.ps1
# または任意の静的サーバで index.html を開く
```

ハードリロード: **Ctrl+F5**

---

## Claude への依頼の書き方（コピペ用）

```
CHARGE OFFICE の法人LPを修正してください。

必ず読むファイル:
- GROKRULES.md
- index.html
- styles.css
- chargeofficelpspec.md（数字・法令）

ルール:
- styles.css は末尾追記禁止。該当セレクタを探して書き換え
- !important 新規禁止
- 数字・法令文言は変更禁止
- 変更箇所だけ報告

やってほしいこと:
（ここに具体的な依頼）
```
