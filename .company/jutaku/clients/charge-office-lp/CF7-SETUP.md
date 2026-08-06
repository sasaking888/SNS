# Contact Form 7 への組み込み手順

CHARGE OFFICE LP のお問い合わせフォームを、charge10.tokyo の既存 WordPress + Contact Form 7 に載せるための手順書。

**前提（2026-08-06 確認済み）**

| 項目 | 内容 |
|---|---|
| サイト | WordPress |
| フォームプラグイン | Contact Form 7（ソースに `wpcf7` を確認） |
| 送信先 | contact@charge10.tokyo |

---

## 手順

### 1. WordPress管理画面で新しいフォームを作る

`お問い合わせ` → `新規追加` → タイトルを「CHARGE OFFICE LP」にする。

### 2.「フォーム」タブに下記をそのまま貼る

CF7 は `<form>` タグを自動で付けるので、**`<form>` は含めない**。

```html
<div class="form-grid">
  <div class="form-field">
    <label for="name">氏名<span class="req">必須</span></label>
    [text* your-name id:name autocomplete:name]
  </div>
  <div class="form-field">
    <label for="company">会社名<span class="req">必須</span></label>
    [text* company id:company autocomplete:organization]
  </div>
  <div class="form-field">
    <label for="address">住所<span class="req">必須</span></label>
    [text* address id:address autocomplete:street-address]
  </div>
  <div class="form-field">
    <label for="email">メールアドレス<span class="req">必須</span></label>
    [email* email id:email autocomplete:email]
  </div>
  <div class="form-field">
    <label for="tel">電話番号<span class="req">必須</span></label>
    [tel* tel id:tel autocomplete:tel]
  </div>
  <div class="form-field">
    <label for="size">従業員数<span class="req">必須</span></label>
    [select* size id:size include_blank "〜29名" "30〜99名" "100〜299名" "300名〜"]
  </div>

  <fieldset class="form-field form-field--radio">
    <legend>希望申込内容<span class="req">必須</span></legend>
    [radio intent use_label_element "無料トライアルのお申し込み" "資料請求" "サービスについての質問" "その他"]
  </fieldset>

  <fieldset class="form-field form-field--radio">
    <legend>サービスを知ったきっかけ<span class="req">必須</span></legend>
    [radio referral use_label_element "テレビ・新聞・雑誌・ラジオ" "インターネット検索" "インターネット広告" "SNS" "Webサイト、ブログ" "チラシ" "知人からの紹介" "その他"]
  </fieldset>

  <div class="form-field">
    <label for="message">質問・ご要望</label>
    [textarea message id:message placeholder "無料トライアル希望、資料請求など"]
  </div>

  <p class="cta-note cta-note--left">ご入力いただいた個人情報は、お問い合わせへの回答および無料トライアル・資料のご案内にのみ利用します。第三者に提供することはありません。</p>

  <label class="form-confirm">
    [acceptance confirm] 入力内容をご確認の上、チェックをお願いします。
  </label>

  <div class="form-actions">
    [submit class:btn class:btn--primary class:btn--block "入力内容を送信する"]
  </div>
</div>
```

### 3.「メール」タブを設定する

| 欄 | 値 |
|---|---|
| 送信先 | `contact@charge10.tokyo` |
| 送信元 | `[_site_admin_email]`（**変更しない**。独自ドメイン以外を入れると迷惑メール判定される） |
| 題名 | `【CHARGE OFFICE LP】[intent] - [company]` |
| 追加ヘッダー | `Reply-To: [email]` |

メッセージ本文：

```
CHARGE OFFICE LP のお問い合わせフォームから送信がありました。

■ 希望申込内容
[intent]

■ 氏名
[your-name]

■ 会社名
[company]

■ 住所
[address]

■ メールアドレス
[email]

■ 電話番号
[tel]

■ 従業員数
[size]

■ サービスを知ったきっかけ
[referral]

■ 質問・ご要望
[message]

--
送信元: [_url]
送信日時: [_date] [_time]
送信者IP: [_remote_ip]
```

### 4. 生成されたショートコードをLPに貼る

保存すると `[contact-form-7 id="123" title="CHARGE OFFICE LP"]` のようなショートコードが出る。
これを `index.html` のフォーム部分（`<form class="form-grid">` 〜 `</form>`）と差し替える。

---

## 注意点（実装時に必ず確認する）

### ラジオボタンの必須指定

**Contact Form 7 のラジオボタンには `[radio*]`（必須）が無い。**
`[radio]` は初期状態でどれも選択されていない状態にできるが、そのまま送信できてしまう。

対処は次のどちらか。実物を見てから決める。

- **A案**: `[select*]` に変える（必須にできるが、見た目がプルダウンに変わる）
- **B案**: ラジオのままにして、未選択でも送信を許容する（「その他」に寄せる運用）

現状のLPはHTMLの `required` で必須にしているので、**CF7に移すと必須が外れる**。ここは仕様が変わる点なのでクライアントに伝えること。

### CSSの適用

`styles.css` の `.form-field` `.radio-option` などがそのまま効くかは、**WordPressテーマのCSSとぶつかる可能性がある**ため実物で要確認。

特に CF7 は `[radio]` を独自のマークアップ（`<span class="wpcf7-list-item">`）で出力するため、
現在の `.radio-option`（`<label>` 直接指定）のCSSは当たらない。下記の読み替えが必要になる見込み。

```css
/* .radio-option → CF7の出力に合わせる */
.form-field--radio .wpcf7-list-item {
  display: block;
  margin: 0 0 8px;
}
```

### フィールド名を `name` から `your-name` に変えている理由

CF7 の一部バージョンで `name` が予約語と衝突する報告があるため、氏名のみ `your-name` にした。
他のフィールド名（`company` `address` `email` `tel` `size` `intent` `referral` `message` `confirm`）は現行LPのまま。

---

## スコープについて

**このLPをWordPressの固定ページとして設置する作業は、当初の作業範囲に含まれていない。**

合意済みのスコープは「デザインモック／LP設計書／実装／公開前レビュー／表示崩れの検証」まで。
サーバーへの設置・WordPressへの移植・CF7の設定は別作業のため、**着手前に追加見積もりを提示すること**（受託部門ルール）。

この手順書があれば先方の制作会社側でも作業できるので、「手順書を渡して先方にやってもらう」も選択肢。
