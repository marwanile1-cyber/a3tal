<?php
if (!defined('ABSPATH')) exit;

define('A3TAL_DIAGNOSTIC_VERSION','0.9.0');

function a3du_setup(){
  add_theme_support('title-tag');
  add_theme_support('post-thumbnails');
  add_theme_support('custom-logo',['height'=>80,'width'=>260,'flex-height'=>true,'flex-width'=>true]);
  add_theme_support('responsive-embeds');
  add_theme_support('html5',['search-form','gallery','caption','style','script']);
  register_nav_menus(['primary'=>'القائمة الرئيسية','footer'=>'روابط الفوتر']);
}
add_action('after_setup_theme','a3du_setup');

function a3du_assets(){
  wp_enqueue_style('a3du-fonts','https://fonts.googleapis.com/css2?family=Alexandria:wght@500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap',[],null);
  wp_enqueue_style('a3du-style',get_stylesheet_uri(),['a3du-fonts'],A3TAL_DIAGNOSTIC_VERSION);
  wp_enqueue_script('a3du-theme',get_template_directory_uri().'/assets/js/theme.js',[],A3TAL_DIAGNOSTIC_VERSION,true);
}
add_action('wp_enqueue_scripts','a3du_assets');

function a3du_read_time($id=0){
  $id=$id?:get_the_ID();
  $text=wp_strip_all_tags((string)get_post_field('post_content',$id));
  $words=preg_split('/\s+/u',trim($text));
  return max(1,(int)ceil(count(array_filter((array)$words))/220));
}

function a3du_search_url($term=''){
  return add_query_arg('s',$term,home_url('/'));
}

function a3du_menu_fallback(){
  echo '<ul>';
  $items=[
    ['شخّص عطل',a3du_search_url('عطل')],
    ['أكواد DTC',a3du_search_url('P0420')],
    ['الصيانة',a3du_search_url('صيانة')],
    ['دليل السيارات',a3du_search_url('دليل السيارات')],
    ['مراكز الخدمة',a3du_search_url('مركز خدمة')],
  ];
  foreach($items as $item){
    echo '<li><a href="'.esc_url($item[1]).'">'.esc_html($item[0]).'</a></li>';
  }
  echo '</ul>';
}

function a3du_post_card($id=0){
  $id=$id?:get_the_ID();
  $cats=get_the_category($id);
  $label=$cats?($cats[0]->name??'تشخيص'):'تشخيص';
  echo '<article class="a3-post-card">';
  echo '<a class="a3-post-thumb" href="'.esc_url(get_permalink($id)).'">';
  if(has_post_thumbnail($id)){
    echo get_the_post_thumbnail($id,'large',['loading'=>'lazy']);
  }else{
    echo '<div style="height:100%;display:grid;place-items:center;background:linear-gradient(135deg,#0B1220,#18304D);color:#67E8F9;font:900 30px ui-monospace">A3TAL</div>';
  }
  echo '</a><div class="a3-post-body">';
  echo '<span class="a3-post-type">'.esc_html($label).'</span>';
  echo '<h3><a href="'.esc_url(get_permalink($id)).'">'.esc_html(get_the_title($id)).'</a></h3>';
  $excerpt=get_the_excerpt($id);
  if(!$excerpt) $excerpt=wp_trim_words(wp_strip_all_tags((string)get_post_field('post_content',$id)),22);
  echo '<p>'.esc_html(wp_trim_words($excerpt,22)).'</p>';
  echo '<div class="a3-post-meta"><span>'.esc_html(get_the_modified_date('j M Y',$id)).'</span><span>'.esc_html(a3du_read_time($id)).' دقائق</span></div>';
  echo '</div></article>';
}

function a3du_article_meta($key,$fallback){
  $v=trim((string)get_post_meta(get_the_ID(),$key,true));
  return $v!==''?$v:$fallback;
}

function a3du_inject_heading_ids($content){
  if(!is_singular('post')) return $content;
  $used=[];
  $content=preg_replace_callback('/<h([23])([^>]*)>(.*?)<\/h\1>/isu',function($m)use(&$used){
    if(preg_match('/\sid=["\'][^"\']+["\']/i',$m[2])) return $m[0];
    $plain=wp_strip_all_tags($m[3]);
    $base=sanitize_title($plain);
    if($base==='') $base='section';
    $id=$base;$n=2;
    while(isset($used[$id])){$id=$base.'-'.$n;$n++;}
    $used[$id]=true;
    return '<h'.$m[1].$m[2].' id="'.esc_attr($id).'">'.$m[3].'</h'.$m[1].'>';
  },$content);
  return $content;
}
add_filter('the_content','a3du_inject_heading_ids',8);

function a3du_toc(){
  $content=(string)get_post_field('post_content',get_the_ID());
  preg_match_all('/<h2[^>]*>(.*?)<\/h2>/isu',$content,$m);
  $items=[];
  foreach($m[1]??[] as $raw){
    $title=trim(wp_strip_all_tags($raw));
    if($title==='') continue;
    $items[]=['title'=>$title,'id'=>sanitize_title($title)];
  }
  return $items;
}
