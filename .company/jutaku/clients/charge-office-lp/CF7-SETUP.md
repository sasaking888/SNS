# Contact Form 7 への組み込み手順

CHARGE OFFICE LP のお問い合わせフォームを、charge10.tokyo の WordPress + Contact Form 7 に載せるための手順書。

**2026-08-06 更新**: 実際の管理画面と既存フォームの中身を確認したため、推測で書いていた初版を全面的に差し替えた。

---

## 前提（実機で確認済み）

| 項目 | 内容 |
|---|---|
| サイト | WordPress |
| フォームプラグイン | Contact Form 7 |
| 送信先 | contact@charge10.tokyo |
| reCAPTCHA | **有効**（既存フォームに表記あり） |
| サンクスページ | `https://charge10.tokyo/thanks/` |

### 既存のフォーム3つ

| フォーム名 | ショートコード |
|---|---|
| お問い合わせフォーム | `[contact-form-7 id="317"]` |
| チャージイベントお問い合わせフォーム | `[contact-form-7 id="500"]` |
| **チャージオフィスお問い合わせフォーム** | `[contact-form-7 id="488"]` |

---

## 方針：488 を「複製」して LP 専用を作る

**488 を直接編集しないこと。** 既存ページで使われている可能性が高く、上書きするとそのページのフォームも変わる。

複製する利点：

- **メールタブを一切触らなくて済む**（フィールド名がそのまま引き継がれるため）
- reCAPTCHA・サンクスページへのリダイレクトも引き継がれる
- 既存サイトと同じ挙動になるので、先方が運用で戸惑わない

---

## 手順

### 1. 複製する

`お問い合わせ` → 一覧の「チャージオフィスお問い合わせフォーム」の下にある **`複製`** をクリック。
タイトルを **「CHARGE OFFICE LP」** に変更して保存。

### 2.「フォーム」タブを下記に差し替える

**CF7のタグ名（`your-name` `text-862` など）は複製元のまま変えていない。**
これを変えるとメールタブの設定が全部壊れるので、**タグ名は絶対に触らないこと。**

変えているのは次の3点だけ。

- ラッパーのHTMLを LP のクラス（`.form-field` など）に合わせた
- **希望申込内容**の選択肢を LP の導線に合わせた（提携企業 → 無料トライアル／資料請求）
- **サービスを知ったきっかけ**から「店舗からの案内」を削除した（出張型のため該当しない）

```html
<div class="form-grid">
  <div class="form-field">
    <label for="name">氏名<span class="req">必須</span></label>
    [text* your-name id:name autocomplete:name]
  </div>
  <div class="form-field">
    <label for="company">会社名<span class="req">必須</span></label>
    [text* text-862 id:company autocomplete:organization]
  </div>
  <div class="form-field">
    <label for="address">住所<span class="req">必須</span></label>
    [text* text-905 id:address autocomplete:street-address]
  </div>
  <div class="form-field">
    <label for="email">メールアドレス<span class="req">必須</span></label>
    [email* your-email id:email autocomplete:email]
  </div>
  <div class="form-field">
    <label for="tel">電話番号<span class="req">必須</span></label>
    [tel* tel-731 id:tel autocomplete:tel]
  </div>
  <div class="form-field">
    <label for="size">従業員数<span class="req">必須</span></label>
    [select* menu-43 id:size include_blank "1〜10名" "11〜30名" "31〜50名" "51〜100名" "101〜300名" "301名以上"]
  </div>

  <fieldset class="form-field form-field--radio">
    <legend>希望申込内容<span class="req">必須</span></legend>
    [radio radio-391 use_label_element default:1 "無料トライアルのお申し込み" "資料請求" "サービスについての質問" "その他"]
  </fieldset>

  <fieldset class="form-field form-field--radio">
    <legend>サービスを知ったきっかけ<span class="req">必須</span></legend>
    [radio radio-129 use_label_element default:1 "テレビ・新聞・雑誌・ラジオ" "インターネット検索" "インターネット広告" "SNS" "Webサイト、ブログ" "チラシ" "家族、知人からの紹介" "その他"]
  </fieldset>

  <div class="form-field">
    <label for="msg">質問・ご要望</label>
    [textarea your-message id:msg placeholder "無料トライアル希望、資料請求など"]
  </div>

  <p class="cta-note cta-note--left">ご入力いただいた個人情報は、お問い合わせへの回答および無料トライアル・資料のご案内にのみ利用します。第三者に提供することはありません。</p>

  <div class="form-confirm">
    [acceptance acceptance-683] 入力内容をご確認の上、チェックをお願いします。 [/acceptance]
  </div>

  <p class="cta-note cta-note--left">このサイトはreCAPTCHAによって保護されており、Googleの<a style="text-decoration:underline;" href="https://policies.google.com/privacy">プライバシーポリシー</a>と<a href="https://policies.google.com/terms" style="text-decoration:underline;">利用規約</a>が適用されます。</p>

  <div class="form-actions">
    [submit class:btn class:btn--primary class:btn--block "入力内容を送信する"]
  </div>
</div>

<script>
document.addEventListener( 'wpcf7mailsent', function( event ) {
  location = 'https://charge10.tokyo/thanks/';
}, false );
</script>
```

