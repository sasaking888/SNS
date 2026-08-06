<?php
/**
 * Meta ピクセル（ID: 930843926650257）を全ページに設置する
 *
 * ・全ページで PageView を送信
 * ・サンクスページに ?lp=office が付いているときだけ Lead を送信
 *   （既存フォーム 317 / 500 / 488 の問い合わせは lp=office が付かないので混ざらない）
 *
 * 使い方: Code Snippets プラグインに追加して有効化する
 *
 * 2026-08-06
 */

add_action( 'wp_head', function () {

	$pixel_id = '930843926650257';

	// 管理画面にログイン中の自分のアクセスは数えない（テストでCVが増えるのを防ぐ）
	if ( is_user_logged_in() ) {
		return;
	}
	?>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window,document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '<?php echo esc_js( $pixel_id ); ?>');
fbq('track', 'PageView');
<?php
	// CHARGE OFFICE LP 経由の問い合わせ完了だけ Lead として送る
	$is_lp_thanks = isset( $_GET['lp'] ) && 'office' === $_GET['lp'];
	if ( $is_lp_thanks ) {
		?>
fbq('track', 'Lead', { content_name: 'CHARGE OFFICE LP' });
		<?php
	}
	?>
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=<?php echo esc_attr( $pixel_id ); ?>&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
	<?php
}, 1 );
