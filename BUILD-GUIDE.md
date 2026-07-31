# CHARGE OFFICE LP — 実装指示書（マークアップ担当向け）

このファイルと `tokens.css` / `base.css` / `charge-office-lp-spec.md` の4点で作業する。

---

## 0. 大原則 — 最初に読む

1. **CSSは完成している。1行も書かない。1行も変えない。** `tokens.css` と `base.css` をそのまま読み込むだけ
2. **クラス名はこの指示書にあるものだけを使う。** 新しいクラスを作らない
3. **`style=""` を書かない。** インラインCSSは禁止
4. **レイアウトを自分で判断しない。** カラム数・余白・折り返しは全部CSS側で決まっている
5. **文言・数字は `charge-office-lp-spec.md` が正。** 勝手に書き換えない、勝手に足さない、勝手に計算しない
6. **JSライブラリを入れない。** FAQは素の `<details>`、スクロールは CSS の `scroll-behavior` で足りている

**やりがちな失敗（実際に起きた）**: ヒーローを勝手に2カラムで組む。
→ ヒーローの2カラム化は **CSSが900px以上で自動的にやる**。HTML側は下の骨格どおりに並べるだけでよい。

---

## 1. ファイルの骨格

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>企業出張整体 CHARGE OFFICE｜オフィスに出張、ひとり10分の福利厚生</title>
  <meta name="description" content="【設計書§1より120字以内】">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Zen+Kaku+Gothic+New:wght@700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="base.css">
</head>
<body>
  <!-- ここに §3 のセクションを順番どおり並べる -->
</body>
</html>
```

---

## 2. セクションの順番と背景色（この通りに並べる）

背景色は**各セクションに明示指定**する。`nth-child` で自動反転させない。

| # | セクション | 外側のクラス |
|---|---|---|
| 1 | ヘッダー | `site-header`（`band` は付けない） |
| 2 | ファーストビュー | `hero`（`band` は付けない） |
| 3 | 3つのバッジ | `band band--alt` |
| 4 | 企業のお悩み | `band band--white` |
| 5 | CHARGE OFFICEとは | `band band--alt` |
| 6 | 選ばれる3つの理由 | `band band--white` |
| 7 | 導入メリット（6つ） | `band band--alt` |
| 8 | 料金 | `band band--white` |
| 9 | 施術イメージ | `band band--alt` |
| 10 | ご利用の流れ | `band band--white` |
| 11 | 導入企業 | `band band--alt` |
| — | **お客様の声** | **v1では作らない。HTMLコメントで位置だけ残す** |
| 12 | よくあるご質問 | `band band--white` |
| 13 | 安心のサポート体制 | `band band--navy` |
| 14 | 最終CTA＋フォーム | `band band--alt` |
| 15 | フッター | `site-footer` |
| 16 | 追従CTA（スマホ） | `sticky-cta` |

> **あとで声セクションを足すとき**: `band band--white` で 11 と 12 の間に入れ、**12（FAQ）を `band--alt` に変える**。これだけで交互が保たれる。

---

## 3. 共通パターン（使い回す型）

### パターンA — 見出し＋3カラムカード

**使う場所**: 4 お悩み / 6 選ばれる理由 / 7 導入メリット（※6枚なので同じ型で6つ並べる）/ 10 ご利用の流れ

```html
<section class="band band--white">
  <div class="inner">
    <div class="sec-head">
      <h2>【見出し】</h2>
      <p class="lead">【リード。不要なら削る】</p>
    </div>
    <div class="grid grid--3">
      <div class="card">
        <h3>【小見出し】</h3>
        <p class="mute">【本文】</p>
      </div>
      <!-- カードを必要数くり返す -->
    </div>
  </div>
</section>
```

- **`grid--3` を書けば3カラム、`grid--2` なら2カラム。720px未満では自動で1カラムに落ちる。** SP用の記述は不要
- **カードの中にカードを入れない**

### パターンB — 番号つきカード

**使う場所**: 6 選ばれる3つの理由 / 10 ご利用の流れ

パターンAの `.card` の中で、`<h3>` の**前**に番号を置く。

```html
<div class="card">
  <div class="num">01</div>
  <h3>【小見出し】</h3>
  <p class="mute">【本文】</p>
</div>
```

### パターンC — CTAブロック

**使う場所**: 3 バッジの下 / 8 料金の下 / 14 最終CTA

```html
<div class="cta-row">
  <a class="cta" href="#contact">【主CTAの文言】</a>
  <a class="cta cta--sub" href="#contact">【副CTAの文言】</a>