#### 貼り付け時に崩さないための4つのルール（実機シミュレーションで確認済み）

CF7の出力構造を再現したテストページを作り、LPのCSSで描画して検証した結果、
**下記を守れば静的HTML版とフォームの高さがピクセル単位で一致する**（375px幅で 1694px、実測）。

1. **`<label>` の中にCF7タグを入れない。** `<label>` とタグは兄弟にする
   （入れ子にするとラベル高が22px→66pxになり、ラベルと入力欄の間隔が -44px に潰れる）
2. **`id:` オプションを付ける。** `<label for="...">` と対応させるために必要
3. **`[submit]` に `class:btn class:btn--primary class:btn--block` を付ける。**
   付けないとCF7の素の `<input type="submit">` になりボタンの見た目が出ない
4. **確認チェックは `<label>` ではなく `<div class="form-confirm">` で囲む。**
   `[acceptance]` が内部で `<label>` を生成するため、labelの入れ子になり不正なHTMLになる


### 3.「メール」タブは触らない

複製元の設定（送信先 contact@charge10.tokyo・本文テンプレート）がそのまま使える。
**フィールド名を変えていないので編集は不要。**

念のため送信先が `contact@charge10.tokyo` になっていることだけ目視で確認する。

### 4. ショートコードをLPに貼る

保存すると新しいIDのショートコードが出る（例: `[contact-form-7 id="512" title="CHARGE OFFICE LP"]`）。
`index.html` の `<form class="form-grid">` 〜 `</form>` を、まるごとこのショートコードに差し替える。

### 5. LPを固定ページとして設置する

`styles.css` と `images/` をテーマ側に配置し、固定ページのテンプレートとして読み込ませる。

---

## 確定済みの判断

### ラジオボタンの必須について

初版の手順書で「CF7にはラジオの必須指定がないので必須が外れる」と書いたが、**既存フォームは `default:1` で1つ目を初期選択にすることで空送信を防いでいた。** 同じ方式を採用したので問題は解消。

ただし副作用として、**ユーザーが何も選ばなかった場合は1つ目が送信される。**
LPでは1つ目を「無料トライアルのお申し込み」にしてあるので、主CTAと一致していて不都合はない。

### 従業員数の区分

LPの元案（〜29名／30〜99名／100〜299名／300名〜）ではなく、**既存フォームの6段階に合わせた。**
理由は、先方が既存フォームで集めているデータと区分が揃っていないと集計できなくなるため。

### reCAPTCHAの表記

LP制作時は「実装していない機能を謳うのは事実と異なる」という理由で表記を入れていなかったが、
**実際にはサイトでreCAPTCHAが有効だったため、表記を入れる方針に変更した。**

---

## LP側に反映が必要な項目

CF7に載せる前に `index.html` / `styles.css` 側で対応しておくもの。

- [x] CF7の出力（`.wpcf7-list-item` / `[acceptance]`）に対応したCSSを追加
- [x] 従業員数の選択肢を既存の6段階に変更
- [x] きっかけの表記を既存に統一（知人からの紹介 → 家族、知人からの紹介）
- [x] reCAPTCHAの表記を追加
- [x] `.radio-option` の詳細度を修正し、CF7版とラジオの見た目を一致させた
- [ ] 送信後の遷移先（`https://charge10.tokyo/thanks/`）はCF7側のJSで処理するため、静的HTML側の対応は不要

**LP側の準備は完了。残りはWordPress側の作業のみ。**

---

## スコープについて

WordPressへの移植・CF7設定・サーバー設置は当初の合意範囲（デザインモック／設計書／実装／公開前レビュー／表示検証）に含まれない。
オーナー判断で追加見積もりは挟まず進める方針だが、**実工数は記録すること**（受託部門ルール／価格改定の根拠になるため）。
