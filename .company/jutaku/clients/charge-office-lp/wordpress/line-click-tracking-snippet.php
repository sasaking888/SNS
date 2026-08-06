<?php
/**
 * LP内のLINEボタンのクリックを LINEClick イベントとして計測する
 *
 * ・CHARGE OFFICE LP のページでのみ動く（他ページには影響しない）
 * ・Lead ではなく独自イベントとして送るため、既存のコンバージョン最適化を汚さない
 * ・どちらのボタンを押したか（最終CTA / 追随CTA）も一緒に送る
 * ・管理画面にログイン中は送らない
 *
 * 使い方: Code Snippets プラグインに追加して有効化する
 *
 * 2026-08-06
 */

add_action( 'wp_footer', function () {

	if ( is_user_logged_in() ) {
		return;
	}

	// このスニペットが動くのは LP 用テンプレートのページだけ
	if ( ! is_page() || 'co-lp' !== get_page_template_slug( get_queried_object_id() ) ) {
		return;
	}
	?>
<script>
(function () {
	document.addEventListener( 'click', function ( e ) {

		var link = e.target.closest( 'a[href*="lin.ee"]' );
		if ( ! link ) {
			return;
		}

		if ( ! window.fbq ) {
			return;
		}

		// 追随CTA（画面下に固定されているほう）か、ページ内のCTAかを区別する
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
