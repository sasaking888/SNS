<?php
/**
 * Meta ピクセルに Lead イベントだけを追加する
 * （ピクセル本体は既にサイトに設置済みのため、ここでは init も PageView も送らない）
 *
 * ・サンクスページに ?lp=office が付いているときだけ Lead を送信
 *   → 既存フォーム 317 / 500 / 488 の問い合わせは混ざらない
 * ・管理画面にログイン中は送らない（動作確認でCVが増えるのを防ぐ）
 *
 * 使い方: Code Snippets プラグインに追加して有効化する
 *
 * 2026-08-06
 */

add_action( 'wp_footer', function () {

	if ( is_user_logged_in() ) {
		return;
	}

	if ( ! isset( $_GET['lp'] ) || 'office' !== $_GET['lp'] ) {
		return;
	}
	?>
<script>
/* ピクセル本体の読み込みが終わるのを待ってから Lead を送る */
(function () {
	var tries = 0;
	function fire() {
		if ( window.fbq ) {
			fbq( 'track', 'Lead', { content_name: 'CHARGE OFFICE LP' } );
			return;
		}
		if ( ++tries < 20 ) {
			setTimeout( fire, 300 );
		}
	}
	fire();
})();
</script>
	<?php
}, 99 );
