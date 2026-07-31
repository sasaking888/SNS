# 指示書: ヒーロー直下3タイルの再デザイン（2026-07-30）

対象案件: CHARGE OFFICE LP
対象ファイル: `.company/jutaku/clients/charge-office-lp/index.html`, `.company/jutaku/clients/charge-office-lp/styles.css`
関連ブランチ: `claude/lp-credit-optimization-f58d45`（現在のブランチのまま作業してよい。新規ブランチは切らない）

**作業前に必ず `GROK-RULES.md` と `CLAUDE-HANDOFF.md` を読むこと。** 数字・法令文言・禁止語のルールはこの指示書より優先される。

---

## 背景

ヒーロー写真の下にある3枚のタイル（省スペース／高回転／高品質）が「白背景・細い罫線・地味」でインパクトが弱いとオーナーから指摘があった。検討の結果、以下の方針で合意済み。**方針は確定しているので、再提案や別案の相談は不要。このまま実装してよい。**

- 色は白ベースをやめ、**このサイトが既に使っているネイビー（`--c-navy`）を背景にした帯**にする（新しい色を持ち込まない。「安心のサポート体制」セクションで既にネイビー背景は使用実績あり）
- アイコンは黄色い丸＋白線アイコン、右下に小さい黄色チェックマークバッジを添える（参考: オーナー提供の資料。ただしチェックマークの色は緑ではなく黄色系にする。理由: 緑はこのサイトのどこにも使われていない色のため）
- **数字を主役にする**（ヒーローのメダル演出「94.2%」「98.4%」と同じ言語）。各タイルの本文からすでにある数字を抜き出し、大きな数字として上部に表示する
- スマホでも**3列を維持し、縦に積み上げない**（現状は720px未満で1列に潰れて縦長になっている。これが「長い」という不満の一因）
- **文言・数字は一切変えない。** 追加する「大きな数字」は、既存の本文にすでに書かれている数字をそのまま抜き出すだけ（新しい数字を作らない・計算し直さない）

---

## 1. HTML変更（`index.html`）

対象は `id="badges"` の3枚の `<article class="badge-card">`（現在72〜104行目付近）。

### 変更内容（3枚共通のパターン）

各カードで以下2点を追加する。**本文・タイトルの文言は一切変更しない。**

1. `.badge-card__icon` の中の `<svg>` の直後に、チェックマークバッジ用の `<span>` を追加
2. `.badge-card__icon` の直後・`<h3 class="badge-card__title">` の直前に、大きい数字用の `<p class="badge-card__number">` を追加

### カード1（省スペース）

```html
<article class="badge-card">
  <div class="badge-card__icon" aria-hidden="true">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 8V3h5M21 8V3h-5M3 16v5h5M21 16v5h-5"/>
      <rect x="8" y="8" width="8" height="8" rx="1"/>
    </svg>
    <span class="badge-card__check" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>
    </span>
  </div>
  <p class="badge-card__number">0.5畳</p>
  <h3 class="badge-card__title">省スペース</h3>
  <p class="badge-card__text">たった0.5畳分のスペースでOK</p>
</article>
```

### カード2（高回転）

同じパターンでチェックマーク `<span>` を追加し、`<p class="badge-card__number">10分</p>` を `<h3>` の前に追加する（本文「おひとり約10分・1時間で約5名」はそのまま）。

### カード3（高品質）

同じパターンでチェックマーク `<span>` を追加し、`<p class="badge-card__number">33万人+</p>` を `<h3>` の前に追加する（本文「グループ累計33万人以上の施術実績」はそのまま。**12万人ではなく33万人が現在の確定値**。CLAUDE-HANDOFF.mdで確認すること）。

---

## 2. CSS変更（`styles.css`）— 重要: このファイルは修正パッチが積み重なっている

`.badge-card` / `.badge-grid` / `.hero__badges-post` は**現在2箇所で重複して上書きされている**（後述）。新しいルールを追記すると3つ目の重複ができて余計に壊れやすくなるので、**既存の該当ブロックを直接書き換えること。ファイル末尾への追記は禁止。**

### 2-1. `/* 写真の後ろの3タイル */` ブロックを書き換える

現在（351〜393行目付近、`.hero__badges-post` の定義一式）:

