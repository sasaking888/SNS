<?php
/**
 * 【テスト専用】LINEボタンのクリック計測
 *
 * ログイン中の除外を外した版。テストイベントで確認するためだけのもの。
 * 確認が取れたら必ず line-click-tracking-snippet.php（除外あり）に戻すこと。
 * このまま運用すると、管理者自身のクリックが件数に混ざる。
 *
 * 2026-08-06
 */

add_action( 'wp_footer', function () {

	if ( ! is_page() || 'co-lp' !== get_page_template_slug( get_queried_object_id() ) ) {
		return;
	}
	?>
<script>
(function () {
	document.addEventListener( 'click', function ( e ) {
		var link = e.target.closest( 'a[href*="lin.ee"]' );
		if ( ! link || ! window.fbq ) {
			return;
		}
		var place = link.closest( '.sticky-cta' ) ? '追随CTA' : '最終CTA';
		fbq( 'trackCustom', 'LINEClick', {
			content_name: 'CHARGE OFFICE LP',
			placement: place
		} );
	}, true );
})();
</script>
	<?php
}, 99 );
