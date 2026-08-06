<?php
/**
 * CHARGE OFFICE LP 専用の全幅テンプレートを追加する
 *
 * このサイトのテーマは固定ページの本文をそのまま出力しないため、
 * 本文だけを素のHTMLとして出力するテンプレートを1つ追加する。
 * テーマのヘッダー・フッターを読み込まないので、既存ページには一切影響しない。
 *
 * 使い方:
 *   1) このコードを functions.php の末尾、または Code Snippets プラグインに追加
 *   2) 固定ページの編集画面の右サイドバーに「テンプレート」が出るので
 *      「CHARGE OFFICE LP（全幅）」を選んで更新
 *
 * 2026-08-06
 */

/* 固定ページのテンプレート一覧に選択肢を追加する */
add_filter( 'theme_page_templates', function ( $templates ) {
	$templates['co-lp'] = 'CHARGE OFFICE LP（全幅）';
	return $templates;
} );

/* 上のテンプレートが選ばれている固定ページだけ、本文を素のHTMLとして出力する */
add_action( 'template_redirect', function () {

	if ( ! is_page() ) {
		return;
	}

	if ( 'co-lp' !== get_page_template_slug( get_queried_object_id() ) ) {
		return;
	}

	while ( have_posts() ) {
		the_post();
		?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php the_content(); ?>
<?php wp_footer(); ?>
</body>
</html>
		<?php
	}

	exit;
} );