```css
/* 写真の後ろの3タイル */
.hero__badges-post {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: 4px;
  margin-bottom: 0;
}
.hero__badges-post .badge-card__icon {
  background: rgba(245, 182, 42, 0.18);
  color: var(--c-yellow);
}
.hero__badges-post .badge-card__icon svg {
  stroke: var(--c-yellow);
}
@media (max-width: 719px) {
  .hero__badges-post {
    grid-template-columns: 1fr;
  }
  .hero__badges-post .badge-card {
    display: grid;
    grid-template-columns: 40px 1fr;
    grid-template-areas:
      "icon title"
      "icon text";
    column-gap: 12px;
    row-gap: 2px;
    align-items: center;
    text-align: left;
    padding: 12px 16px;
  }
  .hero__badges-post .badge-card__icon {
    grid-area: icon;
    margin: 0;
  }
  .hero__badges-post .badge-card__title {
    grid-area: title;
    margin-bottom: 0;
  }
  .hero__badges-post .badge-card__text {
    grid-area: text;
  }
}
```

これを、**3列を常に維持する**版に書き換える（`@media (max-width: 719px)` ブロックごと削除してよい。中身の1列レイアウトはもう使わない）:

```css
/* 写真の後ろの3タイル（2026-07-30 再デザイン: ネイビー帯・数字を主役に・3列固定） */
.hero__badges-post {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 4px;
  margin-top: 4px;
  margin-bottom: 0;
  background: var(--c-navy);
  border-radius: var(--radius);
  padding: 20px 6px;
}
@media (min-width: 720px) {
  .hero__badges-post { padding: 28px 16px; gap: 12px; }
}
```

### 2-2. 重複パッチ `[1]` を無効化する

`/* --- [1] スマホでバッジ3枚が横並び固定になり... --- */` というコメントの付いたブロック（1390〜1414行目付近）が、上と同じ「720px未満で1列にする」処理を**別のセレクタ（`.badge-grid` / `.badge-card`）で二重に行っている。** これも書き換える。

現在:

```css
@media (max-width: 719px) {
  .badge-grid {
    grid-template-columns: 1fr;
    gap: var(--s-2);
  }
  .badge-card {
    display: grid;
    grid-template-columns: 40px 1fr;
    grid-template-areas:
      "icon title"
      "icon text";
    column-gap: var(--s-2);
    row-gap: 2px;
    align-items: center;
    text-align: left;
    padding: var(--s-2) var(--s-3);
  }
  .badge-card__icon  { grid-area: icon; margin: 0; }
  .badge-card__title { grid-area: title; margin-bottom: 0; }
  .badge-card__text  { grid-area: text; }
}
```

これを丸ごと削除し、代わりに1行のコメントだけ残す（**削除の記録を残すため、無言で消さない**）:

```css
/* --- [1] （2026-07-30 廃止）3タイルは常に3列を維持する方針に変更したため、
   720px未満で1列に潰す処理は不要になった。書き換えは「写真の後ろの3タイル」ブロック側で実施。 --- */
```

### 2-3. `.badge-card` 本体のスタイルを書き換える

現在（417〜460行目付近）:

```css
.badge-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: var(--s-4);
}
.badge-card {
  background: var(--c-bg);
  border: 1px solid var(--c-line);
  border-radius: var(--radius);
  padding: var(--s-3);
  text-align: center;
}
.badge-card__icon {
  width: 40px;
  height: 40px;
  margin: 0 auto var(--s-2);
  border-radius: 50%;
  background: rgba(245, 182, 42, 0.15);
  color: var(--c-navy);
  display: grid;
  place-items: center;
  font-size: 18px;
  font-weight: 700;
}
.badge-card__title {
  font-family: var(--f-head);
  font-weight: 700;
  font-size: 16px;
  color: var(--c-navy);
  margin-bottom: 6px;
}
.badge-card__text {
  font-size: 13px;
  color: var(--c-mute);
  line-height: 1.6;
}
```

これを次のように書き換える（`.badge-grid` は他のセクションで使われていないことを確認済み。このLP内で `class="badge-grid"` は1箇所のみ）:

