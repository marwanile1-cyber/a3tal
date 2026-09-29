<?php
if (!defined('ABSPATH')) exit;
define('A3AP_VERSION','1.0.0');

function a3ap_setup(){
  add_theme_support('title-tag');
  add_theme_support('post-thumbnails');
  add_theme_support('custom-logo',['height'=>90,'width'=>300,'flex-height'=>true,'flex-width'=>true]);
  add_theme_support('responsive-embeds');
  add_theme_support('html5',['search-form','gallery','caption','style','script']);
  register_nav_menus(['primary'=>'القائمة الرئيسية','footer'=>'قائمة الفوتر']);
}
add_action('after_setup_theme','a3ap_setup');

function a3ap_assets(){
  wp_enqueue_style('a3ap-fonts','https://fonts.googleapis.com/css2?family=Alexandria:wght@500;600;700;800&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap',[],null);
  wp_enqueue_style('a3ap-style',get_stylesheet_uri(),['a3ap-fonts'],A3AP_VERSION);
  wp_enqueue_script('a3ap-theme',get_template_directory_uri().'/assets/js/theme.js',[],A3AP_VERSION,true);
}
add_action('wp_enqueue_scripts','a3ap_assets');
add_action('wp_head',function(){echo '<meta name="theme-color" content="#0B1220">'.PHP_EOL;},1);

function a3ap_cat_link($id){$u=get_category_link((int)$id);return is_wp_error($u)?home_url('/'):$u;}
function a3ap_search($q=''){return add_query_arg('s',$q,home_url('/'));}
function a3ap_read_time($id=0){$id=$id?:get_the_ID();$t=wp_strip_all_tags((string)get_post_field('post_content',$id));$w=preg_split('/\s+/u',trim($t));return max(1,(int)ceil(count(array_filter((array)$w))/220));}
function a3ap_primary_cat($id=0){$id=$id?:get_the_ID();$c=get_the_category($id);return $c?($c[0]??null):null;}
function a3ap_excerpt($id=0,$words=23){$id=$id?:get_the_ID();$x=get_the_excerpt($id);if(!$x)$x=wp_strip_all_tags((string)get_post_field('post_content',$id));return wp_trim_words($x,$words);}
function a3ap_is_diagnostic($id=0){$id=$id?:get_the_ID();return has_category([2,8,9,10,11,12,13,14,15,18,298],$id);}

function a3ap_card($id=0,$class=''){
  $id=$id?:get_the_ID();$cat=a3ap_primary_cat($id);?>
  <article class="ap-card <?php echo esc_attr($class); ?>">
    <a class="ap-card-media" href="<?php echo esc_url(get_permalink($id)); ?>">
      <?php if(has_post_thumbnail($id)){echo get_the_post_thumbnail($id,'large',['loading'=>'lazy']);}else{echo '<span class="ap-fallback">A3TAL</span>';} ?>
    </a>
    <div class="ap-card-body">
      <?php if($cat): ?><a class="ap-kicker" href="<?php echo esc_url(get_category_link($cat)); ?>"><?php echo esc_html($cat->name); ?></a><?php endif; ?>
      <h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3>
      <p><?php echo esc_html(a3ap_excerpt($id,20)); ?></p>
      <div class="ap-meta"><span><?php echo esc_html(get_the_modified_date('j M',$id)); ?></span><span><?php echo esc_html(a3ap_read_time($id)); ?> دقائق</span></div>
    </div>
  </article><?php
}

function a3ap_compact($id=0){$id=$id?:get_the_ID();$cat=a3ap_primary_cat($id);?>
  <article class="ap-compact">
    <a class="ap-compact-media" href="<?php echo esc_url(get_permalink($id)); ?>"><?php if(has_post_thumbnail($id)){echo get_the_post_thumbnail($id,'medium_large',['loading'=>'lazy']);}else{echo '<span class="ap-fallback">A3</span>';} ?></a>
    <div><?php if($cat): ?><span class="ap-kicker"><?php echo esc_html($cat->name); ?></span><?php endif; ?><h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3><div class="ap-meta"><span><?php echo esc_html(get_the_modified_date('j M',$id)); ?></span></div></div>
  </article><?php
}
function a3ap_query($args=[]){return new WP_Query(wp_parse_args($args,['post_type'=>'post','post_status'=>'publish','ignore_sticky_posts'=>true]));}
function a3ap_heading_ids($content){
  if(!is_singular())return $content;$used=[];
  return preg_replace_callback('/<h([23])([^>]*)>(.*?)<\/h\1>/isu',function($m)use(&$used){
    if(preg_match('/\sid=["\'][^"\']+["\']/i',$m[2]))return $m[0];
    $plain=trim(wp_strip_all_tags($m[3]));$base=sanitize_title($plain);if(!$base)$base='section';$id=$base;$n=2;while(isset($used[$id])){$id=$base.'-'.$n++;}$used[$id]=1;
    return '<h'.$m[1].$m[2].' id="'.esc_attr($id).'">'.$m[3].'</h'.$m[1].'>';
  },$content);
}
add_filter('the_content','a3ap_heading_ids',8);
function a3ap_toc(){
  $content=(string)get_post_field('post_content',get_the_ID());preg_match_all('/<h2[^>]*>(.*?)<\/h2>/isu',$content,$m);$out=[];
  foreach($m[1]??[] as $raw){$t=trim(wp_strip_all_tags($raw));if($t)$out[]=['t'=>$t,'id'=>sanitize_title($t)];}
  return $out;
}
