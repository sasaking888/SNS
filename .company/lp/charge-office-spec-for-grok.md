# CHARGE OFFICE LP 改修設計書(Grok向け)

> 対象ファイル: `index.html`(1ファイル完結。CSS/JSはインライン)
> この設計書は「何を・どこに・どう作るか」を指示するものです。**指示にない箇所は触らないでください。**

---

## 0. 前提

### サービス概要
- サービス名: CHARGE OFFICE(チャージオフィス)
- 内容: 整体師がオフィスに出張する、法人向け出張整体サブスクリプション
- ターゲット: 従業員30名以上の企業の人事・総務担当者、経営層
- ゴール: 資料請求・LINE相談の獲得

### 参考にしたLP
デジタルハリウッド `https://school.dhw.co.jp/p/graphic-design-ui/`
このLPの **①ヒーロー ②CTA前の導線 ③お悩みセクション** の作りを取り入れています。

---

## 1. 絶対に守るルール(壊さないこと)

### 1-1. 表示保証の仕組み(最重要)
このLPは**スクロールが発生しないプレビュー環境でも必ず表示される**よう設計されています。
以下の仕組みを**絶対に削除・変更しないでください。**

```
・CSSのデフォルトは「表示された状態」
・JSが .anim-ready / .will-animate を付けた時だけアニメーションが有効になる
・IntersectionObserver に加えて setTimeout のフォールバックが必ず入っている
```

該当箇所:
| 仕組み | クラス | フォールバック |
|---|---|---|
| 登場アニメ | `.in-fadeup` `.in-fadein` `.in-jack` | 1600ms |
| 旧リビール | `.reveal` → `.will-animate` → `.is-visible` | 1200ms |
| 導入ステップ | `.flow-steps` → `.in-view` | 1200ms |
| LINE追従CTA | `#lineWidget` → `.visible` | 2000ms |

**「最初は非表示にしておいてスクロールで表示する」という書き方は禁止です。**
必ず「デフォルト表示 → JSが動く環境でだけアニメを乗せる」の順序にしてください。

### 1-2. 画像パス
`images/` 配下のファイル名・パスは変更しないでください。

| ファイル | 用途 |
|---|---|
| `hero-visual.png` | ヒーローの写真(1402×715) |
| `worry-center.png` | お悩み中央イラスト(460×470) |
| `worry-illust1〜5.png` | お悩み各イラスト |
| `step4-treatment.png` | 導入ステップ4の施術写真 |
| `problem-banner.png` | ※現在未使用(切り出し元。削除しないこと) |
| `hero-banner.png` | ※現在未使用(切り出し元。削除しないこと) |

### 1-3. ブランドカラー(`:root` で定義済み。これ以外の色を足さない)
```css
--yellow: #FFC400;      /* メイン */
--yellow-deep: #F5A300;
--orange: #E8531F;      /* サブ・CTA */
--orange-deep: #B8390F;
--line-green: #06C755;  /* LINEボタン専用。他に使わない */
--ink: #201B14;         /* 文字 */
--ink-soft: #5B564C;    /* 本文 */
--cream: #FFF6E3;
--surface: #FBF8F2;
```

---

## 2. 現在のセクション構成と実装方式

| # | セクション | 実装方式 | 状態 |
|---|---|---|---|
| ① | ヘッダー(固定) | HTML | 完了 |
| ② | ヒーロー | **HTML文字 + 写真画像** | 完了 |
| ③ | CTA前3ポイント + メインCTA | HTML | 完了 |
| ④ | 実績カード(12万人/10分〜/0.5畳) | HTML | 完了 |
| ⑤ | お悩み(Problem) | **HTML + 切り出しイラスト6枚** | **要調整(§3)** |
| ⑥ | 未病リスク(Agitation) | HTML | 要改善(§4) |
| ⑦ | サービス紹介・3つの特徴 | HTML | 要改善(§4) |
| ⑧ | 導入4ステップ | HTML + 写真1枚 | 要改善(§4) |
| ⑨ | お客様の声 | HTML アコーディオン | 完了 |
| ⑩ | 料金プラン | HTML | 完了 |
| ⑪ | FAQ | HTML アコーディオン | 完了 |
| ⑫ | クロージング + フォーム | HTML | 完了 |
| + | LINE追従CTA | HTML | 完了 |

---

## 3. 【最優先】お悩みセクションのPC表示を仕上げる

### 現状
モバイルは完成。**PC(768px以上)のレイアウト指定が未実装**で、1カラムのまま縦に長い。

### やること
`@media (min-width: 768px)` 内に、以下のグリッド配置を追加してください。

```
┌─────────┬─────────┬─────────┐
│  item1  │  item2  │  item3  │
├─────────┼─────────┼─────────┤
│  item4  │ center  │  item5  │
└─────────┴─────────┴─────────┘
```

必要な指定:
- `.worry-stage` を `grid-template-columns: repeat(3, 1fr)` の3列に
- `grid-template-areas` で上図の配置を作る
- `.worry-item.item1`〜`item5` と `.worry-center-wrap` に `grid-area` を割り当て
- `.worry-center-wrap` はモバイルで `order: -1`(先頭)になっているので、PCでは `order: 0` に戻す
- `.worry-stage` の `max-width` を 1000px 程度に広げる
- `.worry-head h2` のフォントサイズを 34px 程度に