```css
.badge-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: var(--s-4);
}
.badge-card {
  background: transparent;
  border: none;
  border-radius: var(--radius);
  padding: var(--s-2) 2px;
  text-align: center;
}
.badge-card__icon {
  position: relative;
  width: 44px;
  height: 44px;
  margin: 0 auto var(--s-2);
  border-radius: 50%;
  background: var(--c-yellow);
  color: var(--c-navy);
  display: grid;
  place-items: center;
}
.badge-card__icon svg {
  display: block;
  stroke: var(--c-navy);
}
.badge-card__check {
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--c-navy);
  border: 2px solid var(--c-yellow);
  display: grid;
  place-items: center;
  color: var(--c-yellow);
}
.badge-card__check svg {
  width: 9px;
  height: 9px;
  display: block;
}
.badge-card__number {
  font-family: var(--f-head);
  font-weight: 900;
  font-size: 20px;
  color: var(--c-yellow);
  line-height: 1.2;
  margin: 0 0 2px;
}
.badge-card__title {
  font-family: var(--f-head);
  font-weight: 700;
  font-size: 12px;
  color: #FFFFFF;
  margin-bottom: 4px;
}
.badge-card__text {
  font-size: 10.5px;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.5;
}
@media (min-width: 720px) {
  .badge-card__icon { width: 56px; height: 56px; }
  .badge-card__icon svg { width: 26px; height: 26px; }
  .badge-card__check { width: 22px; height: 22px; }
  .badge-card__check svg { width: 12px; height: 12px; }
  .badge-card__number { font-size: 30px; }
  .badge-card__title { font-size: 15px; }
  .badge-card__text { font-size: 13px; }
}
```

### 2-4. `.badge-card__icon svg { display: block; }`（1450行目付近、パッチ[6]内）

このルールは上の2-3で `.badge-card__icon svg` に `display:block` を含めたため重複する。**削除せず残してよい**（同じ値なので害はない。GROK-RULESの「既存クラス名を変えない」原則に従い、無理に触らない）。

---

## 3. 自己検証（提出前に必ず実施）

Playwrightで以下を確認し、スクリーンショットを撮って自分の目で確認すること（「たぶん入る」で済ませない）。

- [ ] **320px, 375px, 390px, 768px, 1200px** の5幅で `document.documentElement.scrollWidth > document.documentElement.clientWidth` が **false**（横スクロールなし）
- [ ] 320px幅でも3列のまま崩れていない（縦1列に戻っていないこと）
- [ ] 各タイルの本文（例:「おひとり約10分・1時間で約5名」）が1〜2文字だけ次の行に落ちる不自然な折り返しになっていないか
- [ ] チェックマークバッジがアイコンの丸からはみ出しすぎていないか
- [ ] ネイビー帯の中の白文字・黄色文字が背景に対してちゃんと読めるコントラストか
- [ ] 数字（0.5畳 / 10分 / 33万人+）が本文の数字（0.5畳分 / 約10分 / 33万人以上）と一致しているか（新しい数字を作っていないか）
- [ ] ヒーローの他の要素（写真のフルブリード、メダル、CTA、見出しの黄色サブコピーなど）を誤って変更していないか（`git diff` で意図した箇所だけが変わっていることを確認）

---

## 4. プレビューの更新

`/tmp/claude-0/-home-user-SNS/3dc91a25-3c20-53f2-b2d2-d96d2c55cab2/scratchpad/build_preview.py` を実行して `charge-office-preview.html` を再生成し、既存のArtifact URL（`https://claude.ai/code/artifact/38f6aaca-83aa-41ec-93e1-2febccb6787a`）に再公開すること（同じfile_pathで再publishすればURLは変わらない）。

## 5. 記録とコミット

- `.company/jutaku/clients/charge-office.md` に追記1件（変更内容・確認結果・幅ごとのスクリーンショット確認結果を記載）。既存ファイルへの追記のみ。上書き禁止
- `git add` → `git commit`（日本語の短いメッセージ）→ `git push -u origin claude/lp-credit-optimization-f58d45`
- 作業が終わったら、この指示書ファイル（`INSTRUCTIONS-tile-redesign.md`）は削除せず残してよい（経緯の記録として）

## 6. 報告

作業完了後、変更した箇所の差分要約とスクリーンショットでの確認結果を報告すること。全文の再出力は不要。