</div>
<p class="cta-note mute">【安心材料の一文】</p>
```

**どこに何を置くかは設計書§5の「CTAの二段構え」の表に従う。**

---

## 4. 個別の骨格（迷いやすい箇所だけ厳密に指定）

### 1. ヘッダー

```html
<header class="site-header">
  <a class="site-header__brand" href="#">CHARGE OFFICE</a>
  <div class="site-header__right">
    <a class="site-header__tel hide-sp" href="tel:05031843852">050-3184-3852</a>
    <a class="cta hide-sp" href="#contact">無料トライアル</a>
  </div>
</header>
```

- `hide-sp` は**900px以上でのみ表示**される。スマホでは追従CTA（§4-16）が代わりに出るので、ヘッダーにボタンを出さない
- ハンバーガーメニューは**作らない**（1ページなので遷移先がない）

### 2. ファーストビュー ← **ここを間違えた。骨格どおりに組むこと**

```html
<section class="hero">
  <div class="inner">
    <div>
      <p class="hero__sub">オフィスに、健康という投資を。</p>
      <h1>社員が元気だと、<br>会社は強くなる。</h1>
      <p class="hero__service">企業出張整体 CHARGE OFFICE</p>
      <p class="lead">【設計書§3の補足文】</p>
      <div class="cta-row" style="justify-content:flex-start">
        【パターンCのCTA。styleは使わず、cta-rowをそのまま使ってよい】
      </div>
      <ul class="hero__trust">
        <li>初期費用0円で試せる</li>
        <li>グループ累計12万人以上の施術実績</li>
      </ul>
    </div>
    <div>
      <img src="images/hero.jpg" alt="オフィスで施術を受ける社員" width="800" height="600">
    </div>
  </div>
</section>
```

- **`.inner` の直下に `<div>` を2つ置くだけ。** 左＝テキスト、右＝画像
- **カラム指定を書かない。** 900px以上で自動的に2カラム、それ未満で自動的に縦積みになる
- `grid` `flex` `width` `float` を**自分で書かない**

### 3. バッジ帯

```html
<section class="band band--alt">
  <div class="inner">
    <div class="badges">
      <div>
        <div class="badge__label">省スペース</div>
        <p class="badge__body">たった0.5畳分のスペースでOK</p>
      </div>
      <!-- 高回転 / 高品質 も同じ形で -->
    </div>
    【パターンCのCTA】
  </div>
</section>
```

### 8. 料金 ← 中身は設計書§5が正。骨格だけ示す

```html
<section class="band band--white" id="pricing">
  <div class="inner">
    <div class="sec-head"><h2>料金</h2></div>
    <div class="price-box">

      <div class="price-main">
        <span class="price-tag">1時間</span>
        <div class="price-num">11,000<small>円（税込）</small></div>
      </div>

      <dl class="price-list">
        <div><dt>最低契約</dt><dd>スタッフ1名につき3時間〜</dd></div>
        <div><dt>施術可能人数</dt><dd>3時間で15名</dd></div>
        <div><dt>スタッフ出張費</dt><dd>1,100円（税込）</dd></div>
      </dl>

      <div class="price-total">
        <table>
          <tr><td>施術料 11,000円 × 3時間</td><td>33,000円</td></tr>
          <tr><td>スタッフ出張費</td><td>1,100円</td></tr>
          <tr><td>合計（3時間・15名の場合）</td><td>34,100円</td></tr>
        </table>
      </div>

      <div class="price-metaphor">
        <p><strong>1人あたり約2,300円</strong></p>
        <p class="mute">ランチ会1回分のコストで、社員の身体をメンテナンス。</p>
      </div>

      <div class="price-free">
        <p><strong>まずは無料トライアルから</strong></p>
        <p class="mute">【設計書§5bの一文】</p>
      </div>

      <ul class="price-notes">
        <li>【チェアの注記。設計書§5の確定文言をそのまま】</li>
        <li>【増員対応の一文。設計書§5より】</li>
      </ul>

      【パターンCのCTA。ここは主CTAが「資料請求」】
    </div>
  </div>
</section>
```

- `.price-list` は `<dl>` の中に `<div>` を並べる形。**`<table>` にしない**（スマホで崩れる）
- 総額表だけは `<table>` でよい（2列の計算表なので崩れない）

### 9. 施術イメージ

```html
<section class="band band--alt">
  <div class="inner">
    <div class="sec-head"><h2>施術イメージ</h2></div>
    <div class="photos">
      <img src="images/scene-1.jpg" alt="【説明】" width="800" height="600">
      <!-- 4枚 -->
    </div>
    <p class="center mute">服を着たままでOK。デスクワークの合間に、手軽にリフレッシュ。</p>
  </div>