既存のHTML構造(変更不要):
```html
<div class="worry-stage">
  <div class="worry-center-wrap in-fadein">
    <img src="images/worry-center.png" ...>
  </div>
  <div class="worry-item item1 in-fadeup">
    <div class="worry-item-head">
      <span class="worry-num">1</span>
      <p class="worry-title"><u>離職・採用コスト</u>が増えている</p>
    </div>
    <img src="images/worry-illust1.png" ...>
  </div>
  <!-- item2〜item5 も同じ構造。delay01 / delay02 が付いている -->
</div>
```

---

## 4. 【次点】残り3セクションの改善

以下の3つは「文字ばかりで寂しい」状態です。**§5のデザインパターンに沿って**作り直してください。

### 4-1. 未病リスク(Agitation) `.risk-flow`
現状: アイコン3つ + 短文が縦に並ぶだけ。
やること: §5-Aの「見出しの型」を適用し、各ステップに余白と階調をつけて重みを出す。

### 4-2. 3つの特徴 `.feature-cards`
現状: アウトラインアイコン + 上罫線のみでシンプルすぎる。
やること: §5-Aの見出し型 + カードに背景色/影で「面」を作る。

### 4-3. 導入4ステップ `.flow-steps`
**このセクションは何度も作り直して失敗しています。** 現状は白ベース + セリフ体の数字。
やること: §5-Cのパターンで作り直す。**アーチ型(border-radius で上部を丸くする)は絶対に使わないこと。**

---

## 5. 適用すべきデザインパターン(デジハリLP由来)

### 5-A. 見出しの型
```
[英語ラベル] ← 小さく、オレンジ、letter-spacing広め、左に短い横線
[日本語見出し] ← 大きく太く、キーワードだけ色を変える
```
実装済みの `.eyebrow` + `.section-title` がこの型です。**新規セクションもこれに揃えてください。**

### 5-B. 文字の強調は「太字」ではなく「色」
デジハリは `<span class="c-red">未経験</span>` のように**色で強調**しています。
CHARGE OFFICEでは:
- キーワードを `var(--orange)` にする
- または `border-bottom: 3〜5px solid var(--yellow)` で下線マーカー

ヒーローの `"ゼロ"` が実装例です(`.hero-catch em`)。

### 5-C. ステップ/リストの型
```
1つの項目 = [番号バッジ] + [見出し] + [イラストor写真] + [短い説明文]
```
- 番号は**黄色の丸バッジ**(`.worry-num` が実装例)
- 各項目は白背景 + `border-radius: 18px` + 淡い影で「カード」として独立させる
- 項目間は `gap: 16〜20px`

### 5-D. 時間差で登場させる
複数並ぶ要素には、順番に `delay01` `delay02` を付けてください。
```html
<div class="in-fadeup">1つ目</div>
<div class="in-fadeup delay01">2つ目</div>
<div class="in-fadeup delay02">3つ目</div>
```
利用可能クラス: `in-fadeup`(下から) / `in-fadein`(フェードのみ) / `in-jack`(ポップ)
遅延: `delay01`(0.12s) 〜 `delay04`(0.48s)

### 5-E. CTAの型(変更しないこと)
```html
<div class="cta-block in-fadeup">
  <a href="#contact" class="cta-primary">
    <span class="cta-badge">カンタン<b>30秒</b>入力・無料</span>  ← 黒バッジ(上に飛び出す)
    <span class="cta-sub">来社不要・オンライン相談OK</span>        ← 小さい補足
    <span class="cta-main">資料請求はこちら<span class="cta-arrow">▶▶</span></span>
  </a>
  <a href="#" class="btn btn--line btn--small">LINEで気軽に相談</a>  ← サブ(緑)
</div>
```
**CTAの直前には必ず「3ポイント」(`.point-list`)を置く**のがこのLPの型です。
「安心材料を3つ見せる → だから今すぐ」という導線をセットで扱ってください。

---

## 6. やってはいけないこと(過去に失敗した例)

| NG | 理由 |
|---|---|
| 全要素をアーチ型(上部が丸い形)にする | 統一感が崩れて不評だった |
| 黄土色・くすんだオレンジのベタ塗り背景 | 安っぽく見える |
| 白背景に文字だけ置く | 余白だけで中身がなく貧相に見える |
| ブランドカラー外の色(緑・青など)を足す | LINEボタン以外での使用は禁止 |
| スクロール前提でデフォルト非表示にする | §1-1のとおり表示されなくなる |

---

## 7. 未設定項目(公開前に必要。今回の作業対象外)

- [ ] フォームの送信先(`<form action="#">` がダミー)
- [ ] LINE公式アカウントURL(`href="#"` がダミー)
- [ ] お客様の声を実データに差し替え(現在ダミー3件)
- [ ] 導入ステップ2〜3、未病リスクの写真素材
- [ ] チェア価格・導入ステップ詳細のクライアント確認

---

## 8. 納品形式

`index.html` 全体を修正後の完全なコードで返してください。
`images/` のパスは変えないこと。