</section>
```

### 11. 導入企業

```html
<section class="band band--alt">
  <div class="inner">
    <div class="sec-head"><h2>こんな企業にご導入いただいています</h2></div>
    <ul class="industries">
      <li>IT・Web企業</li>
      <li>コンサルティング会社</li>
      <li>広告・制作会社</li>
      <li>金融・保険会社</li>
      <li>不動産・建設会社</li>
      <li>士業・法律事務所</li>
    </ul>
  </div>
</section>

<!-- ▼ お客様の声セクションはここに入る（v1では作らない）
     追加時は band band--white で入れ、次のFAQを band--alt に変える -->
```

### 12. よくあるご質問

```html
<section class="band band--white">
  <div class="inner inner--narrow">
    <div class="sec-head"><h2>よくあるご質問</h2></div>
    <details><summary>【質問】</summary><p>【回答】</p></details>
    <!-- 7問。設計書のFAQ5問＋料金・資格の2問 -->
  </div>
</section>
```

- `<details>` の開閉は**CSSでやっている。JSを書かない**

### 14. 最終CTA＋フォーム

```html
<section class="band band--alt" id="contact">
  <div class="inner">
    <div class="sec-head">
      <h2>【設計書§4-15の見出し】</h2>
      <p class="lead">【安心材料】</p>
    </div>

    <form class="form" method="post" action="【送信先。未定なら action="#" とコメントを残す】">
      <label>会社名<span class="req">必須</span>
        <input type="text" name="company" required></label>
      <label>ご担当者名<span class="req">必須</span>
        <input type="text" name="name" required></label>
      <label>メールアドレス<span class="req">必須</span>
        <input type="email" name="email" required></label>
      <label>電話番号
        <input type="tel" name="tel"></label>
      <label>従業員数
        <select name="employees">
          <option value="">選択してください</option>
          <option>〜30名</option><option>31〜100名</option>
          <option>101〜300名</option><option>301名〜</option>
        </select></label>
      <label>ご相談内容
        <textarea name="message"></textarea></label>
      <label class="privacy">
        <input type="checkbox" name="agree" required>
        <a href="/privacy">プライバシーポリシー</a>に同意します</label>
      <div class="cta-row"><button class="cta" type="submit">無料トライアルを申し込む</button></div>
    </form>

    <p class="center mute">お電話でも承ります　
      <a class="site-header__tel" href="tel:05031843852">050-3184-3852</a>（平日 9:00-18:00）</p>
  </div>
</section>
```

- **項目を増やさない。** 増やすほど離脱する
- `type="email"` `type="tel"` を必ず使う（スマホのキーボードが変わる）

### 15. フッター

```html
<footer class="site-footer">
  <div class="inner">
    <p>企業出張整体 CHARGE OFFICE</p>
    <p>【運営者名】｜050-3184-3852（平日 9:00-18:00）</p>
    <p>対応エリア: 東京23区中心、一部三県（神奈川・千葉・埼玉）</p>
    <p><a href="/privacy">プライバシーポリシー</a></p>
  </div>
</footer>
```

### 16. 追従CTA（スマホのみ・900px以上では自動で消える）

`</body>` の直前に置く。

```html
<div class="sticky-cta">
  <a class="cta cta--sub" href="tel:05031843852">電話する</a>
  <a class="cta" href="#contact">無料トライアル</a>
</div>
```

---

## 5. 画像について

**素材が届くまでは仮のプレースホルダーでよい。** ただし次を守る。

- `width` と `height` を必ず書く（読み込み時のガタつき防止）
- `alt` に**内容を書く**（「画像」「写真」はNG）
- ファイル名は `images/hero.jpg` `images/scene-1.jpg` … の形で、あとから差し替えるだけで済むようにする

---

## 6. 提出前のセルフチェック

- [ ] CSSファイルを編集していない
- [ ] `style=""` を1つも書いていない
- [ ] この指示書に無いクラス名を作っていない
- [ ] 数字が設計書と一致（**12万人**／11,000円／1,100円／34,100円／約2,300円／3時間・15名）
- [ ] 設計書§6の禁止語が1つも入っていない（マッサージ／治る／必ず／効果の断定）
- [ ] 幅320pxで横スクロールが出ない
- [ ] 900px以上でヒーローが2カラム、それ未満で1カラムになる
- [ ] お客様の声セクションを**作っていない**（コメントのみ）
